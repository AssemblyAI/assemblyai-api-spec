llm_gateway_uri = URI("https://llm-gateway.assemblyai.com/v1/chat/completions")
llm_gateway_request = Net::HTTP::Post.new(llm_gateway_uri, headers)
llm_gateway_request.body = {
  model: "claude-sonnet-4-5-20250929",
  messages: [
    { role: "user", content: "#{prompt}\n\nTranscript: #{transcription_result['text']}" }
  ],
  max_tokens: 1000
}.to_json

llm_gateway_http = Net::HTTP.new(llm_gateway_uri.host, llm_gateway_uri.port)
llm_gateway_http.use_ssl = true
llm_gateway_response = llm_gateway_http.request(llm_gateway_request)
llm_gateway_result = JSON.parse(llm_gateway_response.body)
