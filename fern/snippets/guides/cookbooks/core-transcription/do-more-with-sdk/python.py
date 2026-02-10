json_file = open('transcript.json', 'w', encoding='utf8')
json_str = json.dumps(transcript.json_response, ensure_ascii=False, indent=2)

json_file.write(json_str)
json_file.close()

print(json_str)
