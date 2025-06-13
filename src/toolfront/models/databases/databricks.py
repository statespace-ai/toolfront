"""
Databricks integration for Toolfront.
"""
import logging
import pandas as pd
from async_lru import alru_cache
from sqlalchemy.engine.url import URL

from toolfront.config import ALRU_CACHE_TTL
from toolfront.models.database import ConnectionResult, Database, DatabaseError, MatchMode

logger = logging.getLogger("toolfront")

class Databricks(Database):
    """Databricks connection manager with utility functions."""
    
    async def test_connection(self) -> ConnectionResult:
        """Test the connection to the database."""
        try:
            # Use a simple query to test connection
            await self.query("SELECT 1 as test")
            return ConnectionResult(connected=True, message="Connection successful")
        except Exception as e:
            return ConnectionResult(connected=False, message=f"Connection failed: {e}")
    
    async def query(self, code: str) -> pd.DataFrame:
        """Execute a SQL query using Databricks SQL connector."""
        try:
            # Import here to avoid dependency issues
            from databricks import sql
            
            hostname = self.url.host
            http_path = self.url.query.get("http_path", "")
            token = self.url.query.get("token", "")
            
            if not http_path or not token:
                raise ValueError("http_path and token are required in the URL")
            
            logger.debug(f"Connecting to Databricks: hostname={hostname}")
            
            # Create a connection
            with sql.connect(
                server_hostname=hostname,
                http_path=http_path,
                access_token=token,
                _timeout=30
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(code)
                    if cursor.description:
                        # Convert result to DataFrame
                        columns = [column[0] for column in cursor.description]
                        data = cursor.fetchall()
                        return pd.DataFrame(data, columns=columns)
                    else:
                        # No results (e.g., for DDL statements)
                        return pd.DataFrame()
        except ImportError:
            raise DatabaseError(
                "databricks-sql-connector package is required for Databricks integration. "
                "Please install with: pip install toolfront[databricks]"
            )
        except Exception as e:
            raise DatabaseError(f"Query execution failed: {e}")

    @alru_cache(maxsize=None, ttl=ALRU_CACHE_TTL)
    async def get_tables(self) -> list[str]:
        """Get list of all tables in all catalogs and schemas."""
        try:
            code = "SHOW TABLES"
            data = await self.query(code)
            
            if data is None or data.empty:
                return []
                
            columns = data.columns.tolist()
            
            if 'database' in columns and 'tableName' in columns:
                # Standard Databricks format with database and tableName columns
                return [f"{row['database']}.{row['tableName']}" for _, row in data.iterrows()]
            elif 'databaseName' in columns and 'tableName' in columns:
                # Alternative format with databaseName column
                return [f"{row['databaseName']}.{row['tableName']}" for _, row in data.iterrows()]
            elif len(columns) >= 2:
                # Fallback: assume the first column is database/schema and second is table name
                return [f"{row[0]}.{row[1]}" for _, row in data.iterrows()]
            else:
                # If we can't determine the format, just return table names
                logger.warning("Couldn't determine table name format, returning raw table names")
                return [str(row[0]) for _, row in data.iterrows()]
                
        except Exception as first_error:
            logger.warning(f"First table listing method failed: {first_error}, trying alternative approach")
            
            try:
                code = """
                    SELECT 
                        table_catalog, 
                        table_schema, 
                        table_name
                    FROM information_schema.tables
                    WHERE table_type = 'BASE TABLE'
                    ORDER BY table_catalog, table_schema, table_name;
                """
                data = await self.query(code)
                
                if data is None or data.empty:
                    return []
                    
                return [f"{row[0]}.{row[1]}.{row[2]}" for _, row in data.iterrows()]
                
            except Exception as second_error:
                # If both approaches fail, log detailed error and raise exception
                logger.error(f"Failed to get tables from Databricks using multiple methods. Errors: {first_error}, {second_error}")
                raise DatabaseError(f"Failed to get tables from Databricks: {second_error}") from second_error

    async def scan_tables(self, pattern: str, mode: MatchMode = MatchMode.REGEX, limit: int = 10) -> list[str]:
        """Match table names using different algorithms."""
        try:
            table_names = await self.get_tables()
            if not table_names:
                return []
            if mode == MatchMode.REGEX:
                return self._scan_tables_regex(table_names, pattern, limit)
            elif mode == MatchMode.JARO_WINKLER:
                return self._scan_tables_jaro_winkler(table_names, pattern, limit)
            elif mode == MatchMode.TF_IDF:
                return self._scan_tables_tf_idf(table_names, pattern, limit)
            else:
                logger.warning(f"Unknown match mode: {mode}, falling back to regex")
                return self._scan_tables_regex(table_names, pattern, limit)
                
        except Exception as e:
            logger.error(f"Table scan failed for Databricks: {e}")
            raise DatabaseError(f"Failed to scan tables in Databricks: {e}") from e

    async def inspect_table(self, table_path: str) -> pd.DataFrame:
        """Get schema information for the specified table."""
        try:
            if not table_path:
                raise ValueError(f"Invalid table path: {table_path}")
                
            splits = table_path.split(".")
            
            if len(splits) == 3:
                catalog_name, schema_name, table_name = splits
                try:
                    code = f"""
                        SELECT
                            column_name,
                            data_type,
                            is_nullable,
                            column_default,
                            ordinal_position
                        FROM {catalog_name}.information_schema.columns
                        WHERE table_schema = '{schema_name}' 
                        AND table_name = '{table_name}'
                        ORDER BY ordinal_position;
                    """
                    return await self.query(code)
                except Exception as e:
                    logger.warning(f"Failed to inspect using catalog-specific information_schema: {e}")
                    return await self.query(f"DESCRIBE TABLE {table_path}")
            elif len(splits) == 2:
                schema_name, table_name = splits
                return await self.query(f"DESCRIBE TABLE {table_path}")
            else:
                raise ValueError(f"Invalid table path: {table_path}. Expected format: [catalog.]schema.table")
            
        except Exception as e:
            logger.error(f"Failed to inspect table {table_path} in Databricks: {e}")
            raise DatabaseError(f"Failed to inspect table {table_path} in Databricks: {e}") from e

    async def sample_table(self, table_path: str, n: int = 5) -> pd.DataFrame:
        """Get sample rows from the specified table."""
        try:
            if not table_path or not isinstance(table_path, str):
                raise ValueError(f"Invalid table path: {table_path}")
            
            if "." not in table_path and "`" not in table_path:
                logger.warning(f"Table path doesn't contain schema: {table_path}")
            try:
                return await self.query(f"SELECT * FROM {table_path} LIMIT {n}")
            except Exception as e:
                logger.warning(f"Failed to sample table with LIMIT clause: {e}")
                
                try:
                    return await self.query(f"SELECT * FROM {table_path} TABLESAMPLE ({n} ROWS)")
                except Exception as e2:
                    logger.warning(f"Failed to sample table with TABLESAMPLE: {e2}")
                    return await self.query(f"SELECT * FROM {table_path} LIMIT {n}")
                    
        except Exception as e:
            logger.error(f"Failed to sample table {table_path} in Databricks: {e}")
            raise DatabaseError(f"Failed to sample table {table_path} in Databricks: {e}") from e