# Manual Database Access Rule Setup

If the `toolfront deploy aws` command completes but your ToolFront service can't connect to RDS, you need to manually add a database access rule.

## Step 1: Get Your Stack's Security Group ID

```bash
# Replace 'your-stack-name' with your actual CloudFormation stack name
aws cloudformation describe-stacks \
  --stack-name your-stack-name \
  --region your-region \
  --query 'Stacks[0].Outputs[?OutputKey==`SecurityGroupId`].OutputValue' \
  --output text
```

Example output: `sg-075cad0ea26f04185`

## Step 2: Get Your RDS Security Group ID

```bash
# Replace 'your-rds-identifier' with your actual RDS instance name
aws rds describe-db-instances \
  --db-instance-identifier your-rds-identifier \
  --region your-region \
  --query 'DBInstances[0].VpcSecurityGroups[0].VpcSecurityGroupId' \
  --output text
```

Example output: `sg-09456bcc218cff44d`

## Step 3: Add the Access Rule

```bash
# Replace the security group IDs and region with your actual values
aws ec2 authorize-security-group-ingress \
  --group-id sg-09456bcc218cff44d \
  --protocol tcp \
  --port 5432 \
  --source-group sg-075cad0ea26f04185 \
  --region your-region
```

## Step 4: Verify Access

Wait 30-60 seconds, then test the health endpoint:

```bash
# Replace with your actual ToolFront URL from CloudFormation outputs
curl http://your-ec2-ip:8000/health
```

You should see a JSON response indicating the service is healthy.

## Complete Example

```bash
# Example for stack 'my-toolfront' and RDS 'my-database' in us-east-1:

# Get ToolFront security group
TOOLFRONT_SG=$(aws cloudformation describe-stacks \
  --stack-name my-toolfront \
  --region us-east-1 \
  --query 'Stacks[0].Outputs[?OutputKey==`SecurityGroupId`].OutputValue' \
  --output text)

# Get RDS security group  
RDS_SG=$(aws rds describe-db-instances \
  --db-instance-identifier my-database \
  --region us-east-1 \
  --query 'DBInstances[0].VpcSecurityGroups[0].VpcSecurityGroupId' \
  --output text)

# Add access rule
aws ec2 authorize-security-group-ingress \
  --group-id $RDS_SG \
  --protocol tcp \
  --port 5432 \
  --source-group $TOOLFRONT_SG \
  --region us-east-1

# Test health
curl http://$(aws cloudformation describe-stacks \
  --stack-name my-toolfront \
  --region us-east-1 \
  --query 'Stacks[0].Outputs[?OutputKey==`ToolFrontURL`].OutputValue' \
  --output text)/health
```

## Why This is Needed

The ToolFront CLI automatically tries to add this rule, but it may fail if:
- The RDS security group already has many rules
- There are permission issues
- The rule already exists but in a different format

This manual step ensures your ToolFront service can connect to your database.
