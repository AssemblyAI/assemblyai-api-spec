data = {
    "transcript_ids" => [transcript_id],
    "prompt" => prompt
}

uri = URI.parse("https://api.assemblyai.com/lemur/v3/generate/task")
http = Net::HTTP.new(uri.host, uri.port)
http.use_ssl = true

request = Net::HTTP::Post.new(uri.request_uri, headers)
request.body = data.to_json

result = http.request(request)
puts result.parsed_response["response"]
