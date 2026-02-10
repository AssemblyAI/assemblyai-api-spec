var data = new
{
  transcript_ids = new List<string> { id1, id2, id3 },
  prompt = prompt,
  final_model = final_model,
};

var content = new StringContent(JsonSerializer.Serialize(data), Encoding.UTF8, "application/json");
using var response = await httpClient.PostAsync("https://api.assemblyai.com/lemur/v3/generate/task", content);
