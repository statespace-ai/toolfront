# API Examples

Examples for connecting to and querying REST APIs using OpenAPI specifications.

## Stock Market API

```python
from toolfront import API

# Connect to financial API
api = API("https://api.financialdata.com/openapi.json")

# Get stock prices
apple_price: float = api.ask("What's AAPL's current stock price?")
tech_stocks: dict[str, float] = api.ask("Get prices for AAPL, GOOGL, MSFT")

print(f"Apple: ${apple_price}")
```

## Weather API

```python
from toolfront import API
from pydantic import BaseModel

class Weather(BaseModel):
    temperature: float
    humidity: int
    description: str

api = API("https://api.weather.com/openapi.json")

# Get structured weather data
nyc_weather: Weather = api.ask("What's the current weather in New York?")
print(f"NYC: {nyc_weather.temperature}°F, {nyc_weather.description}")
```

## E-commerce API

```python
from toolfront import API

# Connect to e-commerce platform
api = API("https://api.shopify.com/openapi.json", 
          headers={"Authorization": "Bearer your-token"})

# Business intelligence queries
top_products: list[str] = api.ask("What are our best-selling products this month?")
order_count: int = api.ask("How many orders did we process yesterday?")
```

## Social Media API

```python
from toolfront import API
from pydantic import BaseModel
from typing import List

class Post(BaseModel):
    content: str
    likes: int
    shares: int
    engagement_rate: float

api = API("https://api.socialmedia.com/openapi.json")

# Get social media insights
trending_posts: List[Post] = api.ask("Show our top 10 posts by engagement")
for post in trending_posts:
    print(f"Engagement: {post.engagement_rate:.1%} - {post.content[:50]}...")
```

## CRM API

```python
from toolfront import API

# Connect to CRM system
api = API("https://api.salesforce.com/openapi.json",
          headers={"Authorization": "Bearer your-token"})

# Sales analytics
pipeline_value: float = api.ask("What's our total pipeline value?")
closed_deals: int = api.ask("How many deals closed this quarter?")
conversion_rate: float = api.ask("What's our lead to customer conversion rate?")
```

## Custom Business API

```python
from toolfront import API
from pydantic import BaseModel

class Customer(BaseModel):
    name: str
    email: str
    lifetime_value: float
    segment: str

# Connect to your business API
api = API("https://api.yourbusiness.com/v1/openapi.json")

# Customer analytics
high_value_customers: list[Customer] = api.ask("Find customers with LTV > $10,000")
churn_risk: list[str] = api.ask("Which customers are at risk of churning?")
```