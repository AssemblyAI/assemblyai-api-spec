data = {
    "audio_url" => upload_url
}

uri = URI.parse("#{base_url}/transcript")
http = Net::HTTP.new(uri.host, uri.port)
http.use_ssl = true

request = Net::HTTP::Post.new(uri.request_uri, headers)
request.body = data.to_json

response = http.request(request)
