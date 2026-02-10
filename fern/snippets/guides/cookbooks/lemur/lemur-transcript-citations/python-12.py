transcripts = transcribe([
    '', # TODO add file URLs here
])

# TODO: choose granularity either sentence or paragraph
embeddings = create_transcripts_embeddings(transcripts, 'paragraph')

action_item_results = transcripts.lemur.action_items(
    context=action_item_context,
    answer_format=action_item_answer_format).response

# Replace preamble in LeMUR response
action_item_results = action_item_results.replace('Here are action items based on the transcript:', '')

action_item_json_array = json.loads(action_item_results.strip())
action_item_json_array = timestamp_action_items(action_item_json_array)
print(json.dumps(action_item_json_array, indent=4))
