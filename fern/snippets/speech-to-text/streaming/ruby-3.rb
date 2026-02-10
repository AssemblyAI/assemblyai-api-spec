uri = URI('https://api.assemblyai.com/v2/realtime/token')
request = Net::HTTP::Post.new(uri)
request['Authorization'] = '<apiKey>'
request['Content-Type'] = 'application/json'
request.body = { expires_in: 60 }.to_json

response = Net::HTTP.start(uri.hostname, uri.port, use_ssl: true) { |http| http.request(request) }

token = JSON.parse(response.body)['token']
