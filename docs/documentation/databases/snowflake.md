# Snowflake

## Installation

```bash
pip install "toolfront[snowflake]"
```

## Connection URL

```
snowflake://{user}:{password}@{account}/{database}
```

## Connection Parameters

| Name                     | Type                                        | Description                                                                                                                                                                                                                                                                                                                                 | Default           |
|--------------------------|---------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------|
| `user`                   | `str`                                       | Username                                                                                                                                                                                                                                                                                                                                    | **required**      |
| `account`                | `str`                                       | A Snowflake organization ID and a Snowflake user ID, separated by a hyphen. Note that a Snowflake user ID is a separate identifier from a username. See https://docs.snowflake.com/en/user-guide/admin-account-identifier for details                                                                                                   | **required**      |
| `database`               | `str`                                       | A Snowflake database and a Snowflake schema, separated by a /. See https://docs.snowflake.com/en/sql-reference/ddl-database for details                                                                                                                                                                                                  | **required**      |
| `password`               | `str`                                       | Password. If empty or None then authenticator must be passed.                                                                                                                                                                                                                                                                              | **required**      |
| `authenticator`          | `str`                                       | String indicating authentication method. See https://docs.snowflake.com/en/developer-guide/python-connector/python-connector-example#connecting-with-oauth for details. Note that the authentication flow will not take place until a database connection is made. This means that connection can succeed, while subsequent API calls fail if the authentication fails for any reason. | **required**      |
| `create_object_udfs`     | `bool`                                      | Enable object UDF extensions defined on the first connection to the database.                                                                                                                                                                                                                                                              | `True`            |
| `kwargs`                 | `Any`                                       | Additional arguments passed to the DBAPI connection call.                                                                                                                                                                                                                                                                                  | `{}`              |

## Examples

**Using Connection URL:**
```python
from toolfront import Database

db = Database("snowflake://user:pass@account-id/sales")
revenue = db.ask("What's our total revenue this month?")
```

**Using Connection Parameters:**
```python
from toolfront import Database

db = Database(
    url="snowflake://", # REQUIRED (1)
    account="account-id",
    database="sales",
    user="user",
    password="pass",
    authenticator="snowflake"
)
revenue = db.ask("What's our total revenue this month?")
```

1. You must always pass `snowflake` or `snowflake://` as the URL when creating a Snowflake `Database` from parameters. This is required for proper backend selection.