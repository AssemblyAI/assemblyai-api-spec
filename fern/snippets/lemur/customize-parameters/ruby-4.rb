text_with_speaker_labels = ""
transcript["utterances"].each do |utt|
  text_with_speaker_labels += "Speaker #{utt.speaker}:\n#{utt.text}\n"
end

request = Net::HTTP::Post.new("https://api.assemblyai.com/lemur/v3/generate/task", headers)
request.body = {
  prompt: prompt,
  final_model: final_model,
  input_text: text_with_speaker_labels
}.to_json

response = http.request(lemur_request)
