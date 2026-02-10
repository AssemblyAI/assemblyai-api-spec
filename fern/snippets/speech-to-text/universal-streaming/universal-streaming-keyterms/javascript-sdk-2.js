// Replace or establish new set of keyterms
transcriber.updateConfiguration({ keytermsPrompt: ["Universal-3"] });

// Remove keyterms and reset context biasing
transcriber.updateConfiguration({ keytermsPrompt: [] });
