const utterancesData = transcriptResult.utterances.map(u => ({
  text: u.text,
  start: u.start,
  end: u.end,
  speaker: u.speaker
}));
