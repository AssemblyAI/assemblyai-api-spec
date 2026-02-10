require 'net/http'
require 'json'

base_url = 'https://api.assemblyai.com'

headers = {
  'authorization' => '<YOUR_API_KEY>',
  'content-type' => 'application/json'
}

path = "./my-audio.mp3"
uri = URI("#{base_url}/v2/upload")
request = Net::HTTP::Post.new(uri, headers)
request.body = File.read(path)

http = Net::HTTP.new(uri.host, uri.port)
http.use_ssl = true
upload_response = http.request(request)
upload_url = JSON.parse(upload_response.body)["upload_url"]

data = {
    "audio_url" => upload_url, # You can also use a URL to an audio or video file on the web
    "audio_start_from" => 5000, # The start time of the transcription in milliseconds
    "audio_end_at" => 15000 # The end time of the transcription in milliseconds
}

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

transcript_id = response_body['id']
puts "Transcript ID: #{transcript_id}"

polling_endpoint = URI.parse("#{base_url}/v2/transcript/#{transcript_id}")

while true
  polling_http = Net::HTTP.new(polling_endpoint.host, polling_endpoint.port)
  polling_http.use_ssl = true
  polling_request = Net::HTTP::Get.new(polling_endpoint.request_uri, headers)
  polling_response = polling_http.request(polling_request)

  transcription_result = JSON.parse(polling_response.body)

  if transcription_result['status'] == 'completed'
    puts "Transcription text: #{transcription_result['text']}"
    break
  elsif transcription_result['status'] == 'error'
    raise "Transcription failed: #{transcription_result['error']}"
  else
    puts 'Waiting for transcription to complete...'
    sleep(3)
  end
end
