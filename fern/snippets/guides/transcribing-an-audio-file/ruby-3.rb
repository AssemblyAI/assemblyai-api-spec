uri = URI.parse("#{base_url}/v2/transcript")
http = Net::HTTP.new(uri.host, uri.port)
http.use_ssl = true

request = Net::HTTP::Post.new(uri.request_uri, headers)
request.body = data.to_json

response = http.request(request)
response_body = JSON.parse(response.body)

unless response.is_a?(Net::HTTPSuccess)
  raise "API request failed with status #{response.code}: #{response.body}"
end
