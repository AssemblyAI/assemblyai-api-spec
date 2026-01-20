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

const LLM_CONTEXT = `You are an expert at crafting prompts for AssemblyAI's Universal-3-Pro speech transcription model. Based on the user's transcript sample, analyze the domain and terminology patterns to generate an optimized transcription prompt.

Key principles for effective prompts:
1. Use authoritative language: "Non-negotiable:", "Mandatory:", "Strict requirement:"
2. Include explicit examples in format: (correct not incorrect)
3. Keep prompts concise: 3-5 instructions, 50-80 words
4. Show error patterns the model should fix (vowel substitution, sound-alike confusion, etc.)

Generate a prompt that follows this structure:
[Base instruction based on style]
[Authoritative language] + [Specific instruction] + [2-3 explicit examples]

Analyze the transcript for domain-specific terminology that might be misheard and include corrections.`;

export function PromptGenerator() {
  const [transcript, setTranscript] = React.useState("");
  const [style, setStyle] = React.useState<TranscriptionStyle>("readability");
  const [generatedPrompt, setGeneratedPrompt] = React.useState("");
  const [isGenerated, setIsGenerated] = React.useState(false);
  const [copied, setCopied] = React.useState(false);

  const handleGenerate = () => {
    const basePrompt = STYLE_PROMPTS[style];
    
    let samplePrompt = basePrompt;
    
    if (transcript.length > 0) {
      samplePrompt += `\n\nNon-negotiable: Accuracy required for domain-specific terminology.`;
      samplePrompt += `\n\n[Add your domain-specific corrections here, e.g.: (correct not incorrect, correct2 not incorrect2)]`;
    }
    
    setGeneratedPrompt(samplePrompt);
    setIsGenerated(true);
    setCopied(false);
  };

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(generatedPrompt);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      const textArea = document.createElement("textarea");
      textArea.value = generatedPrompt;
      document.body.appendChild(textArea);
      textArea.select();
      document.execCommand("copy");
      document.body.removeChild(textArea);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const buildLLMPrompt = () => {
    const styleLabel = STYLE_LABELS[style];
    const basePrompt = STYLE_PROMPTS[style];
    
    return `${LLM_CONTEXT}

User's selected transcription style: ${styleLabel}
Base prompt for this style:
${basePrompt}

User's transcript sample:
${transcript || "(No transcript provided - generate a general prompt for this style)"}

Please generate an optimized transcription prompt based on the above.`;
  };

  const openInClaude = () => {
    const prompt = encodeURIComponent(buildLLMPrompt());
    window.open(`https://claude.ai/new?q=${prompt}`, "_blank");
  };

  const openInChatGPT = () => {
    const prompt = encodeURIComponent(buildLLMPrompt());
    window.open(`https://chat.openai.com/?q=${prompt}`, "_blank");
  };

  return (
    <div style={{ border: "1px solid var(--border-color, #e5e7eb)", borderRadius: "8px", padding: "24px", backgroundColor: "var(--bg-secondary, #f9fafb)" }}>
      <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
        <div>
          <label style={{ display: "block", fontSize: "14px", fontWeight: 500, marginBottom: "8px" }}>
            Paste your transcript sample
          </label>
          <textarea
            value={transcript}
            onChange={(e) => setTranscript(e.target.value)}
            placeholder="Paste a sample of your transcript here (100-500 words recommended). This helps identify your domain and common terminology patterns..."
            style={{
              width: "100%",
              height: "160px",
              padding: "12px",
              border: "1px solid var(--border-color, #d1d5db)",
              borderRadius: "6px",
              fontSize: "14px",
              fontFamily: "monospace",
              resize: "vertical",
              backgroundColor: "var(--bg-primary, #ffffff)",
              color: "var(--text-primary, #111827)",
            }}
          />
        </div>

        <div style={{ display: "flex", flexWrap: "wrap", gap: "16px", alignItems: "flex-end" }}>
          <div style={{ flex: 1, minWidth: "200px" }}>
            <label style={{ display: "block", fontSize: "14px", fontWeight: 500, marginBottom: "8px" }}>
              Select transcription style
            </label>
            <select
              value={style}
              onChange={(e) => setStyle(e.target.value as TranscriptionStyle)}
              style={{
                width: "100%",
                padding: "8px",
                border: "1px solid var(--border-color, #d1d5db)",
                borderRadius: "6px",
                fontSize: "14px",
                backgroundColor: "var(--bg-primary, #ffffff)",
                color: "var(--text-primary, #111827)",
              }}
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
            style={{
              padding: "8px 16px",
              backgroundColor: "#2563eb",
              color: "#ffffff",
              border: "none",
              borderRadius: "6px",
              fontSize: "14px",
              fontWeight: 500,
              cursor: "pointer",
            }}
          >
            Generate Prompt
          </button>
        </div>

        {isGenerated && (
          <div style={{ marginTop: "16px" }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "8px" }}>
              <label style={{ fontSize: "14px", fontWeight: 500 }}>
                Generated prompt
              </label>
              <button
                onClick={handleCopy}
                style={{
                  fontSize: "12px",
                  color: "#2563eb",
                  background: "none",
                  border: "none",
                  cursor: "pointer",
                  textDecoration: "underline",
                }}
              >
                {copied ? "Copied!" : "Copy to clipboard"}
              </button>
            </div>
            <pre style={{
              width: "100%",
              padding: "12px",
              backgroundColor: "#1f2937",
              border: "1px solid #374151",
              borderRadius: "6px",
              fontSize: "14px",
              fontFamily: "monospace",
              whiteSpace: "pre-wrap",
              color: "#f3f4f6",
              margin: 0,
            }}>
              {generatedPrompt}
            </pre>
            <p style={{ marginTop: "8px", fontSize: "12px", color: "var(--text-secondary, #6b7280)" }}>
              This is a starting point based on your selected style. Customize the prompt by adding domain-specific terminology corrections based on the patterns you observe in your transcripts.
            </p>
            
            <div style={{ marginTop: "16px", display: "flex", gap: "12px", flexWrap: "wrap" }}>
              <button
                onClick={openInClaude}
                style={{
                  display: "inline-flex",
                  alignItems: "center",
                  gap: "8px",
                  padding: "8px 16px",
                  backgroundColor: "#d97706",
                  color: "#ffffff",
                  border: "none",
                  borderRadius: "6px",
                  fontSize: "14px",
                  fontWeight: 500,
                  cursor: "pointer",
                }}
              >
                Open in Claude
              </button>
              <button
                onClick={openInChatGPT}
                style={{
                  display: "inline-flex",
                  alignItems: "center",
                  gap: "8px",
                  padding: "8px 16px",
                  backgroundColor: "#10a37f",
                  color: "#ffffff",
                  border: "none",
                  borderRadius: "6px",
                  fontSize: "14px",
                  fontWeight: 500,
                  cursor: "pointer",
                }}
              >
                Open in ChatGPT
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
