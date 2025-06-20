# How to Integrate Deploy Command into README

## Add this section after the "Run ToolFront in your IDE" section:

### Deploy to the Cloud

Want to make your databases accessible to AI agents from anywhere? Deploy ToolFront to AWS:

```bash
# Install ToolFront
pipx install toolfront

# Deploy to AWS  
toolfront deploy aws \
  --database-url "postgresql://user:pass@host:5432/db" \
  --key-pair my-ec2-key \
  --vpc-id vpc-12345678 \
  --subnet-id subnet-87654321
```

**📖 [Complete Deployment Guide →](DEPLOYMENT.md)**

**⚠️ Having issues?**
- **CLI hanging?** See [us-west-2 workaround →](US_WEST_2_WORKAROUND.md)  
- **Database connection failed?** See [manual setup steps →](MANUAL_DATABASE_STEPS.md)

---

## Modify the existing "Prerequisites" section to include:

### Prerequisites

- **[uv](https://docs.astral.sh/uv/)** or **[Docker](https://www.docker.com/)** to run the MCP server (we recommend **uv**)
- **Database connection URLs** of your databases - [see below](#databases)
- **API key** (optional) to activate collaborative learning - [see below](#collaborative-in-context-learning)
- **AWS account** (optional) for cloud deployment - [see deployment guide](DEPLOYMENT.md)

## Add to the table of contents or quick links section:

## Documentation

| Topic | Link | Description |
|-------|------|-------------|
| **🚀 Deploy to AWS** | [Deployment Guide](DEPLOYMENT.md) | Host ToolFront in the cloud |
| **🔧 Database Setup** | [Database Connections](#databases) | Connect to your databases |
| **⚙️ IDE Integration** | [MCP Setup](#run-toolfront-in-your-ide) | Add to Cursor, Copilot, etc. |
| **🆘 Troubleshooting** | [Common Issues](TROUBLESHOOTING.md) | Fix deployment problems |

## Key principles:

1. **Prominent placement** - Right after local setup, before diving into details
2. **Clear action items** - Show the command, link to details  
3. **Troubleshooting links** - Address the two main failure modes immediately
4. **Progressive disclosure** - Quick example → detailed guide → troubleshooting
