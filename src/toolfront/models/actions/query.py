import sqlparse
from pydantic import BaseModel, Field


class Query(BaseModel):
    code: str = Field(..., description="SQL query string to execute. Must match the SQL dialect of the database.")

    def is_read_only_query(self) -> bool:
        """Check if SQL contains only read operations"""
        parsed = sqlparse.parse(self.code)

        for statement in parsed:
            stmt_type = statement.get_type()
            if stmt_type not in ["SELECT", "WITH", "SHOW", "DESCRIBE", "EXPLAIN"]:
                return False

        return True
