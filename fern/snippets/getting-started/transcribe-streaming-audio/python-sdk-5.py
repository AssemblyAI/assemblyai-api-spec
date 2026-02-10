    try:
        client.stream(
          aai.extras.MicrophoneStream(sample_rate=16000)
        )
