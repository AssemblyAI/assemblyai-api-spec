string textWithSpeakerLabels = "";
foreach (var utt in transcript.utterances)
{
  textWithSpeakerLabels += $"Speaker {utt.speaker}:\n{utt.text}\n";
}

var data = new
{
  prompt,
  final_model = final_model,
  input_text = textWithSpeakerLabels
};

var content = new StringContent(JsonSerializer.Serialize(data), Encoding.UTF8, "application/json");
using var response = await httpClient.PostAsync("https://api.assemblyai.com/lemur/v3/generate/task", content);
