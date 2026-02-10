const filterScores = filteredSentences.map((item) => {
  return {
    ...item,
    words: item.words.filter((word) => word.confidence < confidenceThreshold),
  };
});
