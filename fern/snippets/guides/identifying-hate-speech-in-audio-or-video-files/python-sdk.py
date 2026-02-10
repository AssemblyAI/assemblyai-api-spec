# Get the parts of the transcript which were flagged as sensitive
for result in transcript.content_safety.results:
  print(result.text)  # sensitive text snippet
  print(result.timestamp.start)
  print(result.timestamp.end)

  for label in result.labels:
    print(label.label)  # content safety category
    print(label.confidence) # model's confidence that the text is in this category
    print(label.severity) # severity of the text in relation to the category

# Get the confidence of the most common labels in relation to the entire audio file
for label, confidence in transcript.content_safety.summary.items():
  print(f"{confidence * 100}% confident that the audio contains {label}")

# Get the overall severity of the most common labels in relation to the entire audio file
for label, severity_confidence in transcript.content_safety.severity_score_summary.items():
  print(f"{severity_confidence.low * 100}% confident that the audio contains low-severity {label}")
  print(f"{severity_confidence.medium * 100}% confident that the audio contains mid-severity {label}")
  print(f"{severity_confidence.high * 100}% confident that the audio contains high-severity {label}")
