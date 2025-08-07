# BigQuery

## Installation

```bash
pip install "toolfront[bigquery]"
```

## Connection URL

```
bigquery://{project_id}/{dataset_id}
```

## Connection Parameters

| Name                     | Type                                        | Description                                                                                                                                                                                                                                                                                                                                 | Default           |
|--------------------------|---------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------|
| `project_id`             | `str | None`                                | A BigQuery project id.                                                                                                                                                                                                                                                                                                                     | `None`            |
| `dataset_id`             | `str`                                       | A dataset id that lives inside of the project indicated by project_id.                                                                                                                                                                                                                                                                     | `''`              |
| `credentials`            | `google.auth.credentials.Credentials | None` | Optional credentials.                                                                                                                                                                                                                                                                                                                       | `None`            |
| `application_name`       | `str | None`                                | A string identifying your application to Google API endpoints.                                                                                                                                                                                                                                                                             | `None`            |
| `auth_local_webserver`   | `bool`                                      | Use a local webserver for the user authentication. Binds a webserver to an open port on localhost between 8080 and 8089, inclusive, to receive authentication token. If not set, defaults to False, which requests a token via the console.                                                                                             | `True`            |
| `auth_external_data`     | `bool`                                      | Authenticate using additional scopes required to query external data sources, such as Google Sheets, files in Google Cloud Storage, or files in Google Drive. If not set, defaults to False, which requests the default BigQuery scopes.                                                                                               | `False`           |
| `auth_cache`             | `str`                                       | Selects the behavior of the credentials cache. `'default'` - Reads credentials from disk if available, otherwise authenticates and caches credentials to disk. `'reauth'` - Authenticates and caches credentials to disk. `'none'` - Authenticates and does not cache credentials. Defaults to 'default'.                           | `'default'`       |
| `partition_column`       | `str | None`                                | Identifier to use instead of default _PARTITIONTIME partition column. Defaults to 'PARTITIONTIME'.                                                                                                                                                                                                                                       | `'PARTITIONTIME'` |
| `client`                 | `bq.Client | None`                          | A Client from the google.cloud.bigquery package. If not set, one is created using the project_id and credentials.                                                                                                                                                                                                                        | `None`            |
| `storage_client`         | `bqstorage.BigQueryReadClient | None`       | A BigQueryReadClient from the google.cloud.bigquery_storage_v1 package. If not set, one is created using the project_id and credentials.                                                                                                                                                                                                | `None`            |
| `location`               | `str | None`                                | Default location for BigQuery objects.                                                                                                                                                                                                                                                                                                     | `None`            |
| `generate_job_id_prefix` | `Callable[[], str | None] | None`           | Optional callable that generates a bigquery job ID prefix. If specified, for any query job, jobs will always be created rather than optionally created by BigQuery's Client.query_and_wait.                                                                                                                                              | `None`            |

## Examples

**Using Connection URL:**
```python
from toolfront import Database

db = Database(url="bigquery://my-project/sales")
revenue = db.ask("What's our total revenue this month?")
```

**Using Connection Parameters:**
```python
from toolfront import Database

db = Database(
    url="bigquery://" # REQUIRED (1)
    project_id="my-project",
    dataset_id="sales",
    credentials="/path/to/service-account.json",
    location="us-west1"
)
revenue = db.ask("What's our total revenue this month?")
```

1. You must always pass `bigquery` or `bigquery://` as the URL when creating a BigQuery `Database` from parameters. This is required for proper backend selection.