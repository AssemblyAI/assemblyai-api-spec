# First get the request_id from a previous LeMUR task response
request_id = result.json()["request_id"]

delete_url = f"https://api.assemblyai.com/lemur/v3/{request_id}"
deletion_response = requests.delete(delete_url, headers=headers)
