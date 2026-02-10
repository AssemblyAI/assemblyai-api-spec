import requests

# EasyCron API endpoint for creating a new cron job
api_endpoint = 'https://www.easycron.com/rest/add'

# The data to be sent to EasyCron's API
data = {
    'token': EASYCRON_API_TOKEN,
    'url': url_to_call,
    'cron_expression': cron_expression,
    'http_method': "DELETE",
    'http_headers': f'Authorization: {AAI_API_TOKEN}',
    'timezone': 'UTC'
}

# Make the request to EasyCron's API
response = requests.post(api_endpoint, data=data)

# Print the response from EasyCron's API
print(response.text)
