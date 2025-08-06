# BigQuery

## Installation

```bash
pip install toolfront[bigquery]
```

## Basic Connection

```python
from toolfront import Database

db = Database("bigquery://project-id/dataset-id")
answer = db.ask("What's our total revenue this month?")
```

## Connection String Format

```
bigquery://project_id[/dataset_id][?param1=value1&...]
```

## Configuration Parameters

- `project_id`: GCP project ID (optional)
- `dataset_id`: BigQuery dataset ID
- `credentials`: Google auth credentials (optional)
- `application_name`: Application name for tracking (optional)
- `auth_local_webserver`: Use local webserver for authentication (default: True)
- `auth_external_data`: Request additional scopes for external data sources (default: False)
- `auth_cache`: Credentials cache behavior - 'default', 'reauth', or 'none' (default: 'default')
- `partition_column`: Custom partition column identifier (default: 'PARTITIONTIME')
- `client`: Custom google.cloud.bigquery Client instance (optional)
- `storage_client`: Custom BigQueryReadClient instance (optional)
- `location`: Default location for BigQuery objects (optional)
- `generate_job_id_prefix`: Callable to generate job ID prefixes (optional)

## Connection Examples

```python
from toolfront import Database

# Basic connection
db = Database("bigquery://my-analytics-project/web_analytics")

# With location specification
db = Database("bigquery://my-project/dataset?location=us-west1")

# With service account credentials
db = Database("bigquery://my-project/dataset", credentials="/path/to/service-account.json")
```