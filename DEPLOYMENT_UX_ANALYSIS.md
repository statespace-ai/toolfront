# Deployment UX Issues & Solutions

## Current Problems

### 1. Pre-deployment setup unclear
- **Problem**: Users don't know how to get VPC/subnet IDs
- **Who it affects**: Everyone except AWS experts
- **Solution needed**: Step-by-step infrastructure discovery

### 2. AWS CLI assumption  
- **Problem**: Manual database access step requires AWS CLI
- **Who it affects**: 50%+ of users (many don't have CLI configured)
- **Solution needed**: Alternative methods (console instructions + CLI)

### 3. Post-deployment verification unclear
- **Problem**: Users don't know if deployment worked or when to do manual steps
- **Who it affects**: Everyone
- **Solution needed**: Clear success/failure indicators and next steps

### 4. Order of operations confusion
- **Problem**: Unclear what happens when, and what to do if it fails
- **Who it affects**: Everyone  
- **Solution needed**: Step-by-step workflow with decision points

## Proposed User Flow

### Step 1: Prerequisites Check
```bash
# Check AWS access
aws sts get-caller-identity 2>/dev/null || echo "❌ AWS CLI not configured"

# Install AWS CLI if needed (show instructions)
```

### Step 2: Infrastructure Discovery  
```bash
# Option A: Find existing VPC/subnet
aws ec2 describe-vpcs --query 'Vpcs[].[VpcId,Tags[?Key==`Name`].Value|[0]]' --output table

# Option B: Use RDS auto-discovery  
aws rds describe-db-instances --query 'DBInstances[].[DBInstanceIdentifier,DBSubnetGroup.VpcId]' --output table
```

### Step 3: Deploy
```bash
toolfront deploy aws [with discovered values]
```

### Step 4: Verify & Fix
```bash
# Check if it worked
curl http://[ec2-ip]:8000/health

# If failed, add database access rule
[manual steps with exact commands using stack outputs]
```

## Critical Fixes Needed

1. **Pre-flight checks** in the CLI
2. **Infrastructure discovery helpers** 
3. **AWS CLI setup guide** for users who need it
4. **Post-deployment verification** with clear next steps
5. **Web console fallback** for users without CLI
