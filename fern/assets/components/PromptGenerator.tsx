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

const HELP_ARTICLE_URL = "https://www.assemblyai.com/docs/speech-to-text/pre-recorded-audio/prompt-engineering";

const LLM_CONTEXT = `You are an expert at crafting prompts for AssemblyAI's Universal-3-Pro speech transcription model. Based on the user's transcript sample, analyze the domain and terminology patterns to generate an optimized transcription prompt.

IMPORTANT: Please read the full prompt engineering guide for detailed best practices: ${HELP_ARTICLE_URL}

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
  const [isDarkMode, setIsDarkMode] = React.useState(false);

  React.useEffect(() => {
    const checkDarkMode = () => {
      const html = document.documentElement;
      const body = document.body;
      const isDark = 
        html.classList.contains("dark") ||
        body.classList.contains("dark") ||
        html.getAttribute("data-theme") === "dark" ||
        body.getAttribute("data-theme") === "dark" ||
        window.matchMedia("(prefers-color-scheme: dark)").matches;
      setIsDarkMode(isDark);
    };

    checkDarkMode();

    const observer = new MutationObserver(checkDarkMode);
    observer.observe(document.documentElement, { attributes: true, attributeFilter: ["class", "data-theme"] });
    observer.observe(document.body, { attributes: true, attributeFilter: ["class", "data-theme"] });

    const mediaQuery = window.matchMedia("(prefers-color-scheme: dark)");
    mediaQuery.addEventListener("change", checkDarkMode);

    return () => {
      observer.disconnect();
      mediaQuery.removeEventListener("change", checkDarkMode);
    };
  }, []);

  const buildLLMPrompt = () => {
    const styleLabel = STYLE_LABELS[style];
    const basePrompt = STYLE_PROMPTS[style];
    
    return `${LLM_CONTEXT}

User's selected transcription style: ${styleLabel}
Base prompt for this style:
${basePrompt}

User's transcript sample:
${transcript || "(No transcript provided - generate a general prompt for this style)"}

Please generate an optimized transcription prompt based on the above. Remember to check the help article for additional guidance: ${HELP_ARTICLE_URL}`;
  };

  const openInClaude = () => {
    const prompt = encodeURIComponent(buildLLMPrompt());
    window.open(`https://claude.ai/new?q=${prompt}`, "_blank");
  };

  const openInChatGPT = () => {
    const prompt = encodeURIComponent(buildLLMPrompt());
    window.open(`https://chat.openai.com/?q=${prompt}`, "_blank");
  };

  const openInGemini = () => {
    const prompt = encodeURIComponent(buildLLMPrompt());
    window.open(`https://gemini.google.com/app?q=${prompt}`, "_blank");
  };

  const containerStyle: React.CSSProperties = {
    border: `1px solid ${isDarkMode ? "#374151" : "#e5e7eb"}`,
    borderRadius: "8px",
    padding: "24px",
    backgroundColor: isDarkMode ? "#1f2937" : "#f9fafb",
  };

  const labelStyle: React.CSSProperties = {
    display: "block",
    fontSize: "14px",
    fontWeight: 500,
    marginBottom: "8px",
    color: isDarkMode ? "#f3f4f6" : "#111827",
  };

  const textareaStyle: React.CSSProperties = {
    width: "100%",
    height: "160px",
    padding: "12px",
    border: `1px solid ${isDarkMode ? "#4b5563" : "#d1d5db"}`,
    borderRadius: "6px",
    fontSize: "14px",
    fontFamily: "monospace",
    resize: "vertical",
    backgroundColor: isDarkMode ? "#111827" : "#ffffff",
    color: isDarkMode ? "#f3f4f6" : "#111827",
  };

  const selectStyle: React.CSSProperties = {
    width: "100%",
    padding: "8px",
    border: `1px solid ${isDarkMode ? "#4b5563" : "#d1d5db"}`,
    borderRadius: "6px",
    fontSize: "14px",
    backgroundColor: isDarkMode ? "#111827" : "#ffffff",
    color: isDarkMode ? "#f3f4f6" : "#111827",
  };

  const buttonBaseStyle: React.CSSProperties = {
    display: "inline-flex",
    alignItems: "center",
    gap: "8px",
    padding: "10px 20px",
    border: "none",
    borderRadius: "6px",
    fontSize: "14px",
    fontWeight: 500,
    cursor: "pointer",
    color: "#ffffff",
  };

  const helpTextStyle: React.CSSProperties = {
    marginTop: "12px",
    fontSize: "13px",
    color: isDarkMode ? "#9ca3af" : "#6b7280",
  };

  return (
    <div style={containerStyle}>
      <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
        <div>
          <label style={labelStyle}>
            Paste your transcript sample
          </label>
          <textarea
            value={transcript}
            onChange={(e) => setTranscript(e.target.value)}
            placeholder="Paste a sample of your transcript here (100-500 words recommended). This helps identify your domain and common terminology patterns..."
            style={textareaStyle}
          />
        </div>

        <div>
          <label style={labelStyle}>
            Select transcription style
          </label>
          <select
            value={style}
            onChange={(e) => setStyle(e.target.value as TranscriptionStyle)}
            style={selectStyle}
          >
            {Object.entries(STYLE_LABELS).map(([value, label]) => (
              <option key={value} value={value}>
                {label}
              </option>
            ))}
          </select>
        </div>

        <div style={{ marginTop: "8px" }}>
          <label style={labelStyle}>
            Generate a prompt with AI
          </label>
          <div style={{ display: "flex", gap: "12px", flexWrap: "wrap" }}>
            <button
              onClick={openInClaude}
              style={{
                ...buttonBaseStyle,
                backgroundColor: "#d97706",
              }}
            >
              Open in Claude
            </button>
            <button
              onClick={openInChatGPT}
              style={{
                ...buttonBaseStyle,
                backgroundColor: "#10a37f",
              }}
            >
              Open in ChatGPT
            </button>
            <button
              onClick={openInGemini}
              style={{
                ...buttonBaseStyle,
                backgroundColor: "#4285f4",
              }}
            >
              Open in Gemini
            </button>
          </div>
          <p style={helpTextStyle}>
            Click a button to open your preferred AI assistant with your transcript and style pre-loaded. The AI will generate an optimized prompt based on our prompt engineering guide.
          </p>
        </div>
      </div>
    </div>
  );
}
