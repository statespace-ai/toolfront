# AWS Console Fallback Guide

For users who don't have AWS CLI configured or prefer clicking through the console.

## When to Use This Guide

- You don't have AWS CLI installed/configured
- The CLI commands are giving permission errors
- You prefer visual interfaces over terminal commands

## Step-by-Step Console Instructions

### 1. Find Your Infrastructure Information

#### Find Your VPC ID
1. Go to [EC2 Console](https://console.aws.amazon.com/ec2/)
2. Click **"VPC"** in the left sidebar  
3. Click **"Your VPCs"**
4. Look for the VPC where your existing EC2/RDS instances are
5. Copy the **VPC ID** (starts with `vpc-`)

#### Find Your Public Subnet ID  
1. In the VPC console, click **"Subnets"**
2. Filter by your VPC ID
3. Look for a subnet with **"Auto-assign public IPv4"** = **"Yes"**
4. Copy the **Subnet ID** (starts with `subnet-`)

#### Find Your RDS Instance Name
1. Go to [RDS Console](https://console.aws.amazon.com/rds/)
2. Click **"Databases"**
3. Find your database instance
4. Copy the **DB identifier** (NOT the endpoint - just the name)

#### Find Your Key Pair Name
1. Go to [EC2 Console](https://console.aws.amazon.com/ec2/)
2. Click **"Key Pairs"** in the left sidebar
3. Find the key pair you use to SSH to your EC2 instances
4. Copy the **Key pair name** (without .pem extension)

### 2. Deploy Using AWS CLI

Even if you don't have AWS CLI for general use, you can install it just for this deployment:

```bash
# Quick AWS CLI install (Mac)
brew install awscli

# Quick AWS CLI install (Linux)
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip && sudo ./aws/install

# Configure with your keys
aws configure
```

Then use the values you found in the console:
```bash
toolfront deploy aws \
  --database-url "postgresql://user:pass@your-rds-endpoint:5432/db" \
  --key-pair your-key-pair-name \
  --vpc-id vpc-xxxxxxxxx \
  --subnet-id subnet-xxxxxxxxx \
  --region us-east-1
```

### 3. Manual Database Access Rule (Console Only)

If your deployment succeeds but the health check fails, you need to add a database access rule manually.

#### Get Your ToolFront Security Group ID
1. Go to [CloudFormation Console](https://console.aws.amazon.com/cloudformation/)
2. Click your stack name (e.g., `my-toolfront-stack`)
3. Click the **"Outputs"** tab
4. Find **"SecurityGroupId"** and copy the value (starts with `sg-`)

#### Add Database Access Rule
1. Go to [RDS Console](https://console.aws.amazon.com/rds/)
2. Click your database instance
3. Scroll down to **"Connectivity & security"** section
4. Under **"VPC security groups"**, click the security group link
5. This opens the EC2 Security Groups page
6. Click **"Edit inbound rules"**
7. Click **"Add rule"**
8. Set:
   - **Type**: PostgreSQL (port 5432 auto-fills)
   - **Protocol**: TCP (auto-fills)
   - **Port range**: 5432 (auto-fills)
   - **Source**: Custom
   - **Source value**: Paste your ToolFront security group ID (sg-xxxxxxxx)
   - **Description**: "ToolFront access"
9. Click **"Save rules"**

#### Test the Fix
Wait 30-60 seconds, then test:
```bash
curl http://your-ec2-ip:8000/health
```

You should see: `{"status": "healthy", "database_connections": 1}`

### 4. Get Your ToolFront URL

1. Go to [CloudFormation Console](https://console.aws.amazon.com/cloudformation/)
2. Click your stack name
3. Click **"Outputs"** tab
4. Find **"ToolFrontURL"** - this is your HTTP API endpoint
5. Find **"HealthCheckURL"** - use this to test the service

## Alternative: Manual CloudFormation Deployment

If the ToolFront CLI doesn't work for any reason, you can deploy manually:

### 1. Download the Template
1. Go to [GitHub](https://raw.githubusercontent.com/kruskal-labs/toolfront/main/src/toolfront/templates/aws-cloudformation.yaml)
2. Right-click → "Save as" → Save as `toolfront-template.yaml`

### 2. Deploy via CloudFormation Console
1. Go to [CloudFormation Console](https://console.aws.amazon.com/cloudformation/)
2. Click **"Create stack"** → **"With new resources"**
3. Choose **"Upload a template file"**
4. Upload your `toolfront-template.yaml` file
5. Click **"Next"**

### 3. Fill in Parameters
- **Stack name**: `my-toolfront-stack`
- **DatabaseURL**: 
  ```bash
  # First encode your URL:
  echo "postgresql://user:pass@host:5432/db" | base64
  # Then paste the base64 result
  ```
- **KeyPairName**: Your key pair name (from Step 1)
- **VpcId**: Your VPC ID (from Step 1)  
- **SubnetId**: Your subnet ID (from Step 1)

### 4. Continue Deployment
1. Click **"Next"** (skip Configure stack options)
2. Click **"Next"** (skip Review)
3. Check **"I acknowledge that AWS CloudFormation might create IAM resources"**
4. Click **"Create stack"**
5. Wait 5-10 minutes for **"CREATE_COMPLETE"**

### 5. Get Outputs and Test
1. Click **"Outputs"** tab
2. Copy the **"ToolFrontURL"** 
3. Test: `curl http://your-url:8000/health`
4. If health check fails, follow the database access rule steps above

## Troubleshooting Console Issues

### Can't Find VPC/Subnet
- Make sure you're in the correct AWS region (top-right corner)
- Your RDS and EC2 instances should be in the same VPC
- Look for VPCs with friendly names or tags

### Security Group Rule Won't Save
- Check you're using the correct security group ID format (sg-xxxxxxxx)
- Make sure you're not trying to add a duplicate rule
- Verify you have EC2 permissions in your AWS account

### CloudFormation Stack Fails
- Check the **"Events"** tab for error details
- Common issues: wrong key pair name, wrong AMI ID, permission errors
- Delete the failed stack and try again with corrected parameters

### Database Connection Still Fails
- Verify your database URL is correct by testing with `psql`
- Check your RDS instance is in "Available" status
- Make sure your RDS is in the same VPC as your ToolFront deployment
- Verify the database password doesn't contain special characters (URL encode if needed)

## Getting Help

If you're stuck:
1. Check the [main troubleshooting guide](troubleshooting.md)
2. Gather your error messages and settings
3. Ask for help on [Discord](https://discord.gg/rRyM7zkZTf) or [GitHub Issues](https://github.com/kruskal-labs/toolfront/issues)
