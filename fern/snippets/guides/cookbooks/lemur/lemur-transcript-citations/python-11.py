import json, datetime

def timestamp_action_items(action_items_array):

    for action_item in action_items_array:
        matches = find_relevant_matches(embeddings, action_item['action_item'], k=1)
        for index, m in enumerate(matches):
            action_item['quote'] = m['text']
            action_item['timestamp'] = m['timestamp']
    return action_items_array
