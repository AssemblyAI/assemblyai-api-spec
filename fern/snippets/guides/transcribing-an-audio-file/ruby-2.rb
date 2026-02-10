path = "/my_audio.mp3"
uri = URI("#{base_url}/v2/upload")
request = Net::HTTP::Post.new(uri, headers)
request.body = File.read(path)

http = Net::HTTP.new(uri.host, uri.port)
http.use_ssl = true
upload_response = http.request(request)
upload_url = JSON.parse(upload_response.body)["upload_url"]
