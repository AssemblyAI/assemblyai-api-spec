config = aai.TranscriptionConfig(
  summarization=True,
  summary_model=aai.SummarizationModel.informative, # optional
  summary_type=aai.SummarizationType.bullets # optional
)

transcriber = aai.Transcriber(config=config)
