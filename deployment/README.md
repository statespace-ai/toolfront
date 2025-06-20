# ToolFront AWS Deployment Guide

**For AWS beginners who want to get their databases accessible to AI agents ASAP.**

## What You'll Get

After following this guide:
- ✅ Your database accessible to AI agents from anywhere
- ✅ A secure HTTP API running on AWS
- ✅ Automatic security group configuration
- ⏱️ Total time: ~15-20 minutes

## Who This Is For

You probably:
- 🐣 Created an RDS database by clicking around the AWS console
- 🔑 Have an EC2 "bastion" instance you SSH into to access your database  
- 🔒 Connect to your database with `psql` and manually type passwords
- 📊 Want AI agents to query your database without exposing it to the internet

**This guide assumes you're comfortable with copy-pasting terminal commands but not an AWS expert.**

## Before You Start

### ✅ Check Your AWS Setup

1. **Can you SSH into your EC2 instance?**
   ```bash
   ssh -i ~/.ssh/your-key.pem ec2-user@your-ec2-ip
   ```

2. **Can you connect to your database from that EC2 instance?**
   ```bash
   psql -h your-rds-endpoint.us-east-1.rds.amazonaws.com -U postgres -d your_database
   ```

3. **Do you know your database connection details?**
   - Hostname: `your-rds.us-east-1.rds.amazonaws.com`
   - Username: probably `postgres` or `admin`
   - Password: the one you set when creating RDS
   - Database name: the database you want AI agents to access

If any of these fail, **stop here** and fix your existing setup first.

---

## Step 1: Get Your AWS Information

We need to find your VPC and subnet IDs. Don't worry - we'll walk through it.

### Option A: Use the AWS CLI (Recommended)

**Install AWS CLI** (if you don't have it):
```bash
# On Mac
brew install awscli

# On Linux  
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

**Configure AWS CLI**:
```bash
aws configure
# Enter your Access Key ID (from IAM console)
# Enter your Secret Access Key (from IAM console)  
# Enter your region (e.g., us-east-1)
# Press Enter for output format
```

**Find your infrastructure**:
```bash
# Find your VPC (look for one with a friendly name)
aws ec2 describe-vpcs --query 'Vpcs[].[VpcId,Tags[?Key==`Name`].Value|[0],CidrBlock]' --output table

# Find your public subnet (in that VPC)
aws ec2 describe-subnets \
  --filters "Name=vpc-id,Values=vpc-YOUR-VPC-ID" "Name=map-public-ip-on-launch,Values=true" \
  --query 'Subnets[].[SubnetId,AvailabilityZone,CidrBlock]' --output table

# Find your RDS instance name
aws rds describe-db-instances --query 'DBInstances[].[DBInstanceIdentifier,Engine,DBInstanceStatus]' --output table
```

**Write down:**
- VPC ID: `vpc-xxxxxxxxx`  
- Subnet ID: `subnet-xxxxxxxxx`
- RDS Identifier: `your-rds-name`
- Your EC2 key pair name: probably the name of your `.pem` file without `.pem`

### Option B: Use the AWS Console (If CLI doesn't work)

1. **Find your VPC**:
   - Go to [EC2 Console](https://console.aws.amazon.com/ec2/) → VPC → Your VPCs
   - Look for the VPC your EC2 instance is in
   - Copy the VPC ID (vpc-xxxxxxxxx)

2. **Find your public subnet**:
   - Go to VPC → Subnets 
   - Filter by your VPC ID
   - Look for a subnet with "Auto-assign public IPv4" = Yes
   - Copy the Subnet ID (subnet-xxxxxxxxx)

3. **Find your RDS name**:
   - Go to [RDS Console](https://console.aws.amazon.com/rds/)
   - Look at your database instances
   - Copy the "DB identifier" (not the endpoint!)

4. **Find your key pair name**:
   - Go to EC2 → Key Pairs
   - Look for the key pair you use to SSH to your EC2 instance

---

## Step 2: Install and Deploy ToolFront

**Install ToolFront**:
```bash
# Install using pipx (recommended)
pipx install toolfront

# Or using pip
pip install toolfront
```

**Build your database URL**:
```bash
# Replace these with your actual values:
# - username: probably 'postgres' or 'admin'  
# - password: what you type when connecting via psql
# - hostname: your RDS endpoint (without :5432)
# - database: your database name

DATABASE_URL="postgresql://username:password@your-rds-endpoint:5432/database_name"
```

**Deploy to AWS**:
```bash
toolfront deploy aws \
  --database-url "$DATABASE_URL" \
  --key-pair your-key-pair-name \
  --vpc-id vpc-xxxxxxxxx \
  --subnet-id subnet-xxxxxxxxx \
  --region us-east-1 \
  --stack-name my-toolfront-stack
```

**OR use auto-detection** (if you have RDS identifier):
```bash
toolfront deploy aws \
  --database-url "$DATABASE_URL" \
  --key-pair your-key-pair-name \
  --rds-identifier your-rds-name \
  --region us-east-1 \
  --stack-name my-toolfront-stack
```

**What happens:**
- Creates a new EC2 instance in your VPC
- Sets up security groups for database access
- Deploys ToolFront HTTP server
- Should take 3-5 minutes

---

## Step 3: Test Your Deployment

**Get your ToolFront URL**:
The deploy command will output something like:
```
📡 ToolFront URL: http://54.123.45.67:8000
🔍 Health Check: http://54.123.45.67:8000/health
```

**Test the health endpoint**:
```bash
curl http://54.123.45.67:8000/health
```

**Expected responses:**

✅ **Success** (you should see JSON):
```json
{"status": "healthy", "database_connections": 1}
```

❌ **Connection refused** (service starting):
```
curl: (7) Failed to connect... Connection refused
```
→ Wait 2-3 minutes and try again

❌ **Timeout** (networking issue):
```
curl: (28) Operation timed out
```
→ Check security groups in AWS console

❌ **Database connection failed**:
```json
{"status": "unhealthy", "error": "database connection failed"}
```
→ Need to add database access rule (see Step 4)

---

## Step 4: Fix Database Access (If Needed)

If the health check shows database connection failed, you need to manually allow your ToolFront instance to connect to RDS.

### Quick Fix (AWS CLI)

```bash
# Get your ToolFront security group ID
TOOLFRONT_SG=$(aws cloudformation describe-stacks \
  --stack-name my-toolfront-stack \
  --query 'Stacks[0].Outputs[?OutputKey==`SecurityGroupId`].OutputValue' \
  --output text)

# Get your RDS security group ID  
RDS_SG=$(aws rds describe-db-instances \
  --db-instance-identifier your-rds-name \
  --query 'DBInstances[0].VpcSecurityGroups[0].VpcSecurityGroupId' \
  --output text)

# Add the access rule
aws ec2 authorize-security-group-ingress \
  --group-id $RDS_SG \
  --protocol tcp \
  --port 5432 \
  --source-group $TOOLFRONT_SG
```

### Manual Fix (AWS Console)

1. **Get your ToolFront security group ID**:
   - Go to [CloudFormation Console](https://console.aws.amazon.com/cloudformation/)
   - Click your stack name (`my-toolfront-stack`)
   - Go to "Outputs" tab
   - Copy the "SecurityGroupId" value (sg-xxxxxxxxx)

2. **Find your RDS security group**:
   - Go to [RDS Console](https://console.aws.amazon.com/rds/)
   - Click your database instance
   - Scroll down to "Connectivity & security"
   - Click the security group link under "VPC security groups"

3. **Add the access rule**:
   - In the security group, click "Edit inbound rules"
   - Click "Add rule"
   - Type: PostgreSQL (port 5432 will auto-fill)
   - Source: Custom → Paste your ToolFront security group ID
   - Click "Save rules"

**Test again:**
```bash
curl http://54.123.45.67:8000/health
```

You should now see: `{"status": "healthy", "database_connections": 1}`

---

## Step 5: Connect AI Agents

Now that ToolFront is running, you can connect it to AI agents:

**For Claude Desktop**:
```json
{
  "mcpServers": {
    "toolfront": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "http://54.123.45.67:8000", "--allow-http"]
    }
  }
}
```

**For Cursor/VSCode**:
```json
{
  "mcpServers": {
    "toolfront": {
      "command": "curl",
      "args": [
        "-H", "Content-Type: application/json",
        "-X", "POST",
        "http://54.123.45.67:8000"
      ]
    }
  }
}
```

---

## Cleanup (When You're Done Testing)

```bash
# Delete the CloudFormation stack
aws cloudformation delete-stack --stack-name my-toolfront-stack

# Verify deletion
aws cloudformation describe-stacks --stack-name my-toolfront-stack
```

---

## Troubleshooting

### "CLI hangs after credential loading"
You're probably in `us-west-2`. Try:
- Use `--region us-east-1` instead
- Or see [us-west-2 workaround](../US_WEST_2_WORKAROUND.md)

### "Key pair not found"  
- Make sure the key pair name matches exactly (without .pem extension)
- Key pairs are region-specific - create one in your target region

### "Health check always fails"
- Check security groups in AWS console
- Make sure your RDS allows connections from the ToolFront security group
- Try the manual database access fix above

### "Database URL format issues"
Your URL should look like:
```
postgresql://username:password@hostname:5432/database_name
```

Common issues:
- **Special characters in password**: URL-encode them
- **Wrong port**: RDS PostgreSQL uses 5432, MySQL uses 3306
- **Wrong hostname**: Use the RDS endpoint, not the IP address

---

## Next Steps

- **Monitor costs**: A t3.micro instance costs ~$8-10/month
- **Set up monitoring**: Use the health check URL for uptime monitoring  
- **Scale up**: Change instance type in CloudFormation if needed
- **Add HTTPS**: Set up a load balancer for production use

**Questions?** Check the [troubleshooting guide](troubleshooting.md) or open an issue.
