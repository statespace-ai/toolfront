import os

from dotenv import load_dotenv

from toolfront import Database

load_dotenv()

pg = Database(url=os.environ["POSTGRES_URL"])
snowflake = Database(url=os.environ["SNOWFLAKE_URL"] + "/NEW_YORK_CITIBIKE_1")

# avg_duration = snowflake.ask("What's the average bike rideshare duration in 2016-2018 in minutes?", model="anthropic:claude-3-5-sonnet-latest")
# print(avg_duration)


schema_summary = pg.ask("Summarize the database schema including key tables and their relationships", model="anthropic:claude-3-5-sonnet-latest")
print(schema_summary)
