# us-west-2 CLI Hang Workaround

## Problem
The `toolfront deploy aws` command hangs indefinitely in us-west-2 due to region-specific DNS/network resolution issues during boto3 client initialization.

## Symptoms
- Command gets stuck after `INFO:botocore.credentials:Found credentials...`
- No error message, just infinite hang
- Works fine in us-east-1 and us-west-1

## Workarounds

### Option 1: Manual CloudFormation (Recommended)
Deploy using AWS CLI directly instead of the ToolFront CLI:

```bash
# Download the CloudFormation template
curl -o toolfront-template.yaml https://raw.githubusercontent.com/kruskal-labs/toolfront/main/src/toolfront/templates/aws-cloudformation.yaml

# Deploy manually
aws cloudformation create-stack \
  --stack-name toolfront-$(date +%s) \
  --template-body file://toolfront-template.yaml \
  --parameters \
    ParameterKey=DatabaseURL,ParameterValue=$(echo "your-database-url" | base64) \
    ParameterKey=KeyPairName,ParameterValue=your-key-pair \
    ParameterKey=VpcId,ParameterValue=your-vpc-id \
    ParameterKey=SubnetId,ParameterValue=your-subnet-id \
  --region us-west-2

# Wait for completion
aws cloudformation wait stack-create-complete \
  --stack-name toolfront-$(date +%s) \
  --region us-west-2
```

### Option 2: Use Different Region
If possible, deploy in us-east-1 or us-west-1 where the CLI works:

```bash
# Works fine:
toolfront deploy aws \
  --database-url "your-db-url" \
  --key-pair your-key \
  --vpc-id your-vpc \
  --subnet-id your-subnet \
  --region us-east-1
```

### Option 3: Cross-Region Setup
Deploy ToolFront in us-east-1 but connect to us-west-2 RDS:

```bash
# Deploy in us-east-1, connect to us-west-2 RDS
toolfront deploy aws \
  --database-url "postgresql://user:pass@your-rds.us-west-2.rds.amazonaws.com:5432/db" \
  --key-pair your-east-1-key \
  --vpc-id your-east-1-vpc \
  --subnet-id your-east-1-subnet \
  --region us-east-1
```

**Note**: Cross-region database connections have higher latency and data transfer costs.

## Status
We're investigating the root cause of the us-west-2 DNS/network issue. Until resolved, we recommend:
1. Use manual CloudFormation for us-west-2
2. Use us-east-1 or us-west-1 for CLI deployments
3. Contact support if you must use the CLI in us-west-2
