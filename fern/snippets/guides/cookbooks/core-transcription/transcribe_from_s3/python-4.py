# Specify the endpoint of the transaction.
get_endpoint = transcript_endpoint + "/" + post_response.json()["id"]

# GET request the transcription.
get_response = requests.get(get_endpoint, headers=headers)

# If the transcription has not finished, wait util it has.
while get_response.json()["status"] != "completed":
    get_response = requests.get(get_endpoint, headers=headers)
    time.sleep(5)

# Once the transcription is complete, print it out.
print(get_response.json()["text"])
