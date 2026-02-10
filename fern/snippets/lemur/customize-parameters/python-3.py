data = {
  "prompt": prompt,
  "transcript_ids": [transcript_id],
  "final_model": final_model,
  "temperature": 0.7
}

result = requests.post("https://api.assemblyai.com/lemur/v3/generate/task", headers=headers, json=data)
