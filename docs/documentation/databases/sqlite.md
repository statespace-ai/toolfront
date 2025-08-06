# SQLite

Configure ToolFront to connect to SQLite databases.

## Installation

```bash
pip install toolfront[sqlite]
```

## Connection

### File Database
```python
from toolfront import Database

# Connect to SQLite file
db = Database("sqlite:///path/to/database.db")

# Query local database
user_count: int = db.ask("How many users are registered?")
print(f"Registered Users: {user_count:,}")
```

### In-Memory Database
```python
# Temporary in-memory database
db = Database("sqlite://")

# Perfect for testing and temporary analysis
test_results = db.ask("Analyze test data loaded into memory")
```

## Connection Formats

```python
# Absolute path
db = Database("sqlite:////absolute/path/to/database.db")

# Relative path  
db = Database("sqlite:///./relative/path/database.db")

# Current directory
db = Database("sqlite:///database.db")

# In-memory
db = Database("sqlite://")
```

## Real-World Examples

### Local Application Data
```python
# Desktop application database
db = Database("sqlite:///~/Documents/MyApp/app_data.db")

settings: dict = db.ask("Show current application settings and preferences")
usage_stats = db.ask("Calculate application usage statistics")
```

### Embedded Analytics
```python
# IoT or embedded device data
db = Database("sqlite:///data/sensor_readings.db")

sensor_analysis = db.ask("Analyze sensor data trends and anomalies")
device_health = db.ask("Check device performance metrics")
```

### Development and Testing
```python
# Development database
db = Database("sqlite:///dev_database.db")

test_coverage = db.ask("Analyze test data coverage and completeness")
mock_data_stats = db.ask("Generate statistics from mock test data")
```

## Advantages

- **Zero-configuration** - No server setup required
- **Self-contained** - Single file database
- **Cross-platform** - Works everywhere
- **ACID compliant** - Reliable transactions
- **Small footprint** - Minimal resource usage

## Best Use Cases

```python
# Local data analysis
local_analysis = db.ask("Analyze data without external dependencies")

# Prototyping and development
prototype_metrics = db.ask("Generate metrics for prototype validation")

# Edge computing
edge_insights = db.ask("Process data at the edge with minimal resources")
```