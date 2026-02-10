transcript_id = response.parsed_response["id"]
polling_endpoint = "https://api.assemblyai.com/v2/transcript/#{transcript_id}"

while true
    polling_response = HTTParty.get(polling_endpoint, headers: headers)
    transcription_result = polling_response.parsed_response

    if transcription_result["status"] == "completed"
        # Print each auto chapter
        transcription_result["auto_chapters"].each do |chapter|
            puts "Chapter Start Time: #{chapter["start"]}"
            puts "Chapter End Time: #{chapter["end"]}"
            puts "Chapter Headline: #{chapter["headline"]}"
            puts "Chapter Gist: #{chapter["gist"]}"
            puts "Chapter Summary: #{chapter["summary"]}"
        end
        break
    elsif transcription_result["status"] == "error"
        raise "Transcription failed: #{transcription_result["error"]}"
    else
        sleep(3)
    end
end
