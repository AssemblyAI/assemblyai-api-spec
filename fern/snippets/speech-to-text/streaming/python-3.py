token = requests.post(
    'https://api.assemblyai.com/v2/realtime/token',
    headers={
        'Authorization': '<apiKey>',
        'Content-Type': 'application/json'
    },
    json={'expires_in': 60}
).json()['token']
