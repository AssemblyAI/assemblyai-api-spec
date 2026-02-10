if response.status_code != 200:
    try:
        print(response.json()['error'])
    except Exception:
        print(response.status_code, response.text, response.url)
