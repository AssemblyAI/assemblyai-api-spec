  var data = new
  {
      audio_url = audioUrl,
      sentiment_analysis = true,
      speaker_labels = true
  };

// ...

  foreach (var result in transcript.SentimentAnalysisResults)
  {
      Console.WriteLine($"Speaker: {result.Speaker}");
  }

// ...
    public class SentimentAnalysisResult
    {
        [JsonPropertyName("text")]
        public string Text { get; set; }

        [JsonPropertyName("sentiment")]
        public string Sentiment { get; set; }

        [JsonPropertyName("confidence")]
        public double Confidence { get; set; }

        [JsonPropertyName("start")]
        public int Start { get; set; }

        [JsonPropertyName("end")]
        public int End { get; set; }

        [JsonPropertyName("speaker")]
        public string Speaker { get; set; }
    }
