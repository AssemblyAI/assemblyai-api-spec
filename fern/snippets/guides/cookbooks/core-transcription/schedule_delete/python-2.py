# In production, you should store your API keys in environment variables
EASYCRON_API_TOKEN = "YOUR_EASYCRON_API_KEY"

from datetime import datetime, timedelta, timezone

# Calculate the time 24 hours from now in EasyCron's expected format
# EasyCron uses a slightly different format, but for simplicity, we'll use the standard UTC format
# and convert this into a cron expression
time_24_hours_from_now = datetime.now(timezone.utc) + timedelta(hours=24)
cron_minute = time_24_hours_from_now.minute
cron_hour = time_24_hours_from_now.hour
cron_day = time_24_hours_from_now.day
cron_month = time_24_hours_from_now.month
cron_year = time_24_hours_from_now.year

cron_expression = f'{cron_minute} {cron_hour} {cron_day} {cron_month} * {cron_year}'
