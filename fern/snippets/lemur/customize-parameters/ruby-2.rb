request = Net::HTTP::Post.new("https://api.assemblyai.com/lemur/v3/generate/task", headers)
request.body = {
  transcript_ids: [transcript_id],
  prompt: prompt,
  final_model: final_model,
  max_output_size: 1000
}.to_json

response = http.request(lemur_request)
