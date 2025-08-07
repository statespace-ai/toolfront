# Financial Reporting

Generate comprehensive financial reports and analysis using natural language queries with your financial database.

## Overview

This example demonstrates how to create financial reports, analyze revenue trends, and calculate key financial metrics using ToolFront's natural language interface.

## Setup

Install ToolFront with your database support and set up authentication:

```bash
pip install toolfront[postgres]
export OPENAI_API_KEY=your_api_key_here
```

!!! info "Database Schema" 
    This example uses financial tables: `revenue` (date, amount, category, region), `expenses` (date, amount, category, department), and `accounts` (account_id, account_name, balance, account_type).

## Monthly Financial Summary

Generate a comprehensive monthly financial report:

```python linenums="1"
from toolfront import Database
from pydantic import BaseModel
from typing import List

# Connect to your financial database
db = Database("postgresql://user:pass@localhost:5432/finance")

class MonthlySummary(BaseModel):
    month: str
    total_revenue: float
    total_expenses: float
    net_profit: float
    profit_margin: float
    growth_rate: float

# Generate monthly summary report
monthly_report: List[MonthlySummary] = db.ask(
    "Generate monthly financial summary for the past 12 months with profit margins and growth rates"
)

print("Monthly Financial Summary")
print("=" * 60)
print(f"{'Month':<12} {'Revenue':<12} {'Expenses':<12} {'Profit':<12} {'Margin':<8} {'Growth':<8}")
print("-" * 60)

for month in monthly_report:
    print(f"{month.month:<12} "
          f"${month.total_revenue:>10,.0f} "
          f"${month.total_expenses:>10,.0f} "
          f"${month.net_profit:>10,.0f} "
          f"{month.profit_margin:>6.1%} "
          f"{month.growth_rate:>+6.1%}")
```

## Revenue Analysis by Category

Analyze revenue breakdown across different categories:

```python linenums="1"
class RevenueBreakdown(BaseModel):
    category: str
    current_month: float
    previous_month: float
    percentage_of_total: float
    month_over_month_change: float

# Analyze revenue by category
revenue_analysis: List[RevenueBreakdown] = db.ask(
    "Break down revenue by category showing month-over-month changes and percentages"
)

print("\nRevenue Analysis by Category")
print("=" * 70)
for category in revenue_analysis:
    change_indicator = "📈" if category.month_over_month_change > 0 else "📉"
    print(f"{category.category}:")
    print(f"  Current: ${category.current_month:,.2f} ({category.percentage_of_total:.1%} of total)")
    print(f"  Change: {change_indicator} {category.month_over_month_change:+.1%} vs last month")
    print()
```

!!! tip "Visual Indicators"
    Using emojis or symbols in reports makes them more readable and helps quickly identify trends.

## Expense Analysis

Analyze expenses by department and category:

```python linenums="1"
class ExpenseAnalysis(BaseModel):
    department: str
    total_expenses: float
    budget_variance: float  # positive = under budget
    top_expense_categories: List[str]
    cost_per_employee: float

# Analyze departmental expenses
expense_report: List[ExpenseAnalysis] = db.ask(
    "Analyze expenses by department with budget variance and cost per employee"
)

print("Departmental Expense Analysis")
print("=" * 50)
for dept in expense_report:
    status = "✅ Under Budget" if dept.budget_variance > 0 else "⚠️ Over Budget"
    print(f"{dept.department}:")
    print(f"  Total expenses: ${dept.total_expenses:,.2f}")
    print(f"  Budget variance: ${dept.budget_variance:+,.2f} ({status})")
    print(f"  Cost per employee: ${dept.cost_per_employee:,.2f}")
    print(f"  Top categories: {', '.join(dept.top_expense_categories[:3])}")
    print()
```

## Key Performance Indicators (KPIs)

Calculate and track essential financial KPIs:

```python linenums="1"
class FinancialKPIs(BaseModel):
    gross_margin: float
    operating_margin: float
    current_ratio: float
    debt_to_equity: float
    return_on_assets: float
    cash_flow: float

# Calculate key financial metrics
kpis: FinancialKPIs = db.ask(
    "Calculate key financial KPIs including margins, ratios, and cash flow for this quarter"
)

print("Key Performance Indicators")
print("=" * 40)
print(f"📊 Gross Margin: {kpis.gross_margin:.1%}")
print(f"💼 Operating Margin: {kpis.operating_margin:.1%}")
print(f"💰 Current Ratio: {kpis.current_ratio:.2f}")
print(f"📈 Debt-to-Equity: {kpis.debt_to_equity:.2f}")
print(f"🎯 Return on Assets: {kpis.return_on_assets:.1%}")
print(f"💸 Cash Flow: ${kpis.cash_flow:,.2f}")
```

!!! note "Benchmarking"
    Compare your KPIs against industry benchmarks to understand your company's relative performance.

## Forecasting and Trends

Use historical data to generate forecasts:

```python linenums="1"
# Add business context for better forecasting
context = """
Our business is a SaaS company with subscription revenue. We typically see:
- Higher revenue in Q4 due to year-end enterprise deals
- Seasonal dips in Q1 and Q3
- Monthly recurring revenue (MRR) growth averaging 8-12%
- Customer acquisition costs trending down due to improved processes
"""

forecast: str = db.ask(
    "Based on historical trends, forecast next quarter's revenue and identify key risk factors",
    context=context
)

print("Revenue Forecast & Risk Analysis")
print("=" * 40)
print(forecast)
```

## Cash Flow Analysis

Track cash flow patterns and liquidity:

```python linenums="1"
class CashFlowAnalysis(BaseModel):
    operating_cash_flow: float
    investing_cash_flow: float
    financing_cash_flow: float
    net_cash_flow: float
    cash_runway_months: int
    burn_rate: float

# Analyze cash flow
cash_flow: CashFlowAnalysis = db.ask(
    "Analyze cash flow components and calculate runway based on current burn rate"
)

print("Cash Flow Analysis")
print("=" * 30)
print(f"Operating Cash Flow: ${cash_flow.operating_cash_flow:,.2f}")
print(f"Investing Cash Flow: ${cash_flow.investing_cash_flow:,.2f}")
print(f"Financing Cash Flow: ${cash_flow.financing_cash_flow:,.2f}")
print(f"Net Cash Flow: ${cash_flow.net_cash_flow:,.2f}")
print(f"Monthly Burn Rate: ${cash_flow.burn_rate:,.2f}")
print(f"Cash Runway: {cash_flow.cash_runway_months} months")

if cash_flow.cash_runway_months < 12:
    print("⚠️ Warning: Cash runway less than 12 months")
```

!!! warning "Cash Management"
    Monitor cash runway closely, especially for startups and growth companies. Plan fundraising or cost optimization when runway drops below 12-18 months.

## Key Takeaways

- **Automated Reporting**: Generate comprehensive financial reports with natural language
- **Trend Analysis**: Identify patterns and growth opportunities in your financial data
- **KPI Tracking**: Monitor essential financial metrics consistently
- **Forecasting**: Use historical data to predict future performance
- **Risk Management**: Identify potential financial risks early

Financial reporting with ToolFront eliminates manual spreadsheet work while providing deeper insights into your business performance.