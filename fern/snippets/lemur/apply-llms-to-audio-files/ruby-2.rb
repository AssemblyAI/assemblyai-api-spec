require 'net/http'
require 'json'

base_url = "https://api.assemblyai.com"
headers = {
   "authorization" => "<YOUR_API_KEY>",
   "content-type" => "application/json"
}

path = "/my_audio.mp3"
uri = URI("#{base_url}/v2/upload")
request = Net::HTTP::Post.new(uri, headers)
request.body = File.read(path)

http = Net::HTTP.new(uri.host, uri.port)
http.use_ssl = true
upload_response = http.request(request)
upload_url = JSON.parse(upload_response.body)["upload_url"]

uri = URI("#{base_url}/v2/transcript")
request = Net::HTTP::Post.new(uri, headers)
request.body = { audio_url: upload_url }.to_json # You can also replace upload_url with an audio file URL

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
