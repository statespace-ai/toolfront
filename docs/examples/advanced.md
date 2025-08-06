# Advanced Examples

Complex workflows combining multiple data sources and advanced techniques.

## Multi-Source Data Pipeline

```python
from toolfront import Database, API, Document
from pydantic import BaseModel

# Connect to multiple data sources
sales_db = Database("postgresql://user:pass@host/sales")
market_api = API("https://api.marketdata.com/openapi.json")
report_doc = Document("/path/to/analyst_report.pdf")

# Gather data from all sources
internal_revenue: float = sales_db.ask("What's our Q4 revenue?")
market_size: float = market_api.ask("What's the total market size for our industry?")
analyst_insights: list[str] = report_doc.ask("What are the key market trends?")

# Calculate business metrics
market_share = (internal_revenue / market_size) * 100
print(f"Market Share: {market_share:.2f}%")
```

## Real-time Analytics Dashboard

```python
from toolfront import Database
from pydantic import BaseModel
import asyncio

class Metrics(BaseModel):
    active_users: int
    revenue_today: float
    conversion_rate: float
    top_product: str

async def get_realtime_metrics():
    db = Database("postgresql://user:pass@host/analytics")
    
    # Get multiple metrics in parallel
    metrics = Metrics(
        active_users=await db.ask("How many users are currently active?"),
        revenue_today=await db.ask("What's today's revenue so far?"),
        conversion_rate=await db.ask("What's today's conversion rate?"),
        top_product=await db.ask("What's the best-selling product today?")
    )
    
    return metrics

# Update dashboard every 5 minutes
while True:
    current_metrics = await get_realtime_metrics()
    print(f"Active Users: {current_metrics.active_users:,}")
    print(f"Revenue Today: ${current_metrics.revenue_today:,.2f}")
    await asyncio.sleep(300)  # 5 minutes
```

## Automated Report Generation

```python
from toolfront import Database, Document
from pydantic import BaseModel
from datetime import datetime
import pandas as pd

class WeeklyReport(BaseModel):
    week_ending: str
    total_revenue: float
    new_customers: int
    top_products: list[str]
    growth_rate: float
    key_insights: list[str]

def generate_weekly_report():
    db = Database("postgresql://user:pass@host/db")
    
    # Generate comprehensive report
    report = WeeklyReport(
        week_ending=datetime.now().strftime("%Y-%m-%d"),
        total_revenue=db.ask("What's our revenue this week?"),
        new_customers=db.ask("How many new customers this week?"),
        top_products=db.ask("What are the top 5 products by sales this week?"),
        growth_rate=db.ask("What's our week-over-week growth rate?"),
        key_insights=db.ask("What are 3 key business insights from this week?")
    )
    
    # Export to multiple formats
    report_dict = report.model_dump()
    
    # Save as JSON
    with open(f"weekly_report_{report.week_ending}.json", "w") as f:
        json.dump(report_dict, f, indent=2)
    
    # Create Excel report
    df = pd.DataFrame([report_dict])
    df.to_excel(f"weekly_report_{report.week_ending}.xlsx", index=False)
    
    return report

weekly_data = generate_weekly_report()
```

## Customer 360 Analysis

```python
from toolfront import Database, API
from pydantic import BaseModel
from typing import List, Optional

class CustomerProfile(BaseModel):
    customer_id: str
    name: str
    email: str
    total_spent: float
    order_count: int
    avg_order_value: float
    last_purchase_date: str
    preferred_categories: List[str]
    churn_risk: str
    lifetime_value: float

def create_customer_360(customer_id: str):
    # Connect to multiple systems
    crm_db = Database("postgresql://user:pass@host/crm")
    orders_db = Database("postgresql://user:pass@host/orders")
    support_api = API("https://api.support.com/openapi.json")
    
    # Build comprehensive customer profile
    profile = CustomerProfile(
        customer_id=customer_id,
        name=crm_db.ask(f"What's the name for customer {customer_id}?"),
        email=crm_db.ask(f"What's the email for customer {customer_id}?"),
        total_spent=orders_db.ask(f"Total spent by customer {customer_id}?"),
        order_count=orders_db.ask(f"How many orders for customer {customer_id}?"),
        avg_order_value=orders_db.ask(f"Average order value for customer {customer_id}?"),
        last_purchase_date=orders_db.ask(f"Last purchase date for customer {customer_id}?"),
        preferred_categories=orders_db.ask(f"Top product categories for customer {customer_id}?"),
        churn_risk=crm_db.ask(f"Churn risk level for customer {customer_id}?"),
        lifetime_value=crm_db.ask(f"Predicted lifetime value for customer {customer_id}?")
    )
    
    return profile

# Analyze high-value customers
high_value_customers = ["CUST001", "CUST002", "CUST003"]
for customer_id in high_value_customers:
    profile = create_customer_360(customer_id)
    print(f"{profile.name}: ${profile.total_spent:,.2f} LTV (Risk: {profile.churn_risk})")
```

## Fraud Detection Pipeline

```python
from toolfront import Database
from pydantic import BaseModel
from typing import List
import pandas as pd

class SuspiciousTransaction(BaseModel):
    transaction_id: str
    amount: float
    timestamp: str
    customer_id: str
    risk_score: float
    red_flags: List[str]

def detect_fraud():
    db = Database("postgresql://user:pass@host/transactions")
    
    # Get potentially fraudulent transactions
    suspicious: List[SuspiciousTransaction] = db.ask(
        "Find transactions with unusual patterns that might be fraudulent"
    )
    
    # Flag high-risk transactions
    high_risk = [t for t in suspicious if t.risk_score > 0.8]
    
    if high_risk:
        print(f"🚨 {len(high_risk)} high-risk transactions detected!")
        
        # Get detailed analysis
        for transaction in high_risk[:5]:  # Top 5 riskiest
            details = db.ask(f"Analyze transaction {transaction.transaction_id} for fraud patterns")
            print(f"Transaction {transaction.transaction_id}: ${transaction.amount:,.2f}")
            print(f"Risk Score: {transaction.risk_score:.2f}")
            print(f"Red Flags: {', '.join(transaction.red_flags)}")
            print("---")
    
    return suspicious

# Run fraud detection
fraud_alerts = detect_fraud()
```

## A/B Test Analysis

```python
from toolfront import Database
from pydantic import BaseModel
import scipy.stats as stats

class ABTestResult(BaseModel):
    test_name: str
    control_group_size: int
    treatment_group_size: int
    control_conversion: float  
    treatment_conversion: float
    p_value: float
    confidence_interval: tuple[float, float]
    is_significant: bool
    recommended_action: str

def analyze_ab_test(test_name: str):
    db = Database("postgresql://user:pass@host/experiments")
    
    # Get test data
    control_data: dict = db.ask(f"Get control group results for {test_name}")
    treatment_data: dict = db.ask(f"Get treatment group results for {test_name}")
    
    # Statistical analysis
    control_conversions = control_data['conversions']
    control_total = control_data['total_users']
    treatment_conversions = treatment_data['conversions'] 
    treatment_total = treatment_data['total_users']
    
    # Calculate conversion rates
    control_rate = control_conversions / control_total
    treatment_rate = treatment_conversions / treatment_total
    
    # Perform statistical test
    _, p_value = stats.chi2_contingency([
        [control_conversions, control_total - control_conversions],
        [treatment_conversions, treatment_total - treatment_conversions]
    ])[:2]
    
    # Determine significance and recommendation
    is_significant = p_value < 0.05
    lift = (treatment_rate - control_rate) / control_rate * 100
    
    if is_significant and lift > 0:
        action = f"Deploy treatment (lift: +{lift:.1f}%)"
    elif is_significant and lift < 0:
        action = f"Reject treatment (decline: {lift:.1f}%)"
    else:
        action = "Continue test - no significant difference"
    
    result = ABTestResult(
        test_name=test_name,
        control_group_size=control_total,
        treatment_group_size=treatment_total,
        control_conversion=control_rate,
        treatment_conversion=treatment_rate,
        p_value=p_value,
        confidence_interval=(control_rate * 0.95, control_rate * 1.05),  # Simplified
        is_significant=is_significant,
        recommended_action=action
    )
    
    return result

# Analyze running tests
test_results = analyze_ab_test("homepage_redesign_v2")
print(f"Test: {test_results.test_name}")
print(f"Control: {test_results.control_conversion:.2%}")
print(f"Treatment: {test_results.treatment_conversion:.2%}")
print(f"P-value: {test_results.p_value:.4f}")
print(f"Recommendation: {test_results.recommended_action}")
```