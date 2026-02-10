require 'net/http'

def get_transcript_file(transcript_id, file_format)
  raise "Unsupported file format: #{file_format}. Please specify 'srt' or 'vtt'." unless ['srt', 'vtt'].include?(file_format)

  url = URI.parse("https://api.assemblyai.com/v2/transcript/#{transcript_id}/#{file_format}")

  http = Net::HTTP.new(url.host, url.port)
  http.use_ssl = true

  response = http.get(url.path, headers)
  if response.code.to_i == 200
    response.body
  else
    raise "Failed to retrieve #{file_format} file: #{response.code} #{response.message}"
  end
end

subtitles_text = get_transcript_file(transcript_id, "vtt")  # or "srt"
puts subtitles_text
