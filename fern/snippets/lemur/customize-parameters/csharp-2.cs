var data = new
{
  transcript_ids = transcriptIds,
  prompt = prompt,
  final_model = final_model,
  max_output_size = 1000
};

var content = new StringContent(JsonSerializer.Serialize(data), Encoding.UTF8, "application/json");
using var response = await httpClient.PostAsync("https://api.assemblyai.com/lemur/v3/generate/task", content);
