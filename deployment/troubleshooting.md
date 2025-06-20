# Deployment Troubleshooting

Common issues when deploying ToolFront to AWS, with step-by-step fixes.

## CLI Issues

### us-west-2 CLI Hang

**Symptoms:**
- Command freezes after `INFO:botocore.credentials:Found credentials...`
- No error message, just infinite hang
- Works fine in other regions

**Quick Fix:**
```bash
# Use a different region
toolfront deploy aws \
  --database-url "your-url" \
  --key-pair your-key \
  --vpc-id vpc-xxx \
  --subnet-id subnet-xxx \
  --region us-east-1  # ← Change to us-east-1
```

**Alternative - Manual CloudFormation:**
```bash
# Download template
curl -o toolfront.yaml https://raw.githubusercontent.com/kruskal-labs/toolfront/main/src/toolfront/templates/aws-cloudformation.yaml

# Deploy manually  
aws cloudformation create-stack \
  --stack-name toolfront-manual \
  --template-body file://toolfront.yaml \
  --parameters \
    ParameterKey=DatabaseURL,ParameterValue=$(echo "your-database-url" | base64) \
    ParameterKey=KeyPairName,ParameterValue=your-key \
    ParameterKey=VpcId,ParameterValue=vpc-xxx \
    ParameterKey=SubnetId,ParameterValue=subnet-xxx \
  --region us-west-2
```

### Key Pair Not Found

**Symptoms:**
```
❌ Key pair 'my-key' not found
```

**Fixes:**

1. **Check key pair exists in correct region:**
   ```bash
   aws ec2 describe-key-pairs --region us-east-1
   ```

2. **Create key pair if missing:**
   ```bash
   aws ec2 create-key-pair \
     --key-name toolfront-key \
     --region us-east-1 \
     --query 'KeyMaterial' \
     --output text > ~/.ssh/toolfront-key.pem
   
   chmod 400 ~/.ssh/toolfront-key.pem
   ```

3. **Use correct key name (without .pem):**
   ```bash
   # Wrong
   --key-pair my-key.pem
   
   # Correct  
   --key-pair my-key
   ```

### VPC/Subnet Not Found

**Symptoms:**
```
❌ VPC 'vpc-xxx' not found
❌ Subnet 'subnet-xxx' not found
```

**Fixes:**

1. **Verify IDs in correct region:**
   ```bash
   # Check VPCs
   aws ec2 describe-vpcs --region us-east-1
   
   # Check subnets
   aws ec2 describe-subnets --region us-east-1
   ```

2. **Use RDS auto-detection instead:**
   ```bash
   toolfront deploy aws \
     --database-url "your-url" \
     --key-pair your-key \
     --rds-identifier your-rds-name \
     --region us-east-1
   ```

## Database Connection Issues

### Health Check Shows Database Error

**Symptoms:**
```json
{"status": "unhealthy", "error": "database connection failed"}
```

**Step-by-step fix:**

1. **Get security group IDs:**
   ```bash
   # ToolFront security group (from CloudFormation outputs)
   aws cloudformation describe-stacks \
     --stack-name your-stack-name \
     --query 'Stacks[0].Outputs[?OutputKey==`SecurityGroupId`].OutputValue' \
     --output text
   
   # RDS security group
   aws rds describe-db-instances \
     --db-instance-identifier your-rds-name \
     --query 'DBInstances[0].VpcSecurityGroups[0].VpcSecurityGroupId' \
     --output text
   ```

2. **Add database access rule:**
   ```bash
   aws ec2 authorize-security-group-ingress \
     --group-id sg-rds-security-group \
     --protocol tcp \
     --port 5432 \
     --source-group sg-toolfront-security-group
   ```

3. **Verify the rule was added:**
   ```bash
   aws ec2 describe-security-groups --group-ids sg-rds-security-group
   ```

4. **Test again:**
   ```bash
   curl http://your-ec2-ip:8000/health
   ```

### Database URL Format Issues

**Symptoms:**
- Connection timeouts
- Authentication failures  
- "database does not exist" errors

**Common URL problems:**

1. **Special characters in password:**
   ```bash
   # Wrong (unescaped special chars)
   postgresql://user:p@ssw0rd!@host:5432/db
   
   # Correct (URL encoded)
   postgresql://user:p%40ssw0rd%21@host:5432/db
   ```

2. **Wrong hostname format:**
   ```bash
   # Wrong (includes protocol)
   postgresql://user:pass@https://mydb.rds.amazonaws.com:5432/db
   
   # Correct
   postgresql://user:pass@mydb.rds.amazonaws.com:5432/db
   ```

3. **Wrong port:**
   ```bash
   # PostgreSQL uses 5432
   postgresql://user:pass@host:5432/db
   
   # MySQL uses 3306
   mysql://user:pass@host:3306/db
   ```

**Test your database URL:**
```bash
# Install psql if needed
sudo apt-get install postgresql-client  # Ubuntu/Debian
brew install postgresql                  # Mac

# Test connection
psql "postgresql://user:pass@host:5432/db" -c "SELECT 1;"
```

### RDS Not Found

**Symptoms:**
```
❌ Failed to detect VPC from RDS: DBInstanceIdentifier not found
```

**Fixes:**

1. **Check RDS instance exists:**
   ```bash
   aws rds describe-db-instances --region us-east-1
   ```

2. **Use exact RDS identifier:**
   ```bash
   # Check exact name in RDS console or:
   aws rds describe-db-instances \
     --query 'DBInstances[].DBInstanceIdentifier' \
     --output text
   ```

3. **Switch to manual VPC/subnet:**
   ```bash
   toolfront deploy aws \
     --database-url "your-url" \
     --key-pair your-key \
     --vpc-id vpc-xxx \
     --subnet-id subnet-xxx \
     --region us-east-1
   ```

## Post-Deployment Issues

### Health Check Timeout

**Symptoms:**
```bash
curl: (28) Operation timed out after 30000 milliseconds
```

**Fixes:**

1. **Check security groups allow HTTP traffic:**
   ```bash
   # Should show port 8000 open to 0.0.0.0/0
   aws ec2 describe-security-groups \
     --group-ids sg-your-toolfront-sg \
     --query 'SecurityGroups[0].IpPermissions'
   ```

2. **Check instance is running:**
   ```bash
   aws ec2 describe-instances \
     --filters "Name=tag:aws:cloudformation:stack-name,Values=your-stack-name" \
     --query 'Reservations[].Instances[].[InstanceId,State.Name,PublicIpAddress]'
   ```

3. **Check CloudFormation events for errors:**
   ```bash
   aws cloudformation describe-stack-events \
     --stack-name your-stack-name \
     --query 'StackEvents[?ResourceStatus==`CREATE_FAILED`]'
   ```

### Service Not Starting

**Symptoms:**
- Health check returns connection refused
- Service seems to never start

**Debug steps:**

1. **SSH into the instance:**
   ```bash
   # Get instance IP from CloudFormation outputs
   aws cloudformation describe-stacks \
     --stack-name your-stack-name \
     --query 'Stacks[0].Outputs[?OutputKey==`SSHCommand`].OutputValue'
   
   # SSH in
   ssh -i ~/.ssh/your-key.pem ec2-user@your-instance-ip
   ```

2. **Check service logs:**
   ```bash
   # On the instance
   sudo journalctl -u toolfront -f
   
   # Or check system logs
   sudo tail -f /var/log/cloud-init-output.log
   ```

3. **Check if service is running:**
   ```bash
   # On the instance
   sudo systemctl status toolfront
   ps aux | grep toolfront
   netstat -tlnp | grep 8000
   ```

4. **Restart service manually:**
   ```bash
   # On the instance
   sudo systemctl restart toolfront
   ```

## AWS Permission Issues

### Access Denied Errors

**Symptoms:**
```
An error occurred (UnauthorizedOperation) when calling the DescribeVpcs operation
```

**Fixes:**

1. **Check AWS credentials:**
   ```bash
   aws sts get-caller-identity
   ```

2. **Verify IAM permissions:**
   Your user/role needs:
   - `ec2:*` (for VPC, security groups, instances)
   - `cloudformation:*` (for stack operations)
   - `rds:DescribeDBInstances` (for RDS auto-detection)

3. **Try with admin user temporarily:**
   - Create a temporary IAM user with AdministratorAccess
   - Use for deployment, then remove

## Cost and Cleanup Issues

### Unexpected Costs

**What gets created:**
- 1x t3.micro EC2 instance (~$8.50/month)
- Security groups (free)
- CloudFormation stack (free)
- Data transfer (varies)

**Monitor costs:**
- Go to AWS Billing Console
- Set up billing alerts
- Check EC2 instance is t3.micro (not larger)

### Cleanup Not Working

**Delete CloudFormation stack:**
```bash
aws cloudformation delete-stack --stack-name your-stack-name
```

**If delete fails:**
```bash
# Check what's preventing deletion
aws cloudformation describe-stack-events \
  --stack-name your-stack-name \
  --query 'StackEvents[?ResourceStatus==`DELETE_FAILED`]'

# Force delete security groups if needed
aws ec2 delete-security-group --group-id sg-xxx
```

## Getting More Help

### Enable Debug Mode

Add `--debug` to any command:
```bash
toolfront deploy aws --debug [other options]
```

### Check Logs

**CloudFormation logs:**
- Go to CloudFormation Console
- Click your stack → Events tab
- Look for FAILED events

**EC2 instance logs:**
```bash
# SSH to instance, then:
sudo tail -f /var/log/cloud-init-output.log
sudo journalctl -u toolfront -f
```

### Contact Support

If none of these fixes work:
1. **Gather info:**
   - AWS region
   - ToolFront version: `toolfront --version`
   - Error messages (exact text)
   - CloudFormation stack events

2. **Open GitHub issue:**
   - Include debug output
   - Mention you followed this troubleshooting guide

3. **Discord/Community:**
   - Quick questions on Discord
   - Include relevant error messages
