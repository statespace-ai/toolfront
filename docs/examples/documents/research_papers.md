# Research Papers Analysis

Extract key findings, methodologies, and insights from academic research papers and scientific publications using ToolFront.

## Overview

This example demonstrates how to analyze research papers to understand methodologies, extract key findings, identify citations, and summarize complex academic content for easier comprehension.

## Setup

Install ToolFront with document processing capabilities:

```bash
pip install toolfront[document-all]
export ANTHROPIC_API_KEY=your_api_key_here
```

!!! info "Document Types"
    ToolFront works with PDF research papers, arXiv preprints, journal articles, and conference proceedings. Text-based PDFs work best.

## Paper Metadata Extraction

Extract basic information and structure from research papers:

```python linenums="1"
from toolfront import Document
from pydantic import BaseModel
from typing import List, Optional

class Author(BaseModel):
    name: str
    affiliation: str
    email: Optional[str]

class PaperMetadata(BaseModel):
    title: str
    authors: List[Author]
    publication_venue: str
    publication_date: str
    doi: Optional[str]
    abstract: str
    keywords: List[str]
    field_of_study: str

# Analyze a research paper
doc = Document("/path/to/research_paper.pdf")

paper_info: PaperMetadata = doc.ask(
    "Extract paper metadata including authors, publication details, and abstract"
)

print(f"📄 Research Paper Analysis")
print("=" * 60)
print(f"📝 Title: {paper_info.title}")
print(f"📅 Published: {paper_info.publication_date}")
print(f"🏢 Venue: {paper_info.publication_venue}")
print(f"🔬 Field: {paper_info.field_of_study}")

if paper_info.doi:
    print(f"🔗 DOI: {paper_info.doi}")

print(f"\n👥 Authors:")
for author in paper_info.authors:
    print(f"  • {author.name} - {author.affiliation}")

print(f"\n🔑 Keywords: {', '.join(paper_info.keywords)}")

print(f"\n📋 Abstract:")
print(f"  {paper_info.abstract}")
```

The natural language interface automatically identifies and structures academic paper components.

## Methodology Analysis

Extract and understand the research methodology:

```python linenums="1"
class ResearchMethodology(BaseModel):
    research_type: str  # Experimental, Theoretical, Survey, Case Study, etc.
    data_sources: List[str]
    sample_size: Optional[int]
    methodology_description: str
    tools_and_techniques: List[str]
    limitations: List[str]
    ethical_considerations: Optional[str]

# Analyze research methodology
methodology: ResearchMethodology = doc.ask(
    "Extract and analyze the research methodology, data sources, and limitations"
)

print("🔬 Research Methodology:")
print("=" * 50)
print(f"📊 Research Type: {methodology.research_type}")

if methodology.sample_size:
    print(f"👥 Sample Size: {methodology.sample_size:,}")

print(f"\n📚 Data Sources:")
for source in methodology.data_sources:
    print(f"  • {source}")

print(f"\n🛠️ Tools & Techniques:")
for tool in methodology.tools_and_techniques:
    print(f"  • {tool}")

print(f"\n⚠️ Limitations:")
for limitation in methodology.limitations:
    print(f"  • {limitation}")

print(f"\n📖 Methodology Overview:")
print(f"  {methodology.methodology_description}")

if methodology.ethical_considerations:
    print(f"\n⚖️ Ethical Considerations:")
    print(f"  {methodology.ethical_considerations}")
```

!!! tip "Methodology Review"
    Understanding the methodology helps assess the validity and reliability of research findings, crucial for academic review and replication.

## Key Findings Extraction

Identify and structure the main research findings:

```python linenums="1"
class ResearchFinding(BaseModel):
    finding_title: str
    description: str
    significance_level: Optional[str]  # p-value or confidence level
    supporting_data: List[str]
    implications: str

class ResearchResults(BaseModel):
    primary_findings: List[ResearchFinding]
    secondary_findings: List[str]
    statistical_significance: bool
    practical_significance: str
    novel_contributions: List[str]

# Extract key research findings
results: ResearchResults = doc.ask(
    "Extract and categorize all research findings with their significance and implications"
)

print("🎯 Key Research Findings:")
print("=" * 60)

print("🏆 Primary Findings:")
for i, finding in enumerate(results.primary_findings, 1):
    print(f"\n{i}. {finding.finding_title}")
    print(f"   📋 {finding.description}")
    
    if finding.significance_level:
        print(f"   📊 Significance: {finding.significance_level}")
    
    if finding.supporting_data:
        print(f"   📈 Supporting data: {', '.join(finding.supporting_data[:2])}")
    
    print(f"   💡 Implications: {finding.implications}")

if results.secondary_findings:
    print(f"\n📌 Secondary Findings:")
    for finding in results.secondary_findings:
        print(f"  • {finding}")

print(f"\n🆕 Novel Contributions:")
for contribution in results.novel_contributions:
    print(f"  ✨ {contribution}")

print(f"\n🎲 Statistical Significance: {'Yes' if results.statistical_significance else 'No'}")
print(f"🌟 Practical Significance: {results.practical_significance}")
```

## Literature Review Analysis

Understand how the paper relates to existing research:

```python linenums="1"
class LiteratureReview(BaseModel):
    key_references: List[str]
    research_gaps_identified: List[str]
    theoretical_framework: str
    building_upon: List[str]  # Previous work this research builds on
    contradicts_or_challenges: List[str]
    citation_count_estimate: Optional[int]

# Analyze literature review and positioning
lit_review: LiteratureReview = doc.ask(
    "Analyze the literature review, identify research gaps, and show how this work fits into existing research"
)

print("📚 Literature Review Analysis:")
print("=" * 50)

print("🏗️ Theoretical Framework:")
print(f"  {lit_review.theoretical_framework}")

print(f"\n🔍 Research Gaps Identified:")
for gap in lit_review.research_gaps_identified:
    print(f"  🕳️ {gap}")

print(f"\n📖 Key References:")
for ref in lit_review.key_references[:5]:  # Show top 5
    print(f"  • {ref}")

if lit_review.building_upon:
    print(f"\n🏗️ Builds Upon:")
    for work in lit_review.building_upon:
        print(f"  ⬆️ {work}")

if lit_review.contradicts_or_challenges:
    print(f"\n⚡ Challenges/Contradicts:")
    for challenge in lit_review.contradicts_or_challenges:
        print(f"  ❌ {challenge}")
```

## Future Research Directions

Identify suggested future work and research opportunities:

```python linenums="1"
class FutureResearch(BaseModel):
    immediate_next_steps: List[str]
    long_term_directions: List[str]
    methodological_improvements: List[str]
    unanswered_questions: List[str]
    potential_applications: List[str]

# Extract future research suggestions
future_work: FutureResearch = doc.ask(
    "Identify future research directions, unanswered questions, and potential applications suggested by the authors"
)

print("🚀 Future Research Directions:")
print("=" * 50)

print("⏭️ Immediate Next Steps:")
for step in future_work.immediate_next_steps:
    print(f"  1️⃣ {step}")

print(f"\n🎯 Long-term Directions:")
for direction in future_work.long_term_directions:
    print(f"  🔮 {direction}")

print(f"\n🛠️ Methodological Improvements:")
for improvement in future_work.methodological_improvements:
    print(f"  ⚙️ {improvement}")

print(f"\n❓ Unanswered Questions:")
for question in future_work.unanswered_questions:
    print(f"  ❔ {question}")

print(f"\n🌍 Potential Applications:")
for application in future_work.potential_applications:
    print(f"  💼 {application}")
```

!!! note "Research Opportunities"
    Future research directions often provide excellent starting points for new research projects or grant proposals.

## Comparative Analysis

Compare multiple papers on similar topics:

```python linenums="1"
class PaperComparison(BaseModel):
    paper_title: str
    main_finding: str
    methodology: str
    sample_size: Optional[int]
    key_limitation: str
    innovation_score: float  # 1-10 scale

# Compare related papers
papers = [
    "/path/to/paper1.pdf",
    "/path/to/paper2.pdf", 
    "/path/to/paper3.pdf"
]

comparisons: List[PaperComparison] = []

for paper_path in papers:
    doc = Document(paper_path)
    comparison: PaperComparison = doc.ask(
        "Summarize this paper for comparison: main finding, methodology, limitations, and rate innovation 1-10"
    )
    comparisons.append(comparison)

print("📊 Paper Comparison Analysis:")
print("=" * 80)
print(f"{'Title':<30} {'Method':<15} {'Sample':<10} {'Innovation':<10}")
print("-" * 80)

for comp in comparisons:
    sample_str = f"{comp.sample_size:,}" if comp.sample_size else "N/A"
    title_short = comp.paper_title[:27] + "..." if len(comp.paper_title) > 30 else comp.paper_title
    method_short = comp.methodology[:12] + "..." if len(comp.methodology) > 15 else comp.methodology
    
    print(f"{title_short:<30} {method_short:<15} {sample_str:<10} {comp.innovation_score:<10.1f}")
    print(f"  📋 Finding: {comp.main_finding}")
    print(f"  ⚠️  Limitation: {comp.key_limitation}")
    print()
```

## Research Summary Generator

Create executive summaries for non-technical audiences:

```python linenums="1"
# Add context for audience-appropriate summary
context = """
I need to present this research to business executives who are not technical experts.
They need to understand:
1. What problem this research solves
2. What the researchers found
3. How this could impact our business
4. Whether we should invest in this area

Please use plain language and focus on practical implications.
"""

business_summary: str = doc.ask(
    "Create an executive summary explaining this research in business terms with practical implications",
    context=context
)

print("👔 Executive Summary for Business Audience:")
print("=" * 60)
print(business_summary)
```

## Citation Network Analysis

Analyze citation patterns and research impact:

```python linenums="1"
class CitationAnalysis(BaseModel):
    total_references: int
    self_citations: int
    recent_citations: int  # papers from last 3 years
    seminal_papers_cited: List[str]  # highly cited foundational papers
    citation_diversity: str  # How diverse are the citation sources
    potential_impact: str  # Predicted citation impact

# Analyze citation patterns
citations: CitationAnalysis = doc.ask(
    "Analyze the citation patterns, reference diversity, and predict potential research impact"
)

print("📈 Citation Analysis:")
print("=" * 40)
print(f"📚 Total references: {citations.total_references}")
print(f"🔄 Self-citations: {citations.self_citations}")
print(f"🆕 Recent citations: {citations.recent_citations}")
print(f"🌍 Citation diversity: {citations.citation_diversity}")
print(f"🎯 Potential impact: {citations.potential_impact}")

if citations.seminal_papers_cited:
    print(f"\n📖 Key Seminal Papers Referenced:")
    for paper in citations.seminal_papers_cited[:3]:
        print(f"  • {paper}")
```

!!! info "Research Impact"
    Citation analysis helps assess the quality and potential impact of research, useful for evaluating researchers or research directions.

## Key Takeaways

- **Structured Extraction**: Automatically extract and organize complex academic content
- **Methodology Review**: Understand research approaches and assess validity
- **Finding Analysis**: Identify key discoveries and their significance
- **Literature Positioning**: Understand how research fits into existing knowledge
- **Future Directions**: Identify research opportunities and next steps
- **Comparative Analysis**: Compare multiple papers systematically
- **Business Translation**: Convert technical findings into business insights
- **Impact Assessment**: Evaluate research quality and potential influence

Research paper analysis with ToolFront accelerates literature reviews, supports grant writing, and helps researchers stay current with developments in their field.