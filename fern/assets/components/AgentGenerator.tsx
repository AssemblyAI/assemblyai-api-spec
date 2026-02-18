"use client";
import * as React from "react";

const DOCS_URL =
  "https://www.assemblyai.com/docs/speech-to-text/voice-agents/speechtospeech";

type OutputFormat = "python" | "javascript" | "config";

const LLM_CONTEXT = `You are an expert at building real-time voice agents using the AssemblyAI Speech-to-Speech API. Based on the user's description, generate a complete voice agent implementation.

## AssemblyAI Speech-to-Speech API Reference

Endpoint: wss://speech-to-speech.assemblyai.com/v1/realtime
Auth: Authorization: Bearer YOUR_ASSEMBLYAI_API_KEY header on WebSocket connect
Audio: PCM16 (signed 16-bit little-endian), mono, 24000 Hz, base64-encoded in JSON
Voices: sage (default), ember, breeze, cascade

### Session config (flat format, for raw WebSocket):
{
  "type": "session.update",
  "session": {
    "instructions": "System prompt here",
    "voice": "sage",
    "input_audio_format": "pcm16",
    "input_audio_sample_rate": 24000,
    "output_audio_format": "pcm16",
    "output_audio_sample_rate": 24000,
    "input_audio_transcription": {"model": "universal-streaming"},
    "output_modalities": ["audio", "text"],
    "turn_detection": {"type": "server_vad", "threshold": 0.5, "prefix_padding_ms": 300, "silence_duration_ms": 200},
    "tools": [],
    "tool_choice": "auto"
  }
}

### Tool definition schema:
{
  "type": "function",
  "name": "tool_name",
  "description": "What this tool does",
  "parameters": {
    "type": "object",
    "properties": {
      "param_name": {"type": "string", "description": "Param description"}
    },
    "required": ["param_name"]
  }
}

### Tool calling pattern:
- On "response.function_call_arguments.done": Start executing the function immediately (use asyncio.create_task)
- On "response.done": Send results back via "conversation.item.create" with type "function_call_output"
- Do NOT send "response.create" after tool results — the server continues automatically
- Interruptions are handled automatically by server-side VAD — no client logic needed

### Key events:
Client sends: session.update, input_audio_buffer.append (base64 audio)
Server sends: session.created, input_audio_buffer.speech_started, input_audio_buffer.speech_stopped, conversation.item.input_audio_transcription.completed, response.output_audio.delta (base64 audio), response.output_audio_transcript.done, response.function_call_arguments.done, response.done

### Python quickstart template (raw WebSocket with websockets + sounddevice):
\`\`\`python
import asyncio, base64, json, threading, time
import sounddevice as sd
import websockets

API_KEY = "YOUR_ASSEMBLYAI_API_KEY"
WS_URL = "wss://speech-to-speech.assemblyai.com/v1/realtime"
SAMPLE_RATE = 24000

TOOLS = []  # Add tool definitions here

async def run_tool(name, args):
    # Implement tool logic here
    return {"error": f"Unknown tool: {name}"}

class AudioPlayer:
    def __init__(self):
        self._buf = bytearray()
        self._lock = threading.Lock()
        self._out = sd.RawOutputStream(samplerate=SAMPLE_RATE, channels=1, dtype="int16", blocksize=480, latency="low")
        self._out.start()
    def play(self, pcm):
        with self._lock:
            self._buf.extend(pcm)
            while len(self._buf) >= 960:
                self._out.write(bytes(self._buf[:960]))
                del self._buf[:960]
    def close(self):
        self._out.stop(); self._out.close()

async def main():
    player = AudioPlayer()
    q = asyncio.Queue()
    def mic_cb(data, frames, ti, status):
        q.put_nowait(bytes(data))
    mic = sd.RawInputStream(samplerate=SAMPLE_RATE, channels=1, dtype="int16", blocksize=480, callback=mic_cb, latency="low")
    mic.start()

    ws = await websockets.connect(WS_URL, additional_headers={"Authorization": f"Bearer {API_KEY}"})
    await ws.send(json.dumps({"type": "session.update", "session": {
        "input_audio_format": "pcm16", "input_audio_sample_rate": SAMPLE_RATE,
        "output_audio_format": "pcm16", "output_audio_sample_rate": SAMPLE_RATE,
        "input_audio_transcription": {"model": "universal-streaming"},
        "turn_detection": {"type": "server_vad", "threshold": 0.5, "prefix_padding_ms": 300, "silence_duration_ms": 200},
        "output_modalities": ["audio", "text"],
        "instructions": "SYSTEM_PROMPT_HERE",
        "voice": "sage",
        "tools": TOOLS,
        "tool_choice": "auto",
    }}))
    pending_tasks = {}
    async def stream_mic():
        while True:
            try:
                pcm = await asyncio.wait_for(q.get(), timeout=0.1)
                await ws.send(json.dumps({"type": "input_audio_buffer.append", "audio": base64.b64encode(pcm).decode()}))
            except asyncio.TimeoutError:
                pass
    async def handle_events():
        async for raw in ws:
            e = json.loads(raw)
            et = e.get("type", "")
            t = time.strftime("%H:%M:%S")
            if et == "session.created":
                print(f"[{t}] Connected — session {e['session']['id']}")
            elif et == "conversation.item.input_audio_transcription.completed":
                print(f"[{t}] You:   {e.get('transcript', '')}")
            elif et == "response.output_audio.delta":
                player.play(base64.b64decode(e["delta"]))
            elif et == "response.output_audio_transcript.done":
                print(f"[{t}] Agent: {e.get('transcript', '')}")
            elif et == "response.function_call_arguments.done":
                args = json.loads(e["arguments"])
                pending_tasks[e["call_id"]] = asyncio.create_task(run_tool(e["name"], args))
                print(f"[{t}] Tool:  {e['name']}({e['arguments']})")
            elif et == "response.done":
                if pending_tasks and e.get("response", {}).get("status") == "completed":
                    for cid, task in pending_tasks.items():
                        result = await task
                        await ws.send(json.dumps({"type": "conversation.item.create", "item": {"type": "function_call_output", "call_id": cid, "output": json.dumps(result)}}))
                    pending_tasks.clear()
    print("Listening — start talking.\\n")
    try:
        await asyncio.gather(stream_mic(), handle_events())
    except KeyboardInterrupt:
        pass
    finally:
        mic.stop(); mic.close(); player.close(); await ws.close()

if __name__ == "__main__":
    asyncio.run(main())
\`\`\`

### JavaScript quickstart template (raw WebSocket in Node.js):
\`\`\`javascript
// Requires: npm install ws
const WebSocket = require("ws");
const API_KEY = "YOUR_ASSEMBLYAI_API_KEY";
const WS_URL = "wss://speech-to-speech.assemblyai.com/v1/realtime";

const TOOLS = [];  // Add tool definitions here

function runTool(name, args) {
  // Implement tool logic here
  return { error: "Unknown tool: " + name };
}

const ws = new WebSocket(WS_URL, { headers: { Authorization: "Bearer " + API_KEY } });
const pendingTasks = new Map();

ws.on("open", () => {
  ws.send(JSON.stringify({ type: "session.update", session: {
    input_audio_format: "pcm16", input_audio_sample_rate: 24000,
    output_audio_format: "pcm16", output_audio_sample_rate: 24000,
    input_audio_transcription: { model: "universal-streaming" },
    turn_detection: { type: "server_vad", threshold: 0.5, prefix_padding_ms: 300, silence_duration_ms: 200 },
    output_modalities: ["audio", "text"],
    instructions: "SYSTEM_PROMPT_HERE",
    voice: "sage",
    tools: TOOLS,
    tool_choice: "auto",
  }}));
  // Start streaming mic audio as base64 PCM16 via input_audio_buffer.append
});

ws.on("message", async (raw) => {
  const e = JSON.parse(raw);
  if (e.type === "response.output_audio.delta") {
    // Play base64-decoded PCM16 audio: Buffer.from(e.delta, "base64")
  } else if (e.type === "response.output_audio_transcript.done") {
    console.log("Agent:", e.transcript);
  } else if (e.type === "response.function_call_arguments.done") {
    pendingTasks.set(e.call_id, runTool(e.name, JSON.parse(e.arguments)));
  } else if (e.type === "response.done" && pendingTasks.size > 0) {
    for (const [callId, resultPromise] of pendingTasks) {
      const result = await resultPromise;
      ws.send(JSON.stringify({ type: "conversation.item.create", item: { type: "function_call_output", call_id: callId, output: JSON.stringify(result) } }));
    }
    pendingTasks.clear();
  }
});
\`\`\`

Full documentation: ${DOCS_URL}`;

const FORMAT_INSTRUCTIONS: Record<OutputFormat, string> = {
  python: `Generate a COMPLETE, RUNNABLE Python script using the raw WebSocket template above. Include:
1. A detailed system prompt in the instructions field tailored to the agent's purpose
2. All tool definitions in the TOOLS array with proper JSON schemas
3. Full run_tool() implementation with realistic mock data for each tool
4. All imports, the AudioPlayer class, mic handling, and event loop — everything needed to pip install and run
Choose an appropriate voice from: sage, ember, breeze, cascade.`,

  javascript: `Generate a COMPLETE, RUNNABLE JavaScript/Node.js script using the JS WebSocket template above. Include:
1. A detailed system prompt in the instructions field tailored to the agent's purpose
2. All tool definitions in the TOOLS array with proper JSON schemas
3. Full runTool() implementation with realistic mock data for each tool
4. All requires, WebSocket setup, and event handling — everything needed to npm install and run
Choose an appropriate voice from: sage, ember, breeze, cascade.
For audio I/O, use a comment placeholder since Node.js audio libraries vary.`,

  config: `Generate ONLY the session configuration JSON (the session.update payload) with:
1. A detailed system prompt in the instructions field tailored to the agent's purpose
2. All tool definitions in the tools array with proper JSON schemas
3. An appropriate voice chosen from: sage, ember, breeze, cascade
4. All audio format and turn detection settings filled in
Output ONLY the JSON — no script wrapper.`,
};

const MAX_DESCRIPTION_CHARS = 2000;
const MAX_URL_LENGTH = 8000;

const truncateAtWordBoundary = (text: string, maxLength: number): string => {
  if (text.length <= maxLength) return text;
  const truncated = text.substring(0, maxLength);
  const lastSpace = truncated.lastIndexOf(" ");
  if (lastSpace > 50) return text.substring(0, lastSpace);
  return truncated;
};

export function AgentGenerator() {
  const [description, setDescription] = React.useState("");
  const [format, setFormat] = React.useState<OutputFormat>("python");

  const buildPrompt = (maxContentLength?: number) => {
    let descText = description || "(No description provided — generate a general-purpose helpful voice assistant)";

    if (descText.length > MAX_DESCRIPTION_CHARS) {
      descText = truncateAtWordBoundary(descText, MAX_DESCRIPTION_CHARS) + "\n\n[Description truncated]";
    }

    if (maxContentLength && descText.length > maxContentLength) {
      descText = truncateAtWordBoundary(descText, maxContentLength) + "\n\n[Description truncated]";
    }

    return `${LLM_CONTEXT}

## Output format
${FORMAT_INSTRUCTIONS[format]}

## User's agent description
${descText}`;
  };

  const getMaxContentLength = (baseUrl: string) => {
    const promptWithoutDesc = buildPrompt(0).replace(
      description || "(No description provided — generate a general-purpose helpful voice assistant)",
      ""
    );
    const encodedBaseLength = baseUrl.length + encodeURIComponent(promptWithoutDesc).length;
    const available = MAX_URL_LENGTH - encodedBaseLength;
    return Math.floor(available / 3);
  };

  const openInClaude = () => {
    const baseUrl = "https://claude.ai/new?q=";
    const maxLen = getMaxContentLength(baseUrl);
    const prompt = encodeURIComponent(buildPrompt(maxLen));
    window.open(`${baseUrl}${prompt}`, "_blank");
  };

  const openInChatGPT = () => {
    const baseUrl = "https://chat.openai.com/?q=";
    const maxLen = getMaxContentLength(baseUrl);
    const prompt = encodeURIComponent(buildPrompt(maxLen));
    window.open(`${baseUrl}${prompt}`, "_blank");
  };

  const openInGemini = () => {
    const baseUrl = "https://aistudio.google.com/prompts/new_chat?prompt=";
    const maxLen = getMaxContentLength(baseUrl);
    const prompt = encodeURIComponent(buildPrompt(maxLen));
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
    height: "120px",
    padding: "12px",
    border: "1px solid var(--grayscale-a4, #d1d5db)",
    borderRadius: "6px",
    fontSize: "14px",
    fontFamily: "inherit",
    resize: "vertical",
    backgroundColor: "var(--grayscale-1, #ffffff)",
    color: "var(--grayscale-12, #111827)",
  };

  const charCountStyle: React.CSSProperties = {
    fontSize: "12px",
    color: "var(--grayscale-11, #6b7280)",
    marginTop: "4px",
  };

  const toggleContainerStyle: React.CSSProperties = {
    display: "flex",
    gap: "4px",
    padding: "4px",
    backgroundColor: "var(--grayscale-a3, #e5e7eb)",
    borderRadius: "6px",
    width: "fit-content",
  };

  const toggleButtonStyle = (active: boolean): React.CSSProperties => ({
    padding: "6px 16px",
    border: "none",
    borderRadius: "4px",
    fontSize: "13px",
    fontWeight: 500,
    cursor: "pointer",
    backgroundColor: active ? "var(--grayscale-1, #ffffff)" : "transparent",
    color: active ? "var(--grayscale-12, #111827)" : "var(--grayscale-11, #6b7280)",
    boxShadow: active ? "0 1px 2px rgba(0,0,0,0.08)" : "none",
    transition: "all 0.15s ease",
  });

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
          <label style={labelStyle}>Describe your agent</label>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="A customer service agent for a pizza delivery company. It can check order status by order number, estimate delivery time, process refunds, and answer questions about the menu. It should be friendly and concise."
            style={textareaStyle}
          />
          <div style={charCountStyle}>
            {description.length > 0 &&
              `${description.length.toLocaleString()} / ${MAX_DESCRIPTION_CHARS.toLocaleString()} characters`}
            {description.length > MAX_DESCRIPTION_CHARS && " — will be truncated"}
          </div>
        </div>

        <div>
          <label style={labelStyle}>Output format</label>
          <div style={toggleContainerStyle}>
            <button
              onClick={() => setFormat("python")}
              style={toggleButtonStyle(format === "python")}
            >
              Python
            </button>
            <button
              onClick={() => setFormat("javascript")}
              style={toggleButtonStyle(format === "javascript")}
            >
              JavaScript
            </button>
            <button
              onClick={() => setFormat("config")}
              style={toggleButtonStyle(format === "config")}
            >
              Config only
            </button>
          </div>
        </div>

        <div style={{ marginTop: "8px" }}>
          <label style={labelStyle}>Generate with AI</label>
          <div style={{ display: "flex", gap: "12px", flexWrap: "wrap" }}>
            <button
              onClick={openInClaude}
              style={{ ...buttonBaseStyle, backgroundColor: "#d97706" }}
            >
              <svg width="16" height="16" viewBox="0 0 16 17" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path fillRule="evenodd" clipRule="evenodd" d="M9.218 2.52954H11.62L16 13.5162H13.598L9.218 2.52954ZM4.37933 2.52954H6.89067L11.2707 13.5162H8.82133L7.926 11.2089H3.34467L2.44867 13.5155H0L4.38 2.53087L4.37933 2.52954ZM7.134 9.16887L5.63533 5.30754L4.13667 9.16954H7.13333L7.134 9.16887Z" fill="currentColor"/>
              </svg>
              Open in Claude
            </button>
            <button
              onClick={openInChatGPT}
              style={{ ...buttonBaseStyle, backgroundColor: "#10a37f" }}
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M22.0606 9.86697C22.6034 8.23781 22.4165 6.45314 21.5485 4.97127C20.2431 2.69837 17.6188 1.52902 15.0558 2.0793C13.9156 0.794818 12.2774 0.0643507 10.5601 0.074818C7.94025 0.0688367 5.61576 1.75557 4.80978 4.24828C3.12679 4.59295 1.67408 5.64641 0.823986 7.13949C-0.491154 9.40641-0.191341 12.264 1.56567 14.2079C1.02286 15.8371 1.20978 17.6217 2.07782 19.1036C3.38324 21.3765 6.00754 22.5458 8.57053 21.9956C9.70997 23.2801 11.3488 24.0105 13.0662 23.9993C15.6875 24.006 18.0128 22.3178 18.8188 19.8229C20.5017 19.4782 21.9545 18.4247 22.8045 16.9316C24.1182 14.6647 23.8176 11.8094 22.0614 9.86547L22.0606 9.86697ZM13.0677 22.4359C12.0188 22.4374 11.0027 22.0703 10.1974 21.3982L10.3388 21.3182L15.1029 18.5668C15.3466 18.4285 15.4961 18.169 15.4946 17.8886V11.1724L17.5081 12.335C17.5298 12.3455 17.544 12.3664 17.547 12.3903V17.9522C17.544 20.4255 15.541 22.4307 13.0677 22.4359ZM3.43483 18.3215C2.90922 17.4139 2.72006 16.35 2.90025 15.3174L3.04156 15.4019L7.80567 18.1533C8.04716 18.2946 8.34623 18.2946 8.58847 18.1533L14.4045 14.7948V17.1201C14.406 17.144 14.3948 17.1672 14.3761 17.1821L9.56044 19.9627C7.41539 21.1978 4.67595 20.4636 3.43558 18.3215H3.43483ZM2.181 7.92229C2.70436 7.01314 3.53053 6.31781 4.51445 5.95669V6.12117L4.51221 11.6247C4.51072 11.9043 4.66025 12.1638 4.90324 12.3021L10.7193 15.6599L8.70586 16.8225C8.68567 16.8359 8.66025 16.8382 8.63782 16.8285L3.82137 14.0457C1.68081 12.806 0.946603 10.0673 2.18025 7.92304L2.181 7.92229ZM18.7238 11.772L12.9077 8.41351L14.9212 7.25164C14.9414 7.23818 14.9668 7.23594 14.9892 7.24566L19.8057 10.0262C21.95 11.2651 22.6849 14.0083 21.446 16.1526C20.9219 17.0602 20.0965 17.7556 19.1133 18.1174V12.4494C19.1156 12.1698 18.9668 11.9111 18.7245 11.772H18.7238ZM20.7275 8.75594L20.5862 8.67145L15.8221 5.92005C15.5806 5.77874 15.2816 5.77874 15.0393 5.92005L9.22324 9.27856V6.95332C9.22174 6.9294 9.23296 6.90622 9.25165 6.89127L14.0674 4.11295C16.2124 2.87557 18.9548 3.61201 20.1915 5.75781C20.7141 6.66398 20.9032 7.72491 20.726 8.75594H20.7275ZM8.12866 12.9002L6.11445 11.7376C6.09277 11.7272 6.07857 11.7062 6.07558 11.6823V6.12043C6.07707 3.64416 8.08604 1.63743 10.5623 1.63893C11.6098 1.63893 12.6236 2.00678 13.4288 2.67669L13.2875 2.75669L8.52343 5.50809C8.27969 5.64641 8.13016 5.9051 8.13165 6.18547L8.12866 12.8987V12.9002ZM9.22249 10.5421L11.8131 9.04603L14.4038 10.5414V13.5328L11.8131 15.0281L9.22249 13.5328V10.5421Z" fill="currentColor"/>
              </svg>
              Open in ChatGPT
            </button>
            <button
              onClick={openInGemini}
              style={{ ...buttonBaseStyle, backgroundColor: "#4285f4" }}
            >
              <svg width="16" height="16" viewBox="0 0 16 17" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M8 16.5C8 12.634 11.134 9.5 15 9.5V8.5C11.134 8.5 8 5.366 8 1.5C8 5.366 4.866 8.5 1 8.5V9.5C4.866 9.5 8 12.634 8 16.5Z" fill="currentColor"/>
              </svg>
              Open in Gemini
            </button>
          </div>
          <p style={helpTextStyle}>
            Opens your preferred AI with your agent description and the full S2S
            API reference pre-loaded. It will generate a complete agent with
            system prompt, tool definitions, and runnable code.
          </p>
        </div>
      </div>
    </div>
  );
}
