require 'net/http'
require 'json'

base_url = 'https://api.assemblyai.com'

headers = {
  'authorization' => '<YOUR_API_KEY>',
  'content-type' => 'application/json'
}

path = "/my_audio.mp3"
uri = URI("#{base_url}/v2/upload")
request = Net::HTTP::Post.new(uri, headers)
request.body = File.read(path)

http = Net::HTTP.new(uri.host, uri.port)
http.use_ssl = true
upload_response = http.request(request)
upload_url = JSON.parse(upload_response.body)["upload_url"]

data = {
    "audio_url" => upload_url, # You can also use a URL to an audio or video file on the web
    "speech_models" => ["universal-3-pro", "universal-2"],
    "language_detection" => true,
    "content_safety" => true,
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

    transcription_result['content_safety_labels']['results'].each do |result|
      puts result['text']
      puts "Timestamp: #{result['timestamp']['start']} - #{result['timestamp']['end']}"

      # Get category, confidence, and severity.
      result['labels'].each do |label|
        puts "#{label['label']} - #{label['confidence']} - #{label['severity']}"  # content safety category
      end
    end
    # Get the confidence of the most common labels in relation to the entire audio file.
    transcription_result['content_safety_labels']['summary'].each do |label, confidence|
      puts "#{confidence * 100}% confident that the audio contains #{label}"
    end
    # Get the overall severity of the most common labels in relation to the entire audio file.
    transcription_result['content_safety_labels']['severity_score_summary'].each do |label, severity_confidence|
      puts "#{severity_confidence['low'] * 100}% confident that the audio contains low-severity #{label}"
      puts "#{severity_confidence['medium'] * 100}% confident that the audio contains medium-severity #{label}"
      puts "#{severity_confidence['high'] * 100}% confident that the audio contains high-severity #{label}"
    end
  break
  elsif transcription_result['status'] == 'error'
    raise "Transcription failed: #{transcription_result['error']}"
  else
    sleep(3)
  end
end
