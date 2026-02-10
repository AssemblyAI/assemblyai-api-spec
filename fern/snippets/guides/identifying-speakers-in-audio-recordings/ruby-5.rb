transcript_id = response.parsed_response["id"]
polling_endpoint = "https://api.assemblyai.com/v2/transcript/#{transcript_id}"

while true
    polling_response = HTTParty.get(polling_endpoint, headers: headers)
    transcription_result = polling_response.parsed_response

    if transcription_result["status"] == "completed"
        utterances = transcription_result["utterances"]

        # Iterate through each utterance and print the speaker and the text they spoke
        utterances.each do |utterance|
            speaker = utterance["speaker"]
            text = utterance["text"]
            puts "Speaker #{speaker}: #{text}"
        end

        break
    elsif transcription_result["status"] == "error"
        raise "Transcription failed: #{transcription_result["error"]}"
    else
        sleep(3)
    end
end
