transcriber = aai.RealtimeTranscriber(
    ...,
    end_utterance_silence_threshold=500
)

# after connecting
transcriber.configure_end_utterance_silence_threshold(300)
