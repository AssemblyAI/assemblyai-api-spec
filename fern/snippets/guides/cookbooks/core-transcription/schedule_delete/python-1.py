import assemblyai as aai
import requests
from datetime import datetime, timedelta, timezone

# Set up AssemblyAI API key
# In production, store this in an environment variable
aai.settings.api_key = "YOUR_ASSEMBLYAI_API_KEY"

# Get an EasyCron API key here: https://www.easycron.com/user/token
# Set up EasyCron API key
# In production, store this in an environment variable
EASYCRON_API_TOKEN = "YOUR_EASYCRON_API_KEY"

# Create transcriber instance and transcribe audio
transcriber = aai.Transcriber()
transcript = transcriber.transcribe('https://assembly.ai/sports_injuries.mp3')

# Get the transcript ID
transcript_id = transcript.id

# Construct the URL for the DELETE request
url_to_call = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"

# Calculate the time 24 hours from now for the cron expression
time_24_hours_from_now = datetime.now(timezone.utc) + timedelta(hours=24)
cron_minute = time_24_hours_from_now.minute
cron_hour = time_24_hours_from_now.hour
cron_day = time_24_hours_from_now.day
cron_month = time_24_hours_from_now.month
cron_year = time_24_hours_from_now.year

# Create the cron expression
cron_expression = f'{cron_minute} {cron_hour} {cron_day} {cron_month} * {cron_year}'

# EasyCron API endpoint for creating a new cron job
api_endpoint = 'https://www.easycron.com/rest/add'

# Data payload for EasyCron API
data = {
    'token': EASYCRON_API_TOKEN,
    'url': url_to_call,
    'cron_expression': cron_expression,
    'http_method': "DELETE",
    'http_headers': f'Authorization: {aai.settings.api_key}',
    'timezone': 'UTC'
}

# Make the request to EasyCron's API
response = requests.post(api_endpoint, data=data)

# Print the response from EasyCron
print("EasyCron API Response:")
print(response.text)
