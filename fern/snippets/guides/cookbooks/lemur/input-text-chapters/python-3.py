paragraphs = requests.get(polling_endpoint + '/paragraphs', headers=headers).json()['paragraphs']
combined_paragraphs = []
step = 2  # Adjust as needed if you want combined paragraphs to be shorter or longer in length.

# Combine paragraphs into groups, finding the appropriate timestamps and combining all their text into one string.
for i in range(0, len(paragraphs), step):
    paragraph_group = paragraphs[i : i + step]
    start = paragraph_group[0]['start']
    end = paragraph_group[-1]['end']
    text = ""
    for paragraph in paragraph_group:
        text += f"{paragraph['text']} "
    combined_paragraphs.append(f"Paragraph: {text} Start: {start} End: {end}")
