import pandas as pd
from async_lru import alru_cache

from toolfront.config import ALRU_CACHE_TTL
from toolfront.models.database import Database, DatabaseError, SQLAlchemyMixin


class Snowflake(SQLAlchemyMixin, Database):
    @alru_cache(maxsize=None, ttl=ALRU_CACHE_TTL)
    async def get_tables(self) -> list[str]:
        try:
            code = "SHOW TABLES IN ACCOUNT;"
            data = await self.query(code)
            if data is None or data.empty:
                return []
            return data.apply(lambda x: f"{x['database_name']}.{x['schema_name']}.{x['name']}", axis=1).tolist()
        except Exception as e:
            raise DatabaseError(f"Failed to get tables from Snowflake: {e}") from e

    async def inspect_table(self, table_path: str) -> pd.DataFrame:
        return await self.query(f"DESCRIBE TABLE {table_path}")

    async def sample_table(self, table_path: str, n: int = 5) -> pd.DataFrame:
        return await self.query(f"SELECT * FROM {table_path} TABLESAMPLE BERNOULLI ({n} ROWS);")
