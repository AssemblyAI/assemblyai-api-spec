public class Transcript
{
    public string Id { get; set; }
    public string Status { get; set; }
    public string Text { get; set; }

    [JsonPropertyName("language_code")]
    public string LanguageCode { get; set; }

    public string Error { get; set; }
}
