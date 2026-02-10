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
    puts 'Transcription completed!'
    puts "Transcription text: #{transcription_result['text']}"
    break
  elsif transcription_result['status'] == 'error'
    raise "Transcription failed: #{transcription_result['error']}"
  else
    puts 'Waiting for transcription to complete...'
    sleep(3)
  end
end
