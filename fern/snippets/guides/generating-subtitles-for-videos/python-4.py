def get_subtitle_file(transcript_id, file_format):
    if file_format not in ["srt", "vtt"]:
        raise ValueError("Invalid file format. Valid formats are 'srt' and 'vtt'.")

    url = f"https://api.assemblyai.com/v2/transcript/{transcript_id}/{file_format}"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.text
    else:
        raise RuntimeError(f"Failed to retrieve {file_format.upper()} file: {response.status_code} {response.reason}")


subtitle_text = get_subtitle_file(transcript_id, "vtt")
# subtitle_text = get_subtitle_file(transcript_id, "srt")
print(subtitle_text)
