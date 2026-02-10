speaker_mapping = {}

for qa_response in result.response:
    pattern = r"Who is speaker (\w)\?"
    match = re.search(pattern, qa_response.question)
    if match and match.group(1) not in speaker_mapping.keys():
        speaker_mapping.update({match.group(1): qa_response.answer})
