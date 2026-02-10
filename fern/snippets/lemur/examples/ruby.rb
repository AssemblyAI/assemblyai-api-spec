require 'net/http'
require 'json'

base_url = "https://api.assemblyai.com"
headers = {
   "authorization" => "<YOUR_API_KEY>",
   "content-type" => "application/json"
}

# Step 1: Transcribe an audio file.
# path = "/my_audio.mp3"
# uri = URI("#{base_url}/v2/upload")
# request = Net::HTTP::Post.new(uri, headers)
# request.body = File.read(path)

# http = Net::HTTP.new(uri.host, uri.port)
# http.use_ssl = true
# upload_response = http.request(request)
# upload_url = JSON.parse(upload_response.body)["upload_url"]

# Or use a publicly-accessible URL:
upload_url = "https://assembly.ai/call.mp4"

uri = URI("#{base_url}/v2/transcript")
request = Net::HTTP::Post.new(uri, headers)
request.body = { audio_url: upload_url }.to_json

response = http.request(request)
transcript_id = JSON.parse(response.body)["id"]
polling_endpoint = "#{base_url}/v2/transcript/#{transcript_id}"

while true
   polling_uri = URI(polling_endpoint)
   polling_request = Net::HTTP::Get.new(polling_uri, headers)
   polling_response = http.request(polling_request)
   transcription_result = JSON.parse(polling_response.body)

   if transcription_result["status"] == "completed"
       break
   elsif transcription_result["status"] == "error"
       raise "Transcription failed: #{transcription_result["error"]}"
   else
       sleep(3)
   end
end

# Step 2: Define your prompt.
prompt = "What was the emotional sentiment of the phone call?"

# Step 3: Apply LeMUR.
lemur_uri = URI("#{base_url}/lemur/v3/generate/task")
lemur_request = Net::HTTP::Post.new(lemur_uri, headers)
lemur_request.body = {
  final_model: "anthropic/claude-sonnet-4-20250514",
  prompt: prompt,
  transcript_ids: [transcript_id]
}.to_json

lemur_response = http.request(lemur_request)
lemur_result = JSON.parse(lemur_response.body)
puts lemur_result["response"]
