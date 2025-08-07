# Weather Data API Integration

Learn how to integrate with weather APIs to fetch and analyze weather information using natural language queries.

## Overview

This example demonstrates how to connect to weather APIs, retrieve current conditions, forecasts, and historical data using ToolFront's natural language interface.

## Setup

Install ToolFront and configure your environment:

```bash
pip install toolfront
export OPENAI_API_KEY=your_api_key_here
```

!!! info "API Requirements"
    This example uses the OpenWeatherMap API. You'll need an API key from [OpenWeatherMap](https://openweathermap.org/api) and access to their OpenAPI specification.

## Basic Weather Queries

Start with simple weather lookups for current conditions:

```python linenums="1"
from toolfront import API
from pydantic import BaseModel

# Connect to the weather API
weather_api = API("https://api.openweathermap.org/data/2.5/openapi.json")

# Simple current weather query
current_temp: float = weather_api.ask("What's the current temperature in New York?")
print(f"NYC Temperature: {current_temp}°F")

# Get weather description
conditions: str = weather_api.ask("What are the current weather conditions in London?")
print(f"London weather: {conditions}")
```

The natural language interface automatically handles API endpoints, parameters, and data parsing.

## Structured Weather Data

Use Pydantic models to get comprehensive weather information:

```python linenums="1"
from typing import Optional

class WeatherConditions(BaseModel):
    temperature: float
    feels_like: float
    humidity: int
    pressure: float
    wind_speed: float
    wind_direction: int
    description: str
    visibility: Optional[float]

# Get detailed weather data
nyc_weather: WeatherConditions = weather_api.ask(
    "Get current weather conditions for New York City with all available details"
)

print("New York City Weather:")
print(f"  🌡️  Temperature: {nyc_weather.temperature}°F (feels like {nyc_weather.feels_like}°F)")
print(f"  💧  Humidity: {nyc_weather.humidity}%")
print(f"  🌀  Pressure: {nyc_weather.pressure} hPa")
print(f"  💨  Wind: {nyc_weather.wind_speed} mph at {nyc_weather.wind_direction}°")
print(f"  👁️  Visibility: {nyc_weather.visibility} miles")
print(f"  ☁️  Conditions: {nyc_weather.description}")
```

!!! tip "Rich Data Models"
    Structured models ensure you get consistent data formats and can easily integrate weather data into your applications.

## Multi-City Weather Comparison

Compare weather across multiple locations:

```python linenums="1"
class CityWeather(BaseModel):
    city: str
    country: str
    temperature: float
    description: str
    humidity: int
    uv_index: Optional[float]

# Compare weather across multiple cities
cities = ["New York", "London", "Tokyo", "Sydney", "São Paulo"]
city_comparison: list[CityWeather] = weather_api.ask(
    f"Get current weather for these cities: {', '.join(cities)}"
)

print("Global Weather Comparison:")
print("=" * 60)
print(f"{'City':<15} {'Country':<10} {'Temp':<8} {'Conditions':<20} {'Humidity'}")
print("-" * 60)

for city in city_comparison:
    print(f"{city.city:<15} {city.country:<10} {city.temperature:>5.1f}°F "
          f"{city.description:<20} {city.humidity:>6}%")
```

## Weather Alerts and Warnings

Check for severe weather alerts:

```python linenums="1"
class WeatherAlert(BaseModel):
    alert_type: str
    severity: str  # Minor, Moderate, Severe, Extreme
    headline: str
    description: str
    start_time: str
    end_time: str
    affected_areas: list[str]

# Check for weather alerts in a specific region
alerts: list[WeatherAlert] = weather_api.ask(
    "Are there any weather alerts or warnings for Florida?"
)

if alerts:
    print("⚠️ Active Weather Alerts:")
    print("=" * 50)
    for alert in alerts:
        severity_emoji = {
            "Minor": "💛",
            "Moderate": "🟡", 
            "Severe": "🟠",
            "Extreme": "🔴"
        }
        
        print(f"{severity_emoji.get(alert.severity, '⚠️')} {alert.alert_type} - {alert.severity}")
        print(f"  📍 Areas: {', '.join(alert.affected_areas)}")
        print(f"  ⏰ Active: {alert.start_time} to {alert.end_time}")
        print(f"  📰 {alert.headline}")
        print()
else:
    print("✅ No active weather alerts")
```

!!! warning "Safety First"
    Always check for weather alerts when planning outdoor activities or travel, especially during severe weather seasons.

## Weather Forecasting

Get extended forecasts for planning purposes:

```python linenums="1"
class DailyForecast(BaseModel):
    date: str
    high_temp: float
    low_temp: float
    description: str
    precipitation_chance: int
    wind_speed: float
    recommendation: str  # Activity recommendations

# Get 7-day forecast
forecast: list[DailyForecast] = weather_api.ask(
    "Get 7-day weather forecast for San Francisco with activity recommendations"
)

print("San Francisco 7-Day Forecast:")
print("=" * 80)
for day in forecast:
    weather_emoji = "☀️" if "sunny" in day.description.lower() else "☁️"
    print(f"{weather_emoji} {day.date}")
    print(f"  🌡️  High: {day.high_temp}°F, Low: {day.low_temp}°F")
    print(f"  🌧️  Precipitation: {day.precipitation_chance}%")
    print(f"  💨  Wind: {day.wind_speed} mph")
    print(f"  📝  {day.description}")
    print(f"  🎯  Recommendation: {day.recommendation}")
    print()
```

## Historical Weather Analysis

Analyze historical weather patterns:

```python linenums="1"
# Add context for better historical analysis
context = """
I'm planning an outdoor event in Chicago for next June. I want to understand 
typical weather patterns, temperature ranges, and precipitation probability 
to make informed decisions about venue and backup plans.
"""

historical_analysis: str = weather_api.ask(
    "Analyze historical weather data for Chicago in June over the past 5 years",
    context=context
)

print("Historical Weather Analysis - Chicago June:")
print("=" * 50)
print(historical_analysis)
```

## Weather-Based Recommendations

Get actionable recommendations based on weather conditions:

```python linenums="1"
class WeatherRecommendation(BaseModel):
    current_conditions: str
    clothing_suggestions: list[str]
    activity_recommendations: list[str]
    travel_advisories: list[str]
    health_considerations: list[str]

# Get comprehensive weather-based recommendations
recommendations: WeatherRecommendation = weather_api.ask(
    "Based on current weather in Denver, provide clothing, activity, and health recommendations"
)

print("Weather-Based Recommendations for Denver:")
print("=" * 50)
print(f"Current conditions: {recommendations.current_conditions}")
print(f"\n👔 Clothing suggestions:")
for item in recommendations.clothing_suggestions:
    print(f"  • {item}")

print(f"\n🎮 Activity recommendations:")
for activity in recommendations.activity_recommendations:
    print(f"  • {activity}")

if recommendations.travel_advisories:
    print(f"\n🚗 Travel advisories:")
    for advisory in recommendations.travel_advisories:
        print(f"  • {advisory}")

if recommendations.health_considerations:
    print(f"\n🏥 Health considerations:")
    for consideration in recommendations.health_considerations:
        print(f"  • {consideration}")
```

!!! info "Personalization"
    Weather recommendations can be customized based on user preferences, health conditions, or specific activities planned.

## Key Takeaways

- **Natural Language**: Query weather APIs using plain English questions
- **Structured Data**: Use Pydantic models for consistent weather data formats
- **Multi-Location**: Compare weather across multiple cities efficiently  
- **Safety Alerts**: Monitor severe weather warnings for safety planning
- **Forecasting**: Plan activities using extended weather forecasts
- **Recommendations**: Get actionable advice based on current conditions

Weather API integration with ToolFront makes it easy to build weather-aware applications without dealing with complex API documentation or data parsing.