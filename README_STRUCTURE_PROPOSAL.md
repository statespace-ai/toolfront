# README Documentation Structure

## Main README.md (Keep Simple)

```markdown
# ToolFront

Database access for AI agents via MCP protocol.

## Quick Start

### Local Usage
```bash
# Install
pipx install toolfront

# Run MCP server
toolfront "postgresql://user:pass@host:5432/db"
```

### AWS Deployment
```bash
# Deploy to AWS
toolfront deploy aws \
  --database-url "postgresql://..." \
  --key-pair my-key \
  --vpc-id vpc-12345 \
  --subnet-id subnet-67890
```

See [Deployment Guide](docs/DEPLOYMENT.md) for detailed instructions.

## Documentation

- **[Deployment Guide](docs/DEPLOYMENT.md)** - Deploy ToolFront to AWS
- **[MCP Configuration](docs/MCP_SETUP.md)** - Connect to Claude Desktop
- **[Database Setup](docs/DATABASE.md)** - Database connection guides
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** - Common issues and solutions

[rest of existing README content...]
```

## Documentation Structure

```
docs/
├── DEPLOYMENT.md           # Main deployment guide
├── DEPLOYMENT_AWS.md       # AWS-specific details  
├── DEPLOYMENT_REGIONAL.md  # Regional considerations
├── MCP_SETUP.md           # Claude Desktop setup
├── DATABASE.md            # Database connection guides
├── TROUBLESHOOTING.md     # Troubleshooting guide
└── MANUAL_STEPS.md        # Manual fallback procedures
```
