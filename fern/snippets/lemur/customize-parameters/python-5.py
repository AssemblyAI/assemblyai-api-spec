data = {
  "prompt": prompt,
  "transcript_ids": [id1, id2, id3],
  "final_model": final_model,
}

result = requests.post("https://api.assemblyai.com/lemur/v3/generate/task", headers=headers, json=data)
