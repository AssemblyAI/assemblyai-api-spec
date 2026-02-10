transcript_id = response.parsed_response["id"]
polling_endpoint = "https://api.assemblyai.com/v2/transcript/#{transcript_id}"

while true
    polling_response = HTTParty.get(polling_endpoint, headers: headers)
    transcription_result = polling_response.parsed_response

    if transcription_result["status"] == "completed"
        auto_highlights_result = transcription_result['auto_highlights_result']
        auto_highlights_result['results'].each do |highlight|
            puts "Highlight: #{highlight['text']}, Count: #{highlight['count']}, Rank: #{highlight['rank']}, Timestamps: #{highlight['timestamps'].join(",")}"
        end
        break
    elsif transcription_result["status"] == "error"
        raise "Transcription failed: #{transcription_result["error"]}"
    else
        sleep(3)
    end
end
