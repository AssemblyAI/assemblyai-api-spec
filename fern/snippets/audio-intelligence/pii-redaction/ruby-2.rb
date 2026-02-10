data = {
    "audio_url" => upload_url, # You can also use a URL to an audio or video file on the web
    "redact_pii" => true,
    "redact_pii_policies" => ["person_name", "organization", "occupation"],
    "redact_pii_sub" => "hash",
    "redact_pii_audio" => true,
    "redact_pii_audio_quality" => "wav" # Optional. Defaults to "mp3"
}

# ...
redacted_audio_polling_endpoint = URI.parse("#{base_url}/v2/transcript/#{transcript_id}/redacted-audio")

while true
  redacted_audio_polling_http = Net::HTTP.new(redacted_audio_polling_endpoint.host, redacted_audio_polling_endpoint.port)
  redacted_audio_polling_http.use_ssl = true
  redact_audio_polling_request = Net::HTTP::Get.new(redacted_audio_polling_endpoint.request_uri, headers)
  redacted_audio_polling_response = redacted_audio_polling_http.request(redact_audio_polling_request)

  redacted_audio_result = JSON.parse(redacted_audio_polling_response.body)

  if redacted_audio_result['status'] == 'redacted_audio_ready'
    puts redacted_audio_result['redacted_audio_url']
  break
  elsif redacted_audio_result['status'] == 'error'
    raise "Transcription failed: #{redacted_audio_result['error']}"
  else
    sleep(3)
  end
end
