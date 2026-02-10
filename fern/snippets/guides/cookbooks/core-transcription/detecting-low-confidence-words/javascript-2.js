const sentencesWithLowConfidenceWords = (sentences, confidenceThreshold) => {
  return sentences.filter((sentence) => {
    const hasLowConfidenceWord = sentence.words.some(
      (word) => word.confidence < confidenceThreshold
    );
    return hasLowConfidenceWord;
  });
};

const filteredSentences = sentencesWithLowConfidenceWords(
  sentences,
  confidenceThreshold
);
