transcript_id = response.parsed_response["id"]
polling_endpoint = "https://api.assemblyai.com/v2/transcript/#{transcript_id}"

while true
    polling_response = HTTParty.get(polling_endpoint, headers: headers)
    transcription_result = polling_response.parsed_response

    if transcription_result["status"] == "completed"
        content_safety_labels = transcription_result['content_safety_labels']

        # Uncomment the next line to print everything
        # puts content_safety_labels

        content_safety_labels.each do |label|
            # The severity score measures how severe the flagged content is on a scale of 0-1, with 1 being the most severe.
            if label['name'] == 'hate_speech' && label['severity'] >= 0.5
                puts "Hate speech detected with severity score: #{label['severity']}"
                # Do something with this information, such as flagging the transcription for review
            end
        end
        break
    elsif transcription_result["status"] == "error"
        raise "Transcription failed: #{transcription_result["error"]}"
    else
        sleep(3)
    end
end
