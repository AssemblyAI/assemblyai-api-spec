var response = (await client.PostAsJsonAsync("https://api.assemblyai.com/v2/realtime/token",
    new { expires_in = 60 })
).Content.ReadAsStringAsync().Result;
var token = JsonConvert.DeserializeObject<dynamic>(response).token;
