"use client";
import * as React from "react";

type TranscriptionStyle = "readability" | "readable-disfluencies" | "max-verbatim" | "max-verbatim-audio-tags";

const STYLE_PROMPTS: Record<TranscriptionStyle, string> = {
  "readability": `Transcribe audio verbatim.`,
  "readable-disfluencies": `Transcribe audio verbatim:
- Include all disfluencies`,
  "max-verbatim": `Transcribe verbatim:
- Fillers: yes (um, uh, like, you know)
- Repetitions: yes (I I, the the the)
- Stutters: yes (th-that, b-but)
- False starts: yes (I was- I went)
- Colloquial: yes (gonna, wanna, gotta)`,
  "max-verbatim-audio-tags": `Transcribe verbatim:
- Fillers: yes (um, uh, like, you know)
- Repetitions: yes (I I, the the the)
- Stutters: yes (th-that, b-but)
- False starts: yes (I was- I went)
- Colloquial: yes (gonna, wanna, gotta)
Tag sounds: [laughter], [silence], [noise], [cough], [sigh].`,
};

const STYLE_LABELS: Record<TranscriptionStyle, string> = {
  "readability": "Readability",
  "readable-disfluencies": "Readable with disfluencies",
  "max-verbatim": "Max verbatim",
  "max-verbatim-audio-tags": "Max verbatim with audio tags",
};

export function PromptGenerator() {
  const [transcript, setTranscript] = React.useState("");
  const [style, setStyle] = React.useState<TranscriptionStyle>("readability");
  const [generatedPrompt, setGeneratedPrompt] = React.useState("");
  const [isGenerated, setIsGenerated] = React.useState(false);

  const handleGenerate = () => {
    // For now, generate a sample prompt based on the selected style
    // In the future, this will call an LLM to analyze the transcript
    const basePrompt = STYLE_PROMPTS[style];
    
    let samplePrompt = basePrompt;
    
    // Add a sample domain-specific instruction based on transcript length
    if (transcript.length > 0) {
      samplePrompt += `\n\nNon-negotiable: Accuracy required for domain-specific terminology.`;
      
      // Add example instruction
      samplePrompt += `\n\n[Add your domain-specific corrections here, e.g.: (correct not incorrect, correct2 not incorrect2)]`;
    }
    
    setGeneratedPrompt(samplePrompt);
    setIsGenerated(true);
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(generatedPrompt);
  };

  return (
    <div className="border border-gray-200 rounded-lg p-6 bg-gray-50 dark:bg-gray-900 dark:border-gray-700">
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium mb-2">
            Paste your transcript sample
          </label>
          <textarea
            value={transcript}
            onChange={(e) => setTranscript(e.target.value)}
            placeholder="Paste a sample of your transcript here (100-500 words recommended). This helps identify your domain and common terminology patterns..."
            className="w-full h-40 p-3 border border-gray-300 rounded-md text-sm font-mono resize-y dark:bg-gray-800 dark:border-gray-600 dark:text-gray-100"
          />
        </div>

        <div className="flex flex-wrap gap-4 items-end">
          <div className="flex-1 min-w-[200px]">
            <label className="block text-sm font-medium mb-2">
              Select transcription style
            </label>
            <select
              value={style}
              onChange={(e) => setStyle(e.target.value as TranscriptionStyle)}
              className="w-full p-2 border border-gray-300 rounded-md text-sm dark:bg-gray-800 dark:border-gray-600 dark:text-gray-100"
            >
              {Object.entries(STYLE_LABELS).map(([value, label]) => (
                <option key={value} value={value}>
                  {label}
                </option>
              ))}
            </select>
          </div>

          <button
            onClick={handleGenerate}
            className="px-4 py-2 bg-blue-600 text-white rounded-md text-sm font-medium hover:bg-blue-700 transition-colors"
          >
            Generate Prompt
          </button>
        </div>

        {isGenerated && (
          <div className="mt-4">
            <div className="flex justify-between items-center mb-2">
              <label className="block text-sm font-medium">
                Generated prompt
              </label>
              <button
                onClick={handleCopy}
                className="text-xs text-blue-600 hover:text-blue-800 dark:text-blue-400"
              >
                Copy to clipboard
              </button>
            </div>
            <div className="relative">
              <pre className="w-full p-3 bg-white border border-gray-300 rounded-md text-sm font-mono whitespace-pre-wrap dark:bg-gray-800 dark:border-gray-600 dark:text-gray-100">
                {generatedPrompt}
              </pre>
            </div>
            <p className="mt-2 text-xs text-gray-500 dark:text-gray-400">
              This is a starting point based on your selected style. Customize the prompt by adding domain-specific terminology corrections based on the patterns you observe in your transcripts.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
