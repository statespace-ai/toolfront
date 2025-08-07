# Customer Insights

Extract customer behavior patterns and insights from your database using natural language queries.

## Overview

This example shows how to analyze customer data to understand purchasing behavior, segment customers, and identify trends that drive business decisions.

## Setup

Install ToolFront with your database support and configure your environment:

```bash
pip install toolfront[postgres]
export ANTHROPIC_API_KEY=your_api_key_here
```

!!! info "Database Schema"
    This example uses tables: `customers` (customer_id, name, email, signup_date, segment), `orders` (order_id, customer_id, total_amount, order_date), and `order_items` (order_id, product_id, quantity, price).

## Customer Segmentation

Analyze your customer base and identify key segments:

```python linenums="1"
from toolfront import Database
from pydantic import BaseModel
from typing import List

# Connect to your customer database
db = Database("postgresql://user:pass@localhost:5432/crm")

class CustomerSegment(BaseModel):
    segment: str
    customer_count: int
    avg_order_value: float
    total_revenue: float
    retention_rate: float

# Analyze customer segments
segments: List[CustomerSegment] = db.ask(
    "Analyze customer segments with retention rates and revenue metrics"
)

print("Customer Segmentation Analysis:")
print("=" * 60)
for segment in segments:
    print(f"{segment.segment}:")
    print(f"  • {segment.customer_count:,} customers")
    print(f"  • ${segment.avg_order_value:.2f} average order value")
    print(f"  • ${segment.total_revenue:,.2f} total revenue")
    print(f"  • {segment.retention_rate:.1%} retention rate")
    print()
```

## Customer Lifetime Value

Calculate and analyze customer lifetime value (CLV):

```python linenums="1"
class CustomerValue(BaseModel):
    customer_name: str
    total_orders: int
    lifetime_value: float
    avg_order_frequency: float  # orders per month
    last_order_date: str

# Identify high-value customers
high_value_customers: List[CustomerValue] = db.ask(
    "Show me the top 20 customers by lifetime value with their ordering patterns"
)

print("Top Customers by Lifetime Value:")
print("-" * 50)
for customer in high_value_customers[:10]:  # Show top 10
    print(f"{customer.customer_name}:")
    print(f"  LTV: ${customer.lifetime_value:,.2f}")
    print(f"  Orders: {customer.total_orders} ({customer.avg_order_frequency:.1f}/month)")
    print(f"  Last order: {customer.last_order_date}")
    print()
```

!!! tip "Business Intelligence"
    Use CLV analysis to identify your most valuable customers for targeted marketing campaigns and retention programs.

## Purchase Behavior Analysis

Understand customer purchase patterns and preferences:

```python linenums="1"
class PurchasePattern(BaseModel):
    customer_segment: str
    most_popular_products: List[str]
    avg_time_between_orders: int  # days
    peak_purchase_hours: List[int]
    seasonal_preferences: str

# Analyze purchase behavior by segment
purchase_patterns: List[PurchasePattern] = db.ask(
    "Analyze purchase patterns by customer segment including timing and product preferences"
)

for pattern in purchase_patterns:
    print(f"\n{pattern.customer_segment} Customers:")
    print(f"  Popular products: {', '.join(pattern.most_popular_products[:3])}")
    print(f"  Order frequency: Every {pattern.avg_time_between_orders} days")
    print(f"  Peak hours: {pattern.peak_purchase_hours}")
    print(f"  Seasonal trends: {pattern.seasonal_preferences}")
```

## Churn Risk Analysis

Identify customers at risk of churning:

```python linenums="1"
# Simple churn risk analysis
churn_risk: dict = db.ask(
    "Identify customers who haven't ordered in 90+ days but were previously active"
)

print(f"Customers at risk of churn: {churn_risk}")

# For more structured analysis
class ChurnRisk(BaseModel):
    customer_name: str
    last_order_date: str
    days_since_last_order: int
    previous_order_frequency: float
    risk_score: str  # High, Medium, Low

at_risk_customers: List[ChurnRisk] = db.ask(
    "Calculate churn risk scores for customers based on their ordering history"
)

high_risk = [c for c in at_risk_customers if c.risk_score == "High"]
print(f"\nHigh-risk customers: {len(high_risk)}")
for customer in high_risk[:5]:  # Show top 5
    print(f"  {customer.customer_name}: {customer.days_since_last_order} days inactive")
```

!!! warning "Proactive Retention"
    Use churn risk analysis to implement proactive retention strategies before customers leave.

## Customer Journey Analysis

Track the customer journey from acquisition to conversion:

```python linenums="1"
# Add business context for better journey analysis
context = """
Our customer journey typically involves:
1. Website visit or email campaign
2. Product browsing
3. First purchase (often with discount)
4. Repeat purchases
5. Potential upsells to premium products

We track conversion rates and customer satisfaction scores.
"""

journey_insights: str = db.ask(
    "Analyze the customer journey and identify optimization opportunities",
    context=context
)

print("Customer Journey Insights:")
print(journey_insights)
```

## Key Takeaways

- **Segmentation**: Understand different customer groups and their characteristics
- **Lifetime Value**: Focus on high-value customers for maximum ROI
- **Behavior Patterns**: Use purchase patterns to optimize inventory and marketing
- **Churn Prevention**: Identify at-risk customers early for retention efforts
- **Journey Optimization**: Improve the customer experience at each touchpoint

Customer insights drive strategic decisions around marketing, product development, and customer service initiatives.