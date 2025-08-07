# E-commerce API Integration

Learn how to integrate with e-commerce platforms to manage products, orders, and customer data using natural language queries.

## Overview

This example demonstrates how to connect with e-commerce APIs like Shopify, WooCommerce, or custom platforms to manage your online store operations efficiently.

## Setup

Install ToolFront and configure your environment:

```bash
pip install toolfront
export ANTHROPIC_API_KEY=your_api_key_here
```

!!! info "API Access"
    This example uses a Shopify store API. You'll need API credentials and access to the store's REST API or GraphQL endpoint with proper permissions.

## Product Management

Manage your product catalog with natural language commands:

```python linenums="1"
from toolfront import API
from pydantic import BaseModel
from typing import List, Optional

# Connect to your e-commerce API
store_api = API("https://your-shop.myshopify.com/admin/api/2023-10/openapi.json")

class Product(BaseModel):
    id: int
    title: str
    price: float
    inventory_quantity: int
    status: str
    category: str
    
# Get low inventory products
low_stock: List[Product] = store_api.ask(
    "Show me products with less than 10 items in stock"
)

print("⚠️ Low Stock Alert:")
print("=" * 40)
for product in low_stock:
    print(f"📦 {product.title}")
    print(f"   💰 ${product.price} | 📊 {product.inventory_quantity} left")
    print(f"   📂 {product.category} | Status: {product.status}")
    print()
```

The API automatically handles authentication and endpoint routing for inventory management.

## Order Processing

Monitor and manage orders efficiently:

```python linenums="1"
class OrderSummary(BaseModel):
    order_id: str
    customer_name: str
    order_date: str
    total_amount: float
    status: str
    items_count: int
    shipping_address: str

# Get recent orders that need processing
pending_orders: List[OrderSummary] = store_api.ask(
    "Show me orders from the last 24 hours that need fulfillment"
)

print("📋 Orders Pending Fulfillment:")
print("=" * 50)
for order in pending_orders:
    status_emoji = "🟡" if order.status == "pending" else "🟢"
    print(f"{status_emoji} Order #{order.order_id}")
    print(f"   👤 Customer: {order.customer_name}")
    print(f"   📅 Date: {order.order_date}")
    print(f"   💳 Total: ${order.total_amount}")
    print(f"   📦 Items: {order.items_count}")
    print(f"   🏠 Ship to: {order.shipping_address}")
    print()
```

!!! tip "Order Automation"
    Use this data to trigger automated fulfillment processes or send notifications to your warehouse team.

## Customer Analytics

Analyze customer behavior and purchase patterns:

```python linenums="1"
class CustomerInsight(BaseModel):
    customer_id: str
    name: str
    email: str
    total_orders: int
    lifetime_value: float
    avg_order_value: float
    last_purchase_date: str
    favorite_categories: List[str]

# Identify your top customers
vip_customers: List[CustomerInsight] = store_api.ask(
    "Find customers with lifetime value over $1000 and their purchase patterns"
)

print("👑 VIP Customers:")
print("=" * 60)
for customer in vip_customers[:5]:  # Show top 5
    print(f"🌟 {customer.name} ({customer.email})")
    print(f"   💎 Lifetime Value: ${customer.lifetime_value:,.2f}")
    print(f"   🛒 Orders: {customer.total_orders} (avg: ${customer.avg_order_value:.2f})")
    print(f"   📅 Last purchase: {customer.last_purchase_date}")
    print(f"   ❤️  Favorite categories: {', '.join(customer.favorite_categories)}")
    print()
```

## Sales Performance

Track sales metrics and performance indicators:

```python linenums="1"
class SalesMetrics(BaseModel):
    period: str
    total_revenue: float
    order_count: int
    avg_order_value: float
    conversion_rate: float
    top_selling_products: List[str]
    revenue_by_category: dict[str, float]

# Get comprehensive sales analysis
sales_report: SalesMetrics = store_api.ask(
    "Generate sales performance report for this month with category breakdown"
)

print("📊 Monthly Sales Performance:")
print("=" * 50)
print(f"💰 Total Revenue: ${sales_report.total_revenue:,.2f}")
print(f"📦 Orders: {sales_report.order_count:,}")
print(f"🎯 Average Order Value: ${sales_report.avg_order_value:.2f}")
print(f"🔄 Conversion Rate: {sales_report.conversion_rate:.1%}")

print(f"\n🏆 Top Selling Products:")
for i, product in enumerate(sales_report.top_selling_products[:5], 1):
    print(f"  {i}. {product}")

print(f"\n📂 Revenue by Category:")
for category, revenue in sales_report.revenue_by_category.items():
    percentage = (revenue / sales_report.total_revenue) * 100
    print(f"  {category}: ${revenue:,.2f} ({percentage:.1f}%)")
```

!!! note "Performance Tracking"
    Regular sales analysis helps identify trends, optimize inventory, and make data-driven business decisions.

## Inventory Management

Automate inventory tracking and reordering:

```python linenums="1"
class InventoryAlert(BaseModel):
    product_name: str
    current_stock: int
    reorder_level: int
    daily_sales_rate: float
    days_until_stockout: int
    suggested_reorder_quantity: int
    supplier_info: Optional[str]

# Get inventory alerts and reorder suggestions
inventory_alerts: List[InventoryAlert] = store_api.ask(
    "Analyze inventory levels and suggest reorder quantities for products running low"
)

print("📦 Inventory Management Dashboard:")
print("=" * 70)
for alert in inventory_alerts:
    urgency = "🔴" if alert.days_until_stockout <= 7 else "🟡" if alert.days_until_stockout <= 14 else "🟢"
    
    print(f"{urgency} {alert.product_name}")
    print(f"   📊 Current stock: {alert.current_stock} units")
    print(f"   📈 Daily sales: {alert.daily_sales_rate:.1f} units/day")
    print(f"   ⏰ Days until stockout: {alert.days_until_stockout}")
    print(f"   🔄 Suggested reorder: {alert.suggested_reorder_quantity} units")
    if alert.supplier_info:
        print(f"   🏪 Supplier: {alert.supplier_info}")
    print()
```

## Marketing Campaign Analysis

Analyze the effectiveness of marketing campaigns:

```python linenums="1"
# Add business context for campaign analysis
context = """
We recently ran several marketing campaigns:
1. Email newsletter with 20% discount (Campaign: SAVE20)
2. Social media ads for summer collection
3. Influencer partnerships for new product launches
4. Retargeting ads for abandoned carts

We want to understand which campaigns drove the most revenue and conversions.
"""

campaign_analysis: str = store_api.ask(
    "Analyze the performance of recent marketing campaigns and their ROI",
    context=context
)

print("📈 Marketing Campaign Analysis:")
print("=" * 50)
print(campaign_analysis)
```

## Automated Actions

Execute automated actions based on conditions:

```python linenums="1"
class AutomationRule(BaseModel):
    condition: str
    action: str
    affected_items: List[str]
    estimated_impact: str

# Set up automated responses to common scenarios
automation_suggestions: List[AutomationRule] = store_api.ask(
    "Suggest automation rules for inventory management, pricing, and customer service"
)

print("🤖 Automation Opportunities:")
print("=" * 50)
for rule in automation_suggestions:
    print(f"📋 Condition: {rule.condition}")
    print(f"⚡ Action: {rule.action}")
    print(f"🎯 Affected: {', '.join(rule.affected_items[:3])}")
    print(f"📊 Impact: {rule.estimated_impact}")
    print()
```

!!! warning "Automation Safety"
    Always test automation rules on a small scale before full implementation, and include safeguards to prevent unintended consequences.

## Key Takeaways

- **Natural Language**: Manage your e-commerce operations using plain English commands
- **Order Management**: Streamline order processing and fulfillment workflows
- **Customer Insights**: Understand customer behavior and identify high-value segments
- **Inventory Control**: Automate stock monitoring and reorder suggestions
- **Sales Analytics**: Track performance metrics and identify growth opportunities
- **Marketing ROI**: Measure campaign effectiveness and optimize marketing spend

E-commerce API integration with ToolFront simplifies store management while providing actionable insights for business growth.