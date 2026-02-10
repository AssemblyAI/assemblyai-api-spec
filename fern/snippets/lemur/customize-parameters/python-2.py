data = {
  "prompt": prompt,
  "transcript_ids": [transcript_id],
  "final_model": final_model,
  "max_output_size": 1000
}

result = requests.post("https://api.assemblyai.com/lemur/v3/generate/task", headers=headers, json=data)
