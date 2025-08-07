# Social Media Analytics API

Analyze social media performance and engagement metrics using natural language queries with social media platform APIs.

## Overview

This example shows how to connect with social media APIs (Twitter, Instagram, LinkedIn, etc.) to monitor brand mentions, analyze engagement, and track campaign performance.

## Setup

Install ToolFront and configure your environment:

```bash
pip install toolfront
export OPENAI_API_KEY=your_api_key_here
```

!!! info "API Access"
    This example uses Twitter API v2. You'll need a Twitter Developer account and API keys. Similar patterns work with other social media APIs.

## Engagement Analysis

Monitor your social media engagement and performance:

```python linenums="1"
from toolfront import API
from pydantic import BaseModel
from typing import List, Optional

# Connect to social media API
social_api = API("https://api.twitter.com/2/openapi.json")

class PostMetrics(BaseModel):
    post_id: str
    content_preview: str
    post_date: str
    likes: int
    shares: int
    comments: int
    engagement_rate: float
    reach: int
    impressions: int

# Analyze recent post performance
recent_posts: List[PostMetrics] = social_api.ask(
    "Show me performance metrics for posts from the last 7 days"
)

print("📱 Social Media Performance (Last 7 Days):")
print("=" * 60)
print(f"{'Date':<12} {'Likes':<8} {'Shares':<8} {'Comments':<10} {'Engagement':<12}")
print("-" * 60)

for post in recent_posts:
    print(f"{post.post_date:<12} {post.likes:<8} {post.shares:<8} "
          f"{post.comments:<10} {post.engagement_rate:<11.1%}")
    print(f"  📝 {post.content_preview[:50]}...")
    print(f"  👁️  Reach: {post.reach:,} | Impressions: {post.impressions:,}")
    print()
```

## Brand Mention Monitoring

Track mentions of your brand across social platforms:

```python linenums="1"
class BrandMention(BaseModel):
    platform: str
    user_handle: str
    mention_text: str
    sentiment: str  # Positive, Negative, Neutral
    engagement_score: int
    post_date: str
    follower_count: int
    influence_score: float

# Monitor brand mentions and sentiment
brand_mentions: List[BrandMention] = social_api.ask(
    "Find recent mentions of our brand and analyze sentiment"
)

# Group by sentiment
positive = [m for m in brand_mentions if m.sentiment == "Positive"]
negative = [m for m in brand_mentions if m.sentiment == "Negative"]
neutral = [m for m in brand_mentions if m.sentiment == "Neutral"]

print("🎯 Brand Mention Analysis:")
print("=" * 50)
print(f"✅ Positive mentions: {len(positive)}")
print(f"❌ Negative mentions: {len(negative)}")
print(f"➖ Neutral mentions: {len(neutral)}")

if negative:
    print(f"\n⚠️ Negative Mentions Requiring Attention:")
    for mention in negative[:3]:  # Show top 3 negative
        print(f"  👤 @{mention.user_handle} ({mention.follower_count:,} followers)")
        print(f"  💬 {mention.mention_text[:100]}...")
        print(f"  📅 {mention.post_date} | 📊 Influence: {mention.influence_score:.1f}")
        print()
```

!!! warning "Reputation Management"
    Monitor negative mentions closely and respond promptly to maintain your brand reputation, especially from high-influence accounts.

## Audience Insights

Understand your social media audience demographics and behavior:

```python linenums="1"
class AudienceInsight(BaseModel):
    total_followers: int
    growth_rate: float
    demographics: dict[str, float]  # age groups, locations, etc.
    interests: List[str]
    active_hours: List[int]  # hours when audience is most active
    engagement_preferences: dict[str, float]  # video, image, text preference

# Analyze audience characteristics
audience_data: AudienceInsight = social_api.ask(
    "Analyze our follower demographics, interests, and engagement patterns"
)

print("👥 Audience Insights:")
print("=" * 40)
print(f"📈 Total followers: {audience_data.total_followers:,}")
print(f"📊 Growth rate: {audience_data.growth_rate:+.1%} this month")

print(f"\n🌍 Top Demographics:")
for demo, percentage in list(audience_data.demographics.items())[:5]:
    print(f"  {demo}: {percentage:.1%}")

print(f"\n🎯 Top Interests:")
for interest in audience_data.interests[:5]:
    print(f"  • {interest}")

print(f"\n⏰ Peak Activity Hours:")
peak_hours = sorted(audience_data.active_hours)[:5]
print(f"  {', '.join([f'{h}:00' for h in peak_hours])}")

print(f"\n📱 Content Preferences:")
for content_type, preference in audience_data.engagement_preferences.items():
    print(f"  {content_type}: {preference:.1%}")
```

## Campaign Performance

Track social media campaign effectiveness:

```python linenums="1"
class CampaignMetrics(BaseModel):
    campaign_name: str
    start_date: str
    end_date: str
    total_reach: int
    impressions: int
    engagement_rate: float
    click_through_rate: float
    conversion_rate: float
    cost_per_engagement: float
    roi: float

# Analyze recent campaigns
campaigns: List[CampaignMetrics] = social_api.ask(
    "Analyze performance of social media campaigns from the last month"
)

print("🚀 Campaign Performance Analysis:")
print("=" * 70)
print(f"{'Campaign':<20} {'Reach':<10} {'CTR':<8} {'Conv Rate':<10} {'ROI':<8}")
print("-" * 70)

for campaign in campaigns:
    print(f"{campaign.campaign_name:<20} {campaign.total_reach:<10,} "
          f"{campaign.click_through_rate:<7.1%} {campaign.conversion_rate:<9.1%} "
          f"{campaign.roi:<7.1%}")
    print(f"  📅 {campaign.start_date} to {campaign.end_date}")
    print(f"  💰 Cost per engagement: ${campaign.cost_per_engagement:.2f}")
    print()
```

!!! tip "Campaign Optimization"
    Use CTR and conversion rate data to optimize future campaigns. Focus budget on high-performing content types and audiences.

## Content Strategy Analysis

Optimize your content strategy based on performance data:

```python linenums="1"
class ContentAnalysis(BaseModel):
    content_type: str  # video, image, text, link
    avg_engagement_rate: float
    best_posting_times: List[str]
    top_hashtags: List[str]
    optimal_content_length: str
    recommended_posting_frequency: str

# Get content strategy recommendations
content_strategy: List[ContentAnalysis] = social_api.ask(
    "Analyze content performance and recommend optimal posting strategy"
)

print("📝 Content Strategy Recommendations:")
print("=" * 60)
for content in content_strategy:
    print(f"🎨 {content.content_type.title()} Content:")
    print(f"  📊 Avg engagement: {content.avg_engagement_rate:.1%}")
    print(f"  ⏰ Best times: {', '.join(content.best_posting_times)}")
    print(f"  📱 Frequency: {content.recommended_posting_frequency}")
    print(f"  📏 Optimal length: {content.optimal_content_length}")
    
    if content.top_hashtags:
        print(f"  #️⃣  Top hashtags: {', '.join(content.top_hashtags[:5])}")
    print()
```

## Competitor Analysis

Monitor competitor social media performance:

```python linenums="1"
# Add business context for competitor analysis
context = """
Our main competitors in the fitness industry are:
1. FitTech Pro - focuses on wearable devices
2. HealthyLife - wellness and nutrition content
3. GymMaster - fitness equipment and workouts

We want to understand their social media strategies, engagement rates,
and content performance to improve our own approach.
"""

competitor_analysis: str = social_api.ask(
    "Analyze competitor social media performance and identify opportunities",
    context=context
)

print("🔍 Competitor Analysis:")
print("=" * 50)
print(competitor_analysis)
```

## Influencer Identification

Find potential influencers for partnerships:

```python linenums="1"
class InfluencerProfile(BaseModel):
    username: str
    follower_count: int
    engagement_rate: float
    audience_demographics: dict[str, str]
    content_categories: List[str]
    brand_alignment_score: float
    estimated_cost_per_post: float
    recent_brand_partnerships: List[str]

# Identify potential influencers in your niche
influencers: List[InfluencerProfile] = social_api.ask(
    "Find fitness influencers with 10K-100K followers and high engagement rates"
)

print("🌟 Potential Influencer Partners:")
print("=" * 60)
for influencer in influencers[:5]:  # Show top 5
    print(f"👤 @{influencer.username}")
    print(f"  👥 Followers: {influencer.follower_count:,}")
    print(f"  💫 Engagement: {influencer.engagement_rate:.1%}")
    print(f"  🎯 Brand alignment: {influencer.brand_alignment_score:.1f}/10")
    print(f"  💰 Est. cost/post: ${influencer.estimated_cost_per_post:,.0f}")
    print(f"  📂 Categories: {', '.join(influencer.content_categories[:3])}")
    
    if influencer.recent_brand_partnerships:
        print(f"  🤝 Recent partners: {', '.join(influencer.recent_brand_partnerships[:2])}")
    print()
```

!!! info "Influencer Partnerships"
    Consider micro-influencers (10K-100K followers) who often have higher engagement rates and lower costs than mega-influencers.

## Key Takeaways

- **Performance Tracking**: Monitor engagement metrics across all social platforms
- **Sentiment Analysis**: Track brand mentions and respond to feedback promptly
- **Audience Understanding**: Use demographic data to create targeted content
- **Campaign Optimization**: Analyze ROI and adjust strategies based on performance
- **Content Strategy**: Optimize posting times, formats, and frequency
- **Competitive Intelligence**: Learn from competitor strategies and identify gaps
- **Influencer Marketing**: Find authentic partners aligned with your brand values

Social media analytics with ToolFront provides comprehensive insights to improve your social media presence and drive meaningful engagement with your audience.