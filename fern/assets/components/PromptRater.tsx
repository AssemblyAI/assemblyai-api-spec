"use client";
import * as React from "react";

const REPAIR_CONTEXT = `You are a Prompt Coach for a SpeechLLM (Speech-to-Text model with a Llama-3.1-8b decoder). Your job is to grade and improve a user-supplied transcription prompt. The model is sensitive to certain "trigger words" that can flip it into different modes (e.g., adding the word "speaker" can cause speaker tags to appear). The user will provide:

INPUTS
1) USER_PROMPT: the exact prompt they plan to send to the SpeechLLM.
2) OBSERVED_BEHAVIOR: what happened (good/bad), e.g. "it inserted [speaker] tags", "proper nouns became phonetic", "hallucinated [MUSIC]", "mixed two people in one sentence", "smoothed words (be→play)", "ended with a comma", "misspelled Calabrio".

YOUR OUTPUT MUST BE ACTIONABLE AND SPECIFIC.
- Identify likely trigger words/phrases in USER_PROMPT.
- Explain what mode they likely trigger and why it matches the observed behavior.
- Recommend minimal changes (prefer small edits over rewrites).
- Provide 2–3 rewritten prompt options tailored to their goal and failure mode.
- Prefer positive, format-defining constraints over "DO NOT" negative prompting.
- Keep prompts short. The SpeechLLM follows short, clear prompts best.
- If OBSERVED_BEHAVIOR includes examples, use them directly in your suggestions.

IMPORTANT MODEL BEHAVIOR ASSUMPTIONS (based on the conversation history)
- Base training heavily reinforces a "default transcription mode" from a simple prompt like "Transcribe this audio."
- SFT adds "mode switches" keyed off certain phrases (some act like control codes).
- Asking for disfluencies/false starts can shift the model toward a more acoustic-literal mode, increasing phonetic spellings for ambiguous proper nouns.
- Asking for "logical sense" / "complete sentences" can cause smoothing/substitution (e.g., be→play) and unwanted "repairs."
- Requests for markers/events can increase bracket-tag hallucinations unless the output format is constrained.
- Turn-taking requests are often entangled with speaker labeling in training; turn prompts can cause [speaker] tags unless format is locked down.

STEP 1 — Classify the user's intent (infer from USER_PROMPT + OBSERVED_BEHAVIOR)
Determine which capabilities they want:
- Context priming (domain)
- Output style (expressive punctuation vs clean)
- Verbatimness (fillers, false starts)
- Proper noun orthography (canonical spellings)
- Multi-language / code-switching
- Non-speech events (music/laughter)
- Turn-taking / diarization (without tags)
- Profanity handling (preserve vs mask)
- Unclear audio handling (unclear tokens)
- Numbers/digits normalization
If unclear, make a best guess from OBSERVED_BEHAVIOR.

STEP 2 — Scan for trigger words and conflicts
Highlight any words/phrases that often flip modes or conflict. Common trigger/conflict patterns:

A) Tag/label triggers (can cause bracket tags or prefixes)
- "speaker", "speaker labels", "diarization", "labels", "tag", "mark", "annotate", "roles", "gender"
Likely outcome: "Speaker 1:" / "[Speaker]" / label bleed, even if the user didn't want tags.

B) Disfluency/raw-mode triggers (can increase phonetic outputs)
- "disfluencies" (strong trigger), "hesitations", "false starts", "verbatim + disfluencies"
Likely outcome: more acoustic-literal choices; ambiguous proper nouns drift to phonetic-looking spellings.

C) Smoothing/repair triggers (can cause substitutions / hallucinated completions)
- "make logical sense", "complete sentences", "fix grammar", "correct mistakes", "clean up"
Likely outcome: word substitutions (be→play), "helpful" rewriting, finishing fragments.

D) Phonetic spelling triggers
- "as spoken" paired with "best spelling from the audio"
Likely outcome: invented phonetic spellings / made-up words under accents.

E) Event marker triggers
- "audio events", "sound effects", "music", "markers", "[MUSIC]"
Likely outcome: bracket markers; sometimes hallucinated markers at the end.

Call out conflicts explicitly, e.g.:
- "verbatim" + "all sentences must make logical sense"
- "preserve rare terms as spoken" + "standard spelling"
- "separate turns" + "no tags" (often entangled)

STEP 3 — Recommend minimal edits (not a full rewrite)
Give the smallest changes that address the failure mode. Use these "safe" rephrasings:

1) To request fillers without triggering raw-mode too hard:
Prefer examples over the keyword "disfluencies":
- "Include spoken fillers like 'um', 'uh', 'you know', 'like' … when clearly spoken."

2) To request canonical spelling without inviting phonetics:
Avoid "as spoken" + "best spelling from audio."
Use:
- "Use standard spelling, including the usual written spelling of recognized names/brands/acronyms."
Optional uncertainty escape hatch:
- "If a name spelling is uncertain, add (?)"

3) To stop smoothing/repairs:
Replace "logical sense / complete sentences" with:
- "Use punctuation and line breaks for readability while keeping the same words."

4) To ensure terminal punctuation without forcing invented completions:
Use a cutoff rule:
- "If speech cuts off or ends mid-utterance, end with — or …"
And:
- "Ensure the transcript ends with a terminal marker (. ! ? … —)"

5) To prevent unwanted speaker tags while still separating turns:
Do not say "speaker." Use "voice" or "different person."
Lock format with positive constraints:
- "Output plain transcript text only."
- "Each line begins with a spoken word."
- "Allowed punctuation: . , ? ! — … ' \\""
(Do not include [ ] or : in allowed punctuation, since they enable tag formats.)

6) If they still get tag bleed, suggest an optional decoding/postprocess knob:
- Optional decode-time ban: block tokens "[", "]", "Speaker", "Spk", ":"
- Optional postprocess: strip leading label patterns if they appear
(Offer as "optional engineering fixes," not required.)

STEP 4 — Produce 2–3 improved prompt options
Always provide:
- Option A: "Minimal patch" (smallest changes)
- Option B: "Stronger format lock" (adds allowed punctuation / line rules)
- Option C: "With context" (adds a single context line if proper nouns are failing)

Keep each prompt short (2–5 lines max). Do not include long checklists.

OUTPUT FORMAT (strict)
Return the following sections, in this order:

1) Quick diagnosis (2–5 bullets)
- What likely caused the failure, tied to prompt phrases.
- Which "mode switch" was triggered.

2) Trigger words found
- List exact phrases from USER_PROMPT that are likely triggers, each with 1-line effect.

3) Conflicts / ambiguity
- Point out any contradictory requirements.

4) Recommended edits (minimal)
- Provide 3–8 concrete edits with before→after wording.

5) Revised prompt options
- Option A (minimal)
- Option B (format-locked)
- Option C (context-primed)
Each option must be copy-pastable.

6) If the user reported a specific example error
- Add a short "How this fix addresses your example" paragraph referencing their example.

CONSTRAINTS
- Do not be generic. Always tie advice back to the user's prompt and observed behavior.
- Do not recommend long prompts.
- Avoid negative prompting ("DO NOT …") unless you also propose a positive-format alternative.
- Prefer "when clearly spoken" to limit hallucinated fillers.
- If you propose markers/tags, specify a minimal, consistent format (otherwise recommend not requesting events).
- If capability is rare/unreliable, label it "YMMV."

Detailed best practices can be found at https://www.assemblyai.com/docs/speech-to-text/pre-recorded-audio/prompt-engineering and this URL should be looked up live for all up to date best practices.`;

const MAX_PROMPT_CHARS = 6000;
const MIN_PROMPT_CHARS = 1000;
const MAX_BEHAVIOR_CHARS = 2000;

const truncateAtSentenceBoundary = (
  text: string,
  maxLength: number
): string => {
  if (text.length <= maxLength) return text;

  const truncated = text.substring(0, maxLength);
  const lastPeriod = truncated.lastIndexOf(".");
  const lastExclamation = truncated.lastIndexOf("!");
  const lastQuestion = truncated.lastIndexOf("?");

  const lastPunctuation = Math.max(lastPeriod, lastExclamation, lastQuestion);

  if (lastPunctuation > 100) {
    return text.substring(0, lastPunctuation + 1);
  }

  return truncated;
};

const truncateAtWordBoundary = (text: string, maxLength: number): string => {
  if (text.length <= maxLength) return text;

  const truncated = text.substring(0, maxLength);
  const lastSpace = truncated.lastIndexOf(" ");

  if (lastSpace > 50) {
    return text.substring(0, lastSpace);
  }

  return truncated;
};

export function PromptRater() {
  const [userPrompt, setUserPrompt] = React.useState("");
  const [observedBehavior, setObservedBehavior] = React.useState("");

  const MAX_URL_LENGTH = 8000;

  const buildRepairPrompt = (maxContentLength?: number) => {
    let promptText = userPrompt || "(No prompt provided)";
    let behaviorText =
      observedBehavior ||
      "(No observed behavior provided - analyze the prompt for potential issues and suggest improvements)";

    if (behaviorText.length > MAX_BEHAVIOR_CHARS) {
      behaviorText =
        truncateAtWordBoundary(behaviorText, MAX_BEHAVIOR_CHARS) +
        "\n\n[Observed behavior truncated to 2000 characters]";
    }

    const behaviorLength = behaviorText.length;

    let promptLimit = MAX_PROMPT_CHARS;
    if (maxContentLength) {
      promptLimit = Math.max(
        MIN_PROMPT_CHARS,
        Math.min(MAX_PROMPT_CHARS, maxContentLength - behaviorLength)
      );
    }

    if (promptText.length > promptLimit) {
      promptText =
        truncateAtSentenceBoundary(promptText, promptLimit) +
        "\n\n[Prompt truncated - provide full prompt directly to the AI if needed]";
    }

    return `${REPAIR_CONTEXT}

USER_PROMPT: ${promptText}

OBSERVED_BEHAVIOR: ${behaviorText}`;
  };

  const getMaxContentLength = (baseUrl: string) => {
    const promptWithoutContent = buildRepairPrompt(0)
      .replace(userPrompt || "(No prompt provided)", "")
      .replace(
        observedBehavior ||
          "(No observed behavior provided - analyze the prompt for potential issues and suggest improvements)",
        ""
      );
    const encodedBaseLength =
      baseUrl.length + encodeURIComponent(promptWithoutContent).length;
    const availableLength = MAX_URL_LENGTH - encodedBaseLength;
    return Math.floor(availableLength / 3);
  };

  const openInClaude = () => {
    const baseUrl = "https://claude.ai/new?q=";
    const maxLength = getMaxContentLength(baseUrl);
    const prompt = encodeURIComponent(buildRepairPrompt(maxLength));
    window.open(`${baseUrl}${prompt}`, "_blank");
  };

  const openInChatGPT = () => {
    const baseUrl = "https://chat.openai.com/?q=";
    const maxLength = getMaxContentLength(baseUrl);
    const prompt = encodeURIComponent(buildRepairPrompt(maxLength));
    window.open(`${baseUrl}${prompt}`, "_blank");
  };

  const openInGemini = () => {
    const baseUrl = "https://aistudio.google.com/prompts/new_chat?prompt=";
    const maxLength = getMaxContentLength(baseUrl);
    const prompt = encodeURIComponent(buildRepairPrompt(maxLength));
    window.open(`${baseUrl}${prompt}`, "_blank");
  };

  const containerStyle: React.CSSProperties = {
    border: "1px solid var(--grayscale-a4, #e5e7eb)",
    borderRadius: "8px",
    padding: "24px",
    backgroundColor: "var(--grayscale-2, #f9fafb)",
  };

  const labelStyle: React.CSSProperties = {
    display: "block",
    fontSize: "14px",
    fontWeight: 500,
    marginBottom: "8px",
    color: "var(--grayscale-12, #111827)",
  };

  const textareaStyle: React.CSSProperties = {
    width: "100%",
    height: "160px",
    padding: "12px",
    border: "1px solid var(--grayscale-a4, #d1d5db)",
    borderRadius: "6px",
    fontSize: "14px",
    fontFamily: "monospace",
    resize: "vertical",
    backgroundColor: "var(--grayscale-1, #ffffff)",
    color: "var(--grayscale-12, #111827)",
  };

  const charCountStyle: React.CSSProperties = {
    fontSize: "12px",
    color: "var(--grayscale-11, #6b7280)",
    marginTop: "4px",
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
    color: "var(--grayscale-11, #6b7280)",
  };

  return (
    <div style={containerStyle}>
      <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
        <div>
          <label style={labelStyle}>Paste your current prompt</label>
          <textarea
            value={userPrompt}
            onChange={(e) => setUserPrompt(e.target.value)}
            placeholder="Paste the exact prompt you're sending to Universal-3-Pro..."
            style={textareaStyle}
          />
          <div style={charCountStyle}>
            {userPrompt.length > 0 &&
              `${userPrompt.length.toLocaleString()} / ${MAX_PROMPT_CHARS.toLocaleString()} characters`}
            {userPrompt.length > MAX_PROMPT_CHARS && " - will be truncated"}
          </div>
        </div>

        <div>
          <label style={labelStyle}>Describe the issues you observed</label>
          <textarea
            value={observedBehavior}
            onChange={(e) => setObservedBehavior(e.target.value)}
            placeholder='Describe what went wrong, e.g. "it inserted [speaker] tags", "hallucinated [MUSIC]", "proper nouns became phonetic", "misspelled Calabrio", "smoothed words (be→play)"...'
            style={{ ...textareaStyle, height: "120px" }}
          />
          <div style={charCountStyle}>
            {observedBehavior.length > 0 &&
              `${observedBehavior.length.toLocaleString()} / ${MAX_BEHAVIOR_CHARS.toLocaleString()} characters`}
            {observedBehavior.length > MAX_BEHAVIOR_CHARS &&
              " - will be truncated"}
          </div>
        </div>

        <div style={{ marginTop: "8px" }}>
          <label style={labelStyle}>Diagnose and repair with AI</label>
          <div style={{ display: "flex", gap: "12px", flexWrap: "wrap" }}>
            <button
              onClick={openInClaude}
              style={{
                ...buttonBaseStyle,
                backgroundColor: "#d97706",
              }}
            >
              <svg
                width="16"
                height="16"
                viewBox="0 0 16 17"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  fillRule="evenodd"
                  clipRule="evenodd"
                  d="M9.218 2.52954H11.62L16 13.5162H13.598L9.218 2.52954ZM4.37933 2.52954H6.89067L11.2707 13.5162H8.82133L7.926 11.2089H3.34467L2.44867 13.5155H0L4.38 2.53087L4.37933 2.52954ZM7.134 9.16887L5.63533 5.30754L4.13667 9.16954H7.13333L7.134 9.16887Z"
                  fill="currentColor"
                />
              </svg>
              Open in Claude
            </button>
            <button
              onClick={openInChatGPT}
              style={{
                ...buttonBaseStyle,
                backgroundColor: "#10a37f",
              }}
            >
              <svg
                width="16"
                height="16"
                viewBox="0 0 24 24"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <g clipPath="url(#clip0_openai_repair)">
                  <path
                    d="M22.0606 9.86697C22.6034 8.23781 22.4165 6.45314 21.5485 4.97127C20.2431 2.69837 17.6188 1.52902 15.0558 2.0793C13.9156 0.794818 12.2774 0.0643507 10.5601 0.074818C7.94025 0.0688367 5.61576 1.75557 4.80978 4.24828C3.12679 4.59295 1.67408 5.64641 0.823986 7.13949C-0.491154 9.40641 -0.191341 12.264 1.56567 14.2079C1.02286 15.8371 1.20978 17.6217 2.07782 19.1036C3.38324 21.3765 6.00754 22.5458 8.57053 21.9956C9.70997 23.2801 11.3488 24.0105 13.0662 23.9993C15.6875 24.006 18.0128 22.3178 18.8188 19.8229C20.5017 19.4782 21.9545 18.4247 22.8045 16.9316C24.1182 14.6647 23.8176 11.8094 22.0614 9.86547L22.0606 9.86697ZM13.0677 22.4359C12.0188 22.4374 11.0027 22.0703 10.1974 21.3982C10.2341 21.3787 10.2976 21.3436 10.3388 21.3182L15.1029 18.5668C15.3466 18.4285 15.4961 18.169 15.4946 17.8886V11.1724L17.5081 12.335C17.5298 12.3455 17.544 12.3664 17.547 12.3903V17.9522C17.544 20.4255 15.541 22.4307 13.0677 22.4359ZM3.43483 18.3215C2.90922 17.4139 2.72006 16.35 2.90025 15.3174C2.93539 15.3384 2.99744 15.3765 3.04156 15.4019L7.80567 18.1533C8.04716 18.2946 8.34623 18.2946 8.58847 18.1533L14.4045 14.7948V17.1201C14.406 17.144 14.3948 17.1672 14.3761 17.1821L9.56044 19.9627C7.41539 21.1978 4.67595 20.4636 3.43558 18.3215H3.43483ZM2.181 7.92229C2.70436 7.01314 3.53053 6.31781 4.51445 5.95669C4.51445 5.99781 4.51221 6.07033 4.51221 6.12117V11.6247C4.51072 11.9043 4.66025 12.1638 4.90324 12.3021L10.7193 15.6599L8.70586 16.8225C8.68567 16.8359 8.66025 16.8382 8.63782 16.8285L3.82137 14.0457C1.68081 12.806 0.946603 10.0673 2.18025 7.92304L2.181 7.92229ZM18.7238 11.772L12.9077 8.41351L14.9212 7.25164C14.9414 7.23818 14.9668 7.23594 14.9892 7.24566L19.8057 10.0262C21.95 11.2651 22.6849 14.0083 21.446 16.1526C20.9219 17.0602 20.0965 17.7556 19.1133 18.1174V12.4494C19.1156 12.1698 18.9668 11.9111 18.7245 11.772H18.7238ZM20.7275 8.75594C20.6924 8.73426 20.6303 8.69687 20.5862 8.67145L15.8221 5.92005C15.5806 5.77874 15.2816 5.77874 15.0393 5.92005L9.22324 9.27856V6.95332C9.22174 6.9294 9.23296 6.90622 9.25165 6.89127L14.0674 4.11295C16.2124 2.87557 18.9548 3.61201 20.1915 5.75781C20.7141 6.66398 20.9032 7.72491 20.726 8.75594H20.7275ZM8.12866 12.9002L6.11445 11.7376C6.09277 11.7272 6.07857 11.7062 6.07558 11.6823V6.12043C6.07707 3.64416 8.08604 1.63743 10.5623 1.63893C11.6098 1.63893 12.6236 2.00678 13.4288 2.67669C13.3922 2.69613 13.3294 2.73127 13.2875 2.75669L8.52343 5.50809C8.27969 5.64641 8.13016 5.9051 8.13165 6.18547L8.12866 12.8987V12.9002ZM9.22249 10.5421L11.8131 9.04603L14.4038 10.5414V13.5328L11.8131 15.0281L9.22249 13.5328V10.5421Z"
                    fill="currentColor"
                  />
                </g>
                <defs>
                  <clipPath id="clip0_openai_repair">
                    <rect width="23.6262" height="24" fill="currentColor" />
                  </clipPath>
                </defs>
              </svg>
              Open in ChatGPT
            </button>
            <button
              onClick={openInGemini}
              style={{
                ...buttonBaseStyle,
                backgroundColor: "#4285f4",
              }}
            >
              <svg
                width="16"
                height="16"
                viewBox="0 0 16 17"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M8 16.5C8 12.634 11.134 9.5 15 9.5V8.5C11.134 8.5 8 5.366 8 1.5C8 5.366 4.866 8.5 1 8.5V9.5C4.866 9.5 8 12.634 8 16.5Z"
                  fill="currentColor"
                />
              </svg>
              Open in Gemini
            </button>
          </div>
          <p style={helpTextStyle}>
            Click a button to open your preferred AI assistant with your prompt
            and observed issues pre-loaded. The AI will diagnose trigger words,
            identify conflicts, and suggest minimal edits with 2-3 revised prompt
            options.
          </p>
        </div>
      </div>
    </div>
  );
}
