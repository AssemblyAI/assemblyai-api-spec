request = Net::HTTP::Post.new("https://api.assemblyai.com/lemur/v3/generate/task", headers)
request.body = {
  final_model: "anthropic/claude-sonnet-4-20250514",
  prompt: prompt,
  transcript_ids: [transcript_id]
}.to_json

response = http.request(lemur_request)
