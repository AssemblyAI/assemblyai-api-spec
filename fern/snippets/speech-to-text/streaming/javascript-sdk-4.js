const rt = client.realtime.transcriber({
  ...,
  endUtteranceSilenceThreshold: 500
})

// after connecting
rt.configureEndUtteranceSilenceThreshold(300)
