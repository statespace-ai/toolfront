# Legal Contracts Analysis

Analyze legal documents, contracts, and agreements to extract key terms, identify risks, and understand obligations using ToolFront.

## Overview

This example demonstrates how to process legal contracts to extract important clauses, analyze terms and conditions, identify potential risks, and summarize complex legal language in plain English.

## Setup

Install ToolFront with document processing capabilities:

```bash
pip install toolfront[document-all]
export OPENAI_API_KEY=your_api_key_here
```

!!! warning "Legal Disclaimer"
    This tool is for informational purposes only and does not constitute legal advice. Always consult with qualified legal professionals for contract review and legal matters.

## Contract Overview Analysis

Extract basic contract information and structure:

```python linenums="1"
from toolfront import Document
from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import date

class ContractOverview(BaseModel):
    contract_type: str
    parties: List[str]
    effective_date: str
    expiration_date: Optional[str]
    governing_law: str
    contract_value: Optional[float]
    key_subject_matter: str
    renewal_terms: Optional[str]

# Analyze a legal contract
doc = Document("/path/to/service_agreement.pdf")

contract_info: ContractOverview = doc.ask(
    "Extract basic contract information including parties, dates, governing law, and subject matter"
)

print("⚖️ Contract Analysis Summary")
print("=" * 50)
print(f"📄 Contract Type: {contract_info.contract_type}")
print(f"📅 Effective Date: {contract_info.effective_date}")

if contract_info.expiration_date:
    print(f"⏰ Expiration Date: {contract_info.expiration_date}")

print(f"🏛️ Governing Law: {contract_info.governing_law}")

if contract_info.contract_value:
    print(f"💰 Contract Value: ${contract_info.contract_value:,.2f}")

print(f"\n👥 Parties:")
for i, party in enumerate(contract_info.parties, 1):
    print(f"  {i}. {party}")

print(f"\n📋 Subject Matter:")
print(f"  {contract_info.key_subject_matter}")

if contract_info.renewal_terms:
    print(f"\n🔄 Renewal Terms:")
    print(f"  {contract_info.renewal_terms}")
```

The natural language interface automatically identifies and structures legal document components.

## Key Terms and Obligations

Extract important terms, conditions, and obligations:

```python linenums="1"
class ContractObligation(BaseModel):
    party: str
    obligation: str
    deadline: Optional[str]
    penalty_for_breach: Optional[str]

class KeyTerms(BaseModel):
    payment_terms: str
    delivery_terms: str
    performance_standards: List[str]
    intellectual_property_rights: str
    confidentiality_requirements: str
    termination_conditions: List[str]
    key_obligations: List[ContractObligation]

# Extract detailed terms and obligations
key_terms: KeyTerms = doc.ask(
    "Extract all key terms, payment conditions, obligations, and performance requirements"
)

print("📋 Key Contract Terms:")
print("=" * 50)

print(f"💳 Payment Terms:")
print(f"  {key_terms.payment_terms}")

print(f"\n🚚 Delivery Terms:")
print(f"  {key_terms.delivery_terms}")

print(f"\n📊 Performance Standards:")
for standard in key_terms.performance_standards:
    print(f"  • {standard}")

print(f"\n🧠 Intellectual Property:")
print(f"  {key_terms.intellectual_property_rights}")

print(f"\n🔒 Confidentiality:")
print(f"  {key_terms.confidentiality_requirements}")

print(f"\n🏁 Termination Conditions:")
for condition in key_terms.termination_conditions:
    print(f"  • {condition}")

print(f"\n⚖️ Key Obligations:")
for obligation in key_terms.key_obligations:
    print(f"  👤 {obligation.party}:")
    print(f"     📝 {obligation.obligation}")
    if obligation.deadline:
        print(f"     ⏰ Deadline: {obligation.deadline}")
    if obligation.penalty_for_breach:
        print(f"     ⚠️ Penalty: {obligation.penalty_for_breach}")
    print()
```

!!! tip "Obligation Tracking"
    Use extracted obligations to create compliance checklists and deadline tracking systems for contract management.

## Risk Assessment

Identify potential legal and business risks in the contract:

```python linenums="1"
class ContractRisk(BaseModel):
    risk_category: str  # Financial, Legal, Operational, Reputational
    risk_description: str
    severity: str  # Low, Medium, High, Critical
    likelihood: str  # Low, Medium, High
    mitigation_suggestions: List[str]

class RiskAssessment(BaseModel):
    overall_risk_level: str
    identified_risks: List[ContractRisk]
    red_flags: List[str]
    missing_clauses: List[str]
    negotiation_recommendations: List[str]

# Analyze contract risks
risk_analysis: RiskAssessment = doc.ask(
    "Identify all potential risks, red flags, missing clauses, and provide negotiation recommendations"
)

print("⚠️ Contract Risk Assessment:")
print("=" * 60)
print(f"🎯 Overall Risk Level: {risk_analysis.overall_risk_level}")

if risk_analysis.red_flags:
    print(f"\n🚩 Red Flags:")
    for flag in risk_analysis.red_flags:
        print(f"  ❗ {flag}")

print(f"\n📊 Identified Risks:")
for risk in risk_analysis.identified_risks:
    severity_emoji = {"Low": "🟢", "Medium": "🟡", "High": "🟠", "Critical": "🔴"}
    risk_emoji = severity_emoji.get(risk.severity, "⚠️")
    
    print(f"\n{risk_emoji} {risk.risk_category} Risk - {risk.severity} Severity")
    print(f"   📋 {risk.risk_description}")
    print(f"   🎲 Likelihood: {risk.likelihood}")
    
    if risk.mitigation_suggestions:
        print(f"   🛡️ Mitigation:")
        for suggestion in risk.mitigation_suggestions:
            print(f"      • {suggestion}")

if risk_analysis.missing_clauses:
    print(f"\n❌ Missing Important Clauses:")
    for clause in risk_analysis.missing_clauses:
        print(f"  • {clause}")

if risk_analysis.negotiation_recommendations:
    print(f"\n💼 Negotiation Recommendations:")
    for recommendation in risk_analysis.negotiation_recommendations:
        print(f"  🤝 {recommendation}")
```

## Financial Terms Analysis

Extract and analyze all financial aspects of the contract:

```python linenums="1"
class FinancialTerms(BaseModel):
    total_contract_value: Optional[float]
    payment_schedule: List[str]
    penalty_amounts: Dict[str, float]
    expense_allocation: str
    price_adjustment_mechanisms: List[str]
    currency: str
    tax_responsibilities: str
    invoicing_requirements: str

# Analyze financial terms
financial_terms: FinancialTerms = doc.ask(
    "Extract all financial terms including payment schedules, penalties, and cost allocations"
)

print("💰 Financial Terms Analysis:")
print("=" * 50)

if financial_terms.total_contract_value:
    print(f"💵 Total Contract Value: {financial_terms.currency} {financial_terms.total_contract_value:,.2f}")

print(f"\n📅 Payment Schedule:")
for payment in financial_terms.payment_schedule:
    print(f"  • {payment}")

if financial_terms.penalty_amounts:
    print(f"\n⚠️ Penalty Amounts:")
    for penalty_type, amount in financial_terms.penalty_amounts.items():
        print(f"  • {penalty_type}: {financial_terms.currency} {amount:,.2f}")

print(f"\n💸 Expense Allocation:")
print(f"  {financial_terms.expense_allocation}")

if financial_terms.price_adjustment_mechanisms:
    print(f"\n📊 Price Adjustments:")
    for mechanism in financial_terms.price_adjustment_mechanisms:
        print(f"  • {mechanism}")

print(f"\n🧾 Tax Responsibilities:")
print(f"  {financial_terms.tax_responsibilities}")

print(f"\n📄 Invoicing Requirements:")
print(f"  {financial_terms.invoicing_requirements}")
```

!!! note "Financial Planning"
    Use financial terms analysis for budgeting, cash flow planning, and financial risk assessment.

## Compliance Requirements

Identify regulatory and compliance obligations:

```python linenums="1"
class ComplianceRequirement(BaseModel):
    requirement_type: str
    description: str
    responsible_party: str
    compliance_deadline: Optional[str]
    documentation_needed: List[str]
    regulatory_body: Optional[str]

# Extract compliance requirements
compliance: List[ComplianceRequirement] = doc.ask(
    "Identify all compliance requirements, regulatory obligations, and documentation needs"
)

print("📋 Compliance Requirements:")
print("=" * 50)

for req in compliance:
    print(f"📌 {req.requirement_type}")
    print(f"   📝 {req.description}")
    print(f"   👤 Responsible: {req.responsible_party}")
    
    if req.compliance_deadline:
        print(f"   ⏰ Deadline: {req.compliance_deadline}")
    
    if req.regulatory_body:
        print(f"   🏛️ Regulatory Body: {req.regulatory_body}")
    
    if req.documentation_needed:
        print(f"   📄 Required Documentation:")
        for doc_req in req.documentation_needed:
            print(f"      • {doc_req}")
    print()
```

## Plain Language Summary

Generate a plain English summary for non-legal stakeholders:

```python linenums="1"
# Add context for business-friendly summary
context = """
I need to explain this contract to business stakeholders who are not lawyers.
They need to understand:
1. What we're agreeing to do
2. What the other party will do
3. How much it costs and when we pay
4. What happens if things go wrong
5. How we can get out of the contract if needed

Please use simple, clear language and avoid legal jargon.
"""

business_summary: str = doc.ask(
    "Create a plain English summary of this contract for business stakeholders",
    context=context
)

print("👔 Plain English Contract Summary:")
print("=" * 60)
print(business_summary)
```

## Contract Comparison

Compare similar contracts to identify differences:

```python linenums="1"
class ContractComparison(BaseModel):
    contract_name: str
    key_differences: List[str]
    more_favorable_terms: List[str]
    less_favorable_terms: List[str]
    unique_clauses: List[str]
    overall_preference: str

# Compare with a template or previous contract
comparison_doc = Document("/path/to/previous_contract.pdf")

# Compare contracts
comparison: ContractComparison = doc.ask(
    f"Compare this contract with the previous version and identify key differences, advantages, and disadvantages"
)

print("⚖️ Contract Comparison:")
print("=" * 50)
print(f"📊 Overall Assessment: {comparison.overall_preference}")

print(f"\n🔍 Key Differences:")
for diff in comparison.key_differences:
    print(f"  • {diff}")

print(f"\n✅ More Favorable Terms:")
for term in comparison.more_favorable_terms:
    print(f"  • {term}")

print(f"\n❌ Less Favorable Terms:")
for term in comparison.less_favorable_terms:
    print(f"  • {term}")

if comparison.unique_clauses:
    print(f"\n🆕 Unique Clauses:")
    for clause in comparison.unique_clauses:
        print(f"  • {clause}")
```

## Action Items Generator

Create actionable next steps based on contract analysis:

```python linenums="1"
class ActionItem(BaseModel):
    task: str
    responsible_party: str
    priority: str  # High, Medium, Low
    deadline: Optional[str]
    dependencies: List[str]

# Generate action items from contract analysis
action_items: List[ActionItem] = doc.ask(
    "Based on this contract, create action items for implementation, compliance, and risk management"
)

print("✅ Contract Implementation Action Items:")
print("=" * 60)

# Sort by priority
high_priority = [item for item in action_items if item.priority == "High"]
medium_priority = [item for item in action_items if item.priority == "Medium"]
low_priority = [item for item in action_items if item.priority == "Low"]

for priority_group, items in [("🔴 High Priority", high_priority), ("🟡 Medium Priority", medium_priority), ("🟢 Low Priority", low_priority)]:
    if items:
        print(f"\n{priority_group}:")
        for item in items:
            print(f"  📋 {item.task}")
            print(f"     👤 Responsible: {item.responsible_party}")
            if item.deadline:
                print(f"     ⏰ Deadline: {item.deadline}")
            if item.dependencies:
                print(f"     🔗 Dependencies: {', '.join(item.dependencies)}")
            print()
```

!!! warning "Legal Review Required"
    Always have qualified legal counsel review contracts before signing. This analysis is a tool to support, not replace, professional legal advice.

## Key Takeaways

- **Structured Extraction**: Automatically identify and organize contract components
- **Risk Assessment**: Identify potential legal and business risks systematically
- **Financial Analysis**: Extract and analyze all monetary terms and obligations
- **Compliance Tracking**: Identify regulatory requirements and deadlines
- **Plain Language**: Translate legal jargon for business stakeholders
- **Comparison Tools**: Analyze differences between contract versions
- **Action Planning**: Generate implementation and compliance checklists

Legal contract analysis with ToolFront streamlines contract review processes, improves risk identification, and helps ensure compliance with contractual obligations.