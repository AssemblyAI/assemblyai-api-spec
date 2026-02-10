//This function is optional but can be used to format the timestamps from milleseconds to HH:MM:SS
const formatMilliseconds = (milliseconds) => {
  // Calculate hours, minutes, and seconds
  const hours = Math.floor(milliseconds / 3600000);
  const minutes = Math.floor((milliseconds % 3600000) / 60000);
  const seconds = Math.floor((milliseconds % 60000) / 1000);

  // Ensure the values are displayed with leading zeros if needed
  const formattedHours = hours.toString().padStart(2, "0");
  const formattedMinutes = minutes.toString().padStart(2, "0");
  const formattedSeconds = seconds.toString().padStart(2, "0");

  return `${formattedHours}:${formattedMinutes}:${formattedSeconds}`;
};

//Format the final results to contain the sentence, low confidence words, timestamps, and confidence scores.
const finalResults = filterScores.map((res) => {
  return `The following sentence at timestamp ${formatMilliseconds(res.start)} contained low confidence words: ${res.text} \n  Low confidence word(s) from this sentence: ${res.words
    .map((res) => {
      return `${res.text}[score: ${res.confidence}]`;
    })
    .join(", ")}}`;
});

console.log(finalResults);
