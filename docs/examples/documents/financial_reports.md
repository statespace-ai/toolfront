# Financial Reports Analysis

Extract insights and key information from financial documents like annual reports, earnings statements, and financial summaries using ToolFront.

## Overview

This example demonstrates how to analyze financial documents to extract key metrics, identify trends, and generate summaries for investment decisions or business analysis.

## Setup

Install ToolFront with document processing capabilities:

```bash
pip install toolfront[document-all]
export OPENAI_API_KEY=your_api_key_here
```

!!! info "Document Formats"
    ToolFront supports PDF, DOCX, Excel, and other formats commonly used for financial reporting. Ensure documents are text-readable (not scanned images).

## Annual Report Analysis

Extract key financial metrics from annual reports:

```python linenums="1"
from toolfront import Document
from pydantic import BaseModel
from typing import List, Optional

class FinancialMetrics(BaseModel):
    company_name: str
    fiscal_year: str
    revenue: float
    net_income: float
    gross_margin: float
    operating_margin: float
    debt_to_equity: float
    current_ratio: float
    return_on_equity: float
    earnings_per_share: float

# Analyze a company's annual report
doc = Document("/path/to/annual_report_2023.pdf")

financial_data: FinancialMetrics = doc.ask(
    "Extract key financial metrics including revenue, margins, ratios, and per-share data"
)

print(f"📊 Financial Analysis: {financial_data.company_name} ({financial_data.fiscal_year})")
print("=" * 60)
print(f"💰 Revenue: ${financial_data.revenue:,.0f}")
print(f"💵 Net Income: ${financial_data.net_income:,.0f}")
print(f"📈 Gross Margin: {financial_data.gross_margin:.1%}")
print(f"⚡ Operating Margin: {financial_data.operating_margin:.1%}")
print(f"🏦 Debt-to-Equity: {financial_data.debt_to_equity:.2f}")
print(f"💧 Current Ratio: {financial_data.current_ratio:.2f}")
print(f"🎯 ROE: {financial_data.return_on_equity:.1%}")
print(f"💎 EPS: ${financial_data.earnings_per_share:.2f}")
```

The natural language interface automatically identifies and extracts financial data from complex documents.

## Risk Assessment

Identify risks and challenges mentioned in financial reports:

```python linenums="1"
class RiskAssessment(BaseModel):
    major_risks: List[str]
    regulatory_concerns: List[str]
    market_challenges: List[str]
    competitive_threats: List[str]
    mitigation_strategies: List[str]
    risk_level: str  # Low, Medium, High

# Extract risk information from the document
risk_analysis: RiskAssessment = doc.ask(
    "Identify and categorize all risks, challenges, and mitigation strategies mentioned"
)

print("⚠️ Risk Assessment:")
print("=" * 40)
print(f"🎯 Overall Risk Level: {risk_analysis.risk_level}")

print(f"\n🚨 Major Risks:")
for i, risk in enumerate(risk_analysis.major_risks, 1):
    print(f"  {i}. {risk}")

print(f"\n⚖️ Regulatory Concerns:")
for concern in risk_analysis.regulatory_concerns:
    print(f"  • {concern}")

print(f"\n🏢 Competitive Threats:")
for threat in risk_analysis.competitive_threats:
    print(f"  • {threat}")

if risk_analysis.mitigation_strategies:
    print(f"\n🛡️ Mitigation Strategies:")
    for strategy in risk_analysis.mitigation_strategies:
        print(f"  • {strategy}")
```

!!! warning "Due Diligence"
    Always review risk disclosures carefully when making investment decisions. Financial documents may contain forward-looking statements with inherent uncertainties.

## Multi-Year Comparison

Compare financial performance across multiple years:

```python linenums="1"
class YearlyComparison(BaseModel):
    year: str
    revenue: float
    net_income: float
    revenue_growth: Optional[float]
    profit_margin: float

# Process multiple years of financial reports
years = ["2021", "2022", "2023"]
yearly_data: List[YearlyComparison] = []

for year in years:
    doc = Document(f"/path/to/annual_report_{year}.pdf")
    
    year_data: YearlyComparison = doc.ask(
        f"Extract revenue, net income, and profit margin for {year} with growth rates"
    )
    yearly_data.append(year_data)

print("📈 Multi-Year Financial Comparison:")
print("=" * 60)
print(f"{'Year':<6} {'Revenue':<15} {'Net Income':<15} {'Growth':<10} {'Margin'}")
print("-" * 60)

for data in yearly_data:
    growth_str = f"{data.revenue_growth:+.1%}" if data.revenue_growth else "N/A"
    print(f"{data.year:<6} ${data.revenue:<14,.0f} ${data.net_income:<14,.0f} "
          f"{growth_str:<10} {data.profit_margin:.1%}")
```

## Executive Summary Extraction

Generate concise summaries of key business developments:

```python linenums="1"
class ExecutiveSummary(BaseModel):
    key_achievements: List[str]
    strategic_initiatives: List[str]
    financial_highlights: List[str]
    future_outlook: str
    management_priorities: List[str]

# Extract executive summary and key messages
executive_info: ExecutiveSummary = doc.ask(
    "Summarize key achievements, strategic initiatives, and management outlook"
)

print("👔 Executive Summary:")
print("=" * 50)

print("🏆 Key Achievements:")
for achievement in executive_info.key_achievements:
    print(f"  ✅ {achievement}")

print(f"\n🎯 Strategic Initiatives:")
for initiative in executive_info.strategic_initiatives:
    print(f"  🚀 {initiative}")

print(f"\n💡 Financial Highlights:")
for highlight in executive_info.financial_highlights:
    print(f"  💰 {highlight}")

print(f"\n🔮 Future Outlook:")
print(f"  {executive_info.future_outlook}")

print(f"\n📋 Management Priorities:")
for priority in executive_info.management_priorities:
    print(f"  📌 {priority}")
```

## Segment Analysis

Analyze business segment performance from detailed reports:

```python linenums="1"
class BusinessSegment(BaseModel):
    segment_name: str
    revenue: float
    operating_income: float
    margin: float
    growth_rate: float
    key_metrics: dict[str, str]

# Extract segment-level performance data
segments: List[BusinessSegment] = doc.ask(
    "Extract performance data for all business segments including growth rates"
)

print("🏢 Business Segment Performance:")
print("=" * 70)
print(f"{'Segment':<20} {'Revenue':<15} {'Op. Income':<15} {'Margin':<10} {'Growth'}")
print("-" * 70)

for segment in segments:
    print(f"{segment.segment_name:<20} ${segment.revenue:<14,.0f} "
          f"${segment.operating_income:<14,.0f} {segment.margin:<9.1%} "
          f"{segment.growth_rate:+.1%}")
    
    if segment.key_metrics:
        print(f"  📊 Key metrics: {', '.join([f'{k}: {v}' for k, v in segment.key_metrics.items()])}")
    print()
```

!!! tip "Segment Focus"
    Pay attention to segment trends to understand which parts of the business are driving growth or facing challenges.

## ESG Analysis

Extract Environmental, Social, and Governance information:

```python linenums="1"
# Add context for ESG analysis
context = """
I'm analyzing this company for ESG (Environmental, Social, Governance) compliance.
Key areas of interest include:
- Environmental impact and sustainability initiatives
- Social responsibility and employee practices
- Corporate governance and ethical standards
- Diversity and inclusion efforts
- Climate change commitments and targets
"""

esg_analysis: str = doc.ask(
    "Extract and analyze ESG initiatives, commitments, and performance metrics",
    context=context
)

print("🌍 ESG Analysis:")
print("=" * 40)
print(esg_analysis)
```

## Investment Decision Support

Generate investment recommendations based on document analysis:

```python linenums="1"
class InvestmentAnalysis(BaseModel):
    overall_rating: str  # Strong Buy, Buy, Hold, Sell, Strong Sell
    strengths: List[str]
    weaknesses: List[str]
    opportunities: List[str]
    threats: List[str]
    target_price: Optional[float]
    investment_horizon: str
    key_catalysts: List[str]

# Comprehensive investment analysis
investment_view: InvestmentAnalysis = doc.ask(
    "Provide comprehensive investment analysis with SWOT framework and recommendations"
)

print("💹 Investment Analysis:")
print("=" * 50)
print(f"📊 Overall Rating: {investment_view.overall_rating}")

if investment_view.target_price:
    print(f"🎯 Target Price: ${investment_view.target_price:.2f}")

print(f"⏰ Investment Horizon: {investment_view.investment_horizon}")

print(f"\n💪 Strengths:")
for strength in investment_view.strengths:
    print(f"  ✅ {strength}")

print(f"\n⚠️ Weaknesses:")
for weakness in investment_view.weaknesses:
    print(f"  ❌ {weakness}")

print(f"\n🚀 Key Catalysts:")
for catalyst in investment_view.key_catalysts:
    print(f"  🔥 {catalyst}")
```

!!! note "Investment Disclaimer"
    This analysis is for informational purposes only and should not be considered as financial advice. Always consult with qualified financial advisors before making investment decisions.

## Key Takeaways

- **Automated Extraction**: Extract financial metrics from complex documents automatically
- **Risk Analysis**: Identify and categorize business risks and mitigation strategies
- **Trend Analysis**: Compare performance across multiple reporting periods
- **Strategic Insights**: Understand management priorities and business direction
- **Segment Performance**: Analyze individual business unit contributions
- **ESG Compliance**: Evaluate environmental, social, and governance factors
- **Investment Support**: Generate comprehensive investment analysis frameworks

Financial document analysis with ToolFront streamlines due diligence processes and provides structured insights for better decision-making.