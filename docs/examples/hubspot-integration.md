# HubSpot Integration

Connect to HubSpot CRM and analyze your sales and marketing data with natural language.

```python linenums="1"
from toolfront import API
from pydantic import BaseModel

# Connect to HubSpot API (requires your API key in headers)
hubspot = API(
    "https://api.hubapi.com/api-catalog-public/v1/apis/crm/v3/objects",
    headers={"Authorization": "Bearer YOUR_HUBSPOT_API_KEY"}
)

# Get contact information
contacts: list[dict] = hubspot.ask(
    "Get all contacts created in the last 30 days with email, company, and deal stage"
)

print(f"Found {len(contacts)} recent contacts")
```

!!! info "HubSpot API Key"
    Get your API key from HubSpot Settings → Integrations → API key. Set it as an environment variable: `export HUBSPOT_API_KEY=your_key`

## Analyze Deals Pipeline

```python linenums="14"
class Deal(BaseModel):
    dealname: str
    amount: float
    dealstage: str
    closedate: str
    hubspot_owner_id: str

# Get deals from pipeline
recent_deals: list[Deal] = hubspot.ask(
    "Get deals from the last quarter with deal name, amount, stage, close date, and owner"
)

# Analyze pipeline by stage
pipeline_analysis = {}
total_value = 0

for deal in recent_deals:
    stage = deal.dealstage
    pipeline_analysis[stage] = pipeline_analysis.get(stage, 0) + 1
    total_value += deal.amount

print(f"Total pipeline value: ${total_value:,.2f}")
print("Deals by stage:", pipeline_analysis)
```

## Lead Analysis

Get insights on your marketing qualified leads:

```python linenums="35"
# Get MQLs and their sources
mqls: list[dict] = hubspot.ask(
    "Get marketing qualified leads from last month with lead source, email, and lifecycle stage"
)

# Analyze lead sources
lead_sources = {}
for lead in mqls:
    source = lead.get('lead_source', 'Unknown')
    lead_sources[source] = lead_sources.get(source, 0) + 1

print(f"Total MQLs: {len(mqls)}")
print("Top lead sources:")
for source, count in sorted(lead_sources.items(), key=lambda x: x[1], reverse=True):
    print(f"  {source}: {count} leads")
```

## Company Intelligence

Analyze your company database:

```python linenums="50"
# Get companies with revenue data
companies: list[dict] = hubspot.ask(
    "Get companies with annual revenue over $1M, including name, industry, and employee count"
)

# Find top industries
industries = {}
total_revenue = 0

for company in companies:
    industry = company.get('industry', 'Unknown')
    industries[industry] = industries.get(industry, 0) + 1
    
    revenue = company.get('annualrevenue', 0)
    if revenue:
        total_revenue += float(revenue)

print(f"High-value companies: {len(companies)}")
print(f"Combined revenue: ${total_revenue:,.2f}")
print("Top industries:", dict(list(industries.items())[:5]))
```

## Email Campaign Performance

Track your marketing campaigns:

```python linenums="68"
# Get email campaign metrics
campaigns: list[dict] = hubspot.ask(
    "Get email campaigns from last month with name, sent count, open rate, and click rate"
)

# Find best performing campaigns
best_campaigns = sorted(
    campaigns, 
    key=lambda c: c.get('open_rate', 0), 
    reverse=True
)[:5]

print("Top 5 email campaigns by open rate:")
for i, campaign in enumerate(best_campaigns, 1):
    name = campaign.get('name', 'Unknown')
    open_rate = campaign.get('open_rate', 0)
    click_rate = campaign.get('click_rate', 0)
    
    print(f"  {i}. {name}")
    print(f"     Open: {open_rate:.1%} | Click: {click_rate:.1%}")
```

## Sales Rep Performance

Analyze your sales team performance:

```python linenums="87"
# Get deals closed by sales rep
rep_performance: list[dict] = hubspot.ask(
    "Get deals closed this quarter grouped by owner with total value and deal count"
)

print("Sales rep performance this quarter:")
for rep in sorted(rep_performance, key=lambda r: r.get('total_value', 0), reverse=True):
    owner = rep.get('owner_name', 'Unknown')
    total_value = rep.get('total_value', 0)
    deal_count = rep.get('deal_count', 0)
    avg_deal = total_value / deal_count if deal_count > 0 else 0
    
    print(f"{owner}:")
    print(f"  Total: ${total_value:,.0f} | Deals: {deal_count} | Avg: ${avg_deal:.0f}")
```

## Custom Reports

Generate custom insights by combining data:

```python linenums="102"
def generate_monthly_report():
    # Get multiple data points
    new_contacts = hubspot.ask("Count of new contacts this month")
    closed_deals = hubspot.ask("Sum of closed won deals this month")
    pipeline_value = hubspot.ask("Sum of open deals in pipeline")
    
    # Get conversion rates
    conversions: dict = hubspot.ask(
        "Get conversion rates from visitor to lead to customer for this month"
    )
    
    report = f"""
🚀 Monthly HubSpot Report
========================

📊 Key Metrics:
  • New contacts: {new_contacts}
  • Revenue closed: ${closed_deals:,.2f}
  • Pipeline value: ${pipeline_value:,.2f}

📈 Conversion Rates:
  • Visitor to Lead: {conversions.get('visitor_to_lead', 0):.1%}
  • Lead to Customer: {conversions.get('lead_to_customer', 0):.1%}

🎯 Pipeline Health: {"Good" if pipeline_value > closed_deals * 3 else "Needs Attention"}
"""
    
    return report

monthly_report = generate_monthly_report()
print(monthly_report)
```

!!! tip "Real-World Use Cases"
    - **Sales Forecasting**: Analyze pipeline trends and deal velocity
    - **Lead Scoring**: Identify highest-value lead sources  
    - **Campaign ROI**: Track marketing performance and attribution
    - **Sales Coaching**: Identify top performers and improvement areas