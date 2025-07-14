import pandas as pd

from toolfront.config import CACHE_TTL
from toolfront.models.database_connections.base import DatabaseConnection, SyncSQLAlchemyMixin
from toolfront.utils import cache


class SnowflakeConnection(SyncSQLAlchemyMixin, DatabaseConnection):
    @cache(expire=CACHE_TTL)
    async def get_tables(self) -> list[str]:
        """For Snowflake, this method returns both tables and views combined"""
        try:
            # Get both tables and views
            tables_code = "SHOW TABLES IN ACCOUNT;"
            views_code = "SHOW VIEWS IN ACCOUNT;"

            tables_data = self.query(tables_code)
            views_data = self.query(views_code)

            # Comb?ine the results
            combined_data = pd.DataFrame()

            if tables_data is not None and not tables_data.empty:
                combined_data = pd.concat([combined_data, tables_data], ignore_index=True)

            if views_data is not None and not views_data.empty:
                combined_data = pd.concat([combined_data, views_data], ignore_index=True)

            if combined_data.empty:
                return []

            return combined_data.apply(
                lambda x: f"{x['database_name']}.{x['schema_name']}.{x['name']}", axis=1
            ).tolist()
        except Exception as e:
            raise ConnectionError(f"Failed to get tables and views from Snowflake: {e}") from e

    async def inspect_table(self, table_path: str) -> pd.DataFrame:
        return self.query(f"DESCRIBE TABLE {table_path}")

    async def sample_table(self, table_path: str, n: int = 5) -> pd.DataFrame:
        return self.query(f"SELECT * FROM {table_path} TABLESAMPLE BERNOULLI ({n} ROWS);")
