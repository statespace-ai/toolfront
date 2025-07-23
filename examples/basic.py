import os

from dotenv import load_dotenv

from toolfront import Database

load_dotenv()

pg = Database(url=os.environ["POSTGRES_URL"])
snowflake = Database(url=os.environ["SNOWFLAKE_URL"] + "/NEW_YORK_CITIBIKE_1")

# Quiet mode (default) - no streaming output to terminal
schema_summary = pg.ask("Summarize the database schema including key tables and their relationships", model="anthropic:claude-3-5-sonnet-latest")
print(schema_summary)

# Streaming mode - shows live progress in terminal  
# avg_duration = snowflake.ask("What's the average bike rideshare duration in 2016-2018 in minutes?", model="anthropic:claude-3-5-sonnet-latest", stream=True)
# print(avg_duration)
