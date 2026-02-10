request = Net::HTTP::Post.new("https://api.assemblyai.com/lemur/v3/generate/task", headers)
request.body = {
  transcript_ids: [id1, id2, id3],
  prompt: prompt,
  final_model: final_model
}.to_json

response = http.request(request)
