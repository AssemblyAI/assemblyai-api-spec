import os
import json
import time
import threading
from datetime import datetime
from urllib.parse import urlencode

import pyaudio
import websocket
import requests
from dotenv import load_dotenv
from simple_term_menu import TerminalMenu

# Load environment variables from .env if present
try:
    load_dotenv()
except Exception:
    pass

"""
Medical Scribe – Streaming STT + LLM Gateway Enhancement (SOAP-ready)

What this does
--------------
1) Streams mic audio to AssemblyAI Streaming STT (with formatted turns + keyterms)
2) On every utterance or formatted final turn, calls AssemblyAI LLM Gateway to
   apply *medical* edits (terminology, punctuation, proper nouns, etc.)
3) Logs encounter turns and generates a SOAP note at session end via the Gateway

Quick start
-----------
export ASSEMBLYAI_API_KEY=your_key
# Optional: pick a Gateway model (defaults to Claude 3.5 Haiku)
export LLM_GATEWAY_MODEL=claude-3-5-haiku-20241022

python medical_scribe_llm_gateway.py
"""

# === Config ===
ASSEMBLYAI_API_KEY = os.environ.get("ASSEMBLYAI_API_KEY", "your_api_key_here")

# Medical context and terminology (seed – you can swap at runtime)
MEDICAL_KEYTERMS = [
    "hypertension",
    "diabetes mellitus",
    "coronary artery disease",
    "metformin 1000mg",
    "lisinopril 10mg",
    "atorvastatin 20mg",
    "chief complaint",
    "history of present illness",
    "review of systems",
    "physical examination",
    "assessment and plan",
    "auscultation",
    "palpation",
    "reflexes",
    "range of motion",
]

# WebSocket / STT parameters - CONSERVATIVE SETTINGS FOR MEDICAL
CONNECTION_PARAMS = {
    "sample_rate": 16000,
    "format_turns": True,  # Always true for readable clinical notes

    # MEDICAL SCRIBE CONFIGURATION - Conservative for clinical accuracy
    # Medical conversations have LONG pauses (provider thinking, examining patient, reviewing charts)
    "end_of_turn_confidence_threshold": 0.7,  # Higher confidence (vs 0.4 for voice agents)
    "min_end_of_turn_silence_when_confident": 800,  # Wait much longer (vs 160ms voice agents, 560ms meetings)
    "max_turn_silence": 3600,  # Much longer for clinical thinking pauses

    "keyterms_prompt": json.dumps(MEDICAL_KEYTERMS),  # JSON string
}

API_ENDPOINT_BASE_URL = "wss://streaming.assemblyai.com/v3/ws"
API_ENDPOINT = f"{API_ENDPOINT_BASE_URL}?{urlencode(CONNECTION_PARAMS)}"

# Audio config
FRAMES_PER_BUFFER = 800  # 50ms @ 16kHz
SAMPLE_RATE = CONNECTION_PARAMS["sample_rate"]
CHANNELS = 1
FORMAT = pyaudio.paInt16

# Globals
audio = None
stream = None
ws_app = None
audio_thread = None
stop_event = threading.Event()
encounter_buffer = []  # list of dicts with turn data
last_processed_turn = None

# === Model selection ===
AVAILABLE_MODELS = [
    {"id": "claude-3-haiku-20240307", "name": "Claude 3 Haiku", "description": "Fastest Claude, good for simple tasks"},
    {"id": "claude-3-5-haiku-20241022", "name": "Claude 3.5 Haiku", "description": "Fast with better reasoning"},
    {"id": "claude-sonnet-4-20250514", "name": "Claude Sonnet 4", "description": "Balanced speed & intelligence"},
    {"id": "claude-sonnet-4-5-20250929", "name": "Claude Sonnet 4.5", "description": "Best for coding & agents"},
    {"id": "claude-opus-4-20250514", "name": "Claude Opus 4", "description": "Most powerful, deep reasoning"},
]

def select_model():
    menu_entries = [f"{m['name']} - {m['description']}" for m in AVAILABLE_MODELS]
    terminal_menu = TerminalMenu(
        menu_entries,
        title="Select a model (Use ↑↓ arrows, Enter to select):",
        menu_cursor="❯ ",
        menu_cursor_style=("fg_cyan", "bold"),
        menu_highlight_style=("bg_cyan", "fg_black"),
        cycle_cursor=True,
        clear_screen=False,
        show_search_hint=True,
    )
    idx = terminal_menu.show()
    if idx is None:
        print("Model selection cancelled. Exiting...")
        raise SystemExit(0)
    return AVAILABLE_MODELS[idx]["id"]

selected_model = None

# === Gateway helpers ===

def _gateway_chat(messages, max_tokens=800, temperature=0.2, retries=3, backoff=0.75):
    """Call AssemblyAI LLM Gateway with debug logging and retry."""
    url = "https://llm-gateway.assemblyai.com/v1/chat/completions"
    headers = {
        "Authorization": ASSEMBLYAI_API_KEY,
        "Content-Type": "application/json",
    }
    payload = {
        "model": selected_model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }

    last = None
    for attempt in range(retries):
        try:
            print(f"[LLM] POST {url} (model={selected_model}, attempt {attempt+1}/{retries})")
            resp = requests.post(url, headers=headers, json=payload, timeout=60)
            print(f"[LLM] ← status {resp.status_code}, bytes {len(resp.content)}")
            last = resp
        except Exception as e:
            if attempt == retries - 1:
                raise RuntimeError(f"Gateway request error: {e}")
            time.sleep(backoff * (attempt + 1))
            continue

        if resp.status_code == 200:
            data = resp.json()
            if not data.get("choices") or not data["choices"][0].get("message"):
                raise RuntimeError(f"Gateway OK but empty body: {str(data)[:200]}")
            return data
        if resp.status_code in (429, 500, 502, 503, 504):
            print(f"[LLM RETRY] {resp.status_code}: {resp.text[:180]}")
            time.sleep(backoff * (attempt + 1))
            continue
        raise RuntimeError(f"Gateway error {resp.status_code}: {resp.text[:300]}")

    raise RuntimeError(
        f"Gateway failed after retries. Last={getattr(last,'status_code','n/a')} {getattr(last,'text','')[:180]}"
    )


def post_process_with_llm(text: str) -> str:
    """Medical editing & normalization using LLM Gateway."""
    system = {
        "role": "system",
        "content": (
            "You are a clinical transcription editor. Keep the speaker's words, "
            "fix medical terminology (drug names, dosages, anatomy), proper nouns, "
            "and punctuation for readability. Preserve meaning and avoid inventing "
            "details. Prefer U.S. clinical style. If a medication or condition is "
            "phonetically close, correct to the most likely clinical term."
        ),
    }

    user = {
        "role": "user",
        "content": (
            "Context keyterms (JSON array):\n" + json.dumps(MEDICAL_KEYTERMS) + "\n\n"
            "Edit this short transcript for medical accuracy and readability.\n\n"
            f"Transcript:\n{text}"
        ),
    }

    try:
        res = _gateway_chat([system, user], max_tokens=600)
        return res["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"[LLM EDIT ERROR] {e}. Falling back to original.")
        return text


def generate_clinical_note():
    """Create a SOAP note from the encounter buffer via Gateway."""
    if not encounter_buffer:
        print("No encounter data to summarize.")
        return

    print("\n=== GENERATING CLINICAL DOCUMENTATION (SOAP) ===")
    # Build a compact transcript string for the LLM
    lines = []
    for e in encounter_buffer:
        if e.get("type") == "utterance":
            lines.append(f"[{e['timestamp']}] {e.get('speaker', 'Speaker')}: {e['text']}")
        elif e.get("type") == "final":
            lines.append(f"[{e['timestamp']}] FINAL: {e['text']}")
    combined = "\n".join(lines)

    system = {
        "role": "system",
        "content": (
            "You are a clinician generating concise, structured notes. "
            "Produce a SOAP note (Subjective, Objective, Assessment, Plan). "
            "Use bullet points, keep it factual, infer reasonable clinical semantics "
            "from the transcript but do NOT invent data. Include medications with dosage "
            "and frequency if mentioned."
        ),
    }
    user = {
        "role": "user",
        "content": (
            "Create a SOAP note from this clinical encounter transcript.\n\n"
            f"Transcript:\n{combined}\n\n"
            "Format strictly as:\n"
            "Subjective:\n- ...\n\nObjective:\n- ...\n\nAssessment:\n- ...\n\nPlan:\n- ...\n"
        ),
    }

    try:
        res = _gateway_chat([system, user], max_tokens=1200)
        soap = res["choices"][0]["message"]["content"].strip()
        fname = f"clinical_note_soap_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(fname, "w", encoding="utf-8") as f:
            f.write(soap)
        print(f"SOAP note saved: {fname}")
    except Exception as e:
        print(f"[SOAP ERROR] {e}")


# === WebSocket callbacks ===

def on_open(ws):
    print("=" * 80)
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Medical transcription started")
    print(f"Connected to: {API_ENDPOINT_BASE_URL}")
    print(f"Gateway model: {selected_model}")
    print("=" * 80)
    print("\nSpeak to begin. Press Ctrl+C to stop.\n")

    def stream_audio():
        global stream
        while not stop_event.is_set():
            try:
                audio_data = stream.read(FRAMES_PER_BUFFER, exception_on_overflow=False)
                ws.send(audio_data, websocket.ABNF.OPCODE_BINARY)
            except Exception as e:
                if not stop_event.is_set():
                    print(f"Error streaming audio: {e}")
                break

    global audio_thread
    audio_thread = threading.Thread(target=stream_audio, daemon=True)
    audio_thread.start()


def on_message(ws, message):
    global last_processed_turn
    try:
        data = json.loads(message)
        msg_type = data.get("type")

        if msg_type == "Begin":
            print(f"[SESSION] Started - ID: {data.get('id','N/A')}\n")

        elif msg_type == "Turn":
            end_of_turn = data.get("end_of_turn", False)
            turn_is_formatted = data.get("turn_is_formatted", False)
            transcript = data.get("transcript", "")
            utterance = data.get("utterance", "")
            turn_order = data.get("turn_order", 0)
            eot_conf = data.get("end_of_turn_confidence", 0.0)

            # live partials
            if not end_of_turn and transcript:
                print(f"\r[PARTIAL] {transcript[:120]}...", end="", flush=True)

            # If AssemblyAI has finalized a turn AND it's formatted, LLM-edit the transcript
            if end_of_turn and transcript:
                if not turn_is_formatted:
                    # Explicitly skip unformatted finals
                    print("[DEBUG] EOT received (unformatted) – skipping LLM edit, waiting for formatted final…")
                elif turn_is_formatted:
                    if last_processed_turn == turn_order:
                        return  # avoid duplicate processing
                    last_processed_turn = turn_order

                    ts = datetime.now().strftime('%H:%M:%S')
                    print("\n[DEBUG] EOT received (formatted). Calling LLM…")
                    edited = post_process_with_llm(transcript)

                    changed = "(edited)" if edited.strip() != transcript.strip() else "(no change)"
                    print(f"\n[{ts}] [FINAL {changed}]")
                    print(f"  ├─ Original STT : {transcript}")
                    print(f"  └─ Edited by LLM: {edited}")
                    print(f"Turn: {turn_order} | Confidence: {eot_conf:.2%}")

                    encounter_buffer.append({
                        "timestamp": ts,
                        "text": edited,
                        "original_text": transcript,
                        "turn_order": turn_order,
                        "confidence": eot_conf,
                        "type": "final",
                    })

            # If we also get per-utterance chunks, just log them raw (no LLM) for timeline
            if utterance:
                ts = datetime.now().strftime('%H:%M:%S')

                low = utterance.lower()
                if any(t in low for t in ["medication", "prescribe", "dosage", "mg", "daily"]):
                    print("           💊 MEDICATION MENTIONED")
                if any(t in low for t in ["pain", "symptom", "complaint", "problem"]):
                    print("           🏥 SYMPTOM REPORTED")
                if any(t in low for t in ["diagnose", "assessment", "impression"]):
                    print("           📋 DIAGNOSIS DISCUSSED")

                encounter_buffer.append({
                    "timestamp": ts,
                    "text": utterance,
                    "original_text": utterance,
                    "turn_order": turn_order,
                    "confidence": eot_conf,
                    "type": "utterance",
                })
                print()

        elif msg_type == "Termination":
            dur = data.get("audio_duration_seconds", 0)
            print(f"\n[SESSION] Terminated – Duration: {dur}s")
            save_encounter_transcript()
            generate_clinical_note()

        elif msg_type == "Error":
            print(f"\n[ERROR] {data.get('error', 'Unknown error')}")

    except json.JSONDecodeError as e:
        print(f"Error decoding message: {e}")
    except Exception as e:
        print(f"Error handling message: {e}")


def on_error(ws, error):
    print(f"\n[WEBSOCKET ERROR] {error}")
    stop_event.set()


def on_close(ws, close_status_code, close_msg):
    print(f"\n[WEBSOCKET] Disconnected – Status: {close_status_code}")
    global stream, audio
    stop_event.set()

    if stream:
        if stream.is_active():
            stream.stop_stream()
        stream.close()
        stream = None
    if audio:
        audio.terminate()
        audio = None
    if audio_thread and audio_thread.is_alive():
        audio_thread.join(timeout=1.0)


# === Persist artifacts ===

def save_encounter_transcript():
    if not encounter_buffer:
        print("No encounter data to save.")
        return

    fname = f"encounter_transcript_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(fname, "w", encoding="utf-8") as f:
        f.write("Clinical Encounter Transcript\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 80 + "\n\n")
        for e in encounter_buffer:
            if e.get("speaker"):
                f.write(f"[{e['timestamp']}] {e['speaker']}: {e['text']}\n")
            else:
                f.write(f"[{e['timestamp']}] {e['text']}\n")
            f.write(f"Confidence: {e['confidence']:.2%}\n\n")
    print(f"Encounter transcript saved: {fname}")


# === Main ===

def run():
    global audio, stream, ws_app, selected_model

    print("=" * 60)
    print("  🎙️  Medical Scribe - STT + LLM Gateway")
    print("=" * 60)
    selected_model = select_model()
    print(f"✓ Using model: {selected_model}")

    # Init mic
    audio = pyaudio.PyAudio()
    try:
        stream = audio.open(
            input=True,
            frames_per_buffer=FRAMES_PER_BUFFER,
            channels=CHANNELS,
            format=FORMAT,
            rate=SAMPLE_RATE,
        )
        print("Audio stream opened successfully.")
    except Exception as e:
        print(f"Error opening audio stream: {e}")
        if audio:
            audio.terminate()
        return

    # Connect WS
    ws_headers = [f"Authorization: {ASSEMBLYAI_API_KEY}"]
    ws_app = websocket.WebSocketApp(
        API_ENDPOINT,
        header=ws_headers,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )

    ws_thread = threading.Thread(target=ws_app.run_forever, daemon=True)
    ws_thread.start()

    try:
        while ws_thread.is_alive():
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n\nCtrl+C received. Stopping...")
        stop_event.set()
        # best-effort terminate
        if ws_app and ws_app.sock and ws_app.sock.connected:
            try:
                ws_app.send(json.dumps({"type": "Terminate"}))
                time.sleep(0.5)
            except Exception as e:
                print(f"Error sending termination: {e}")
        if ws_app:
            ws_app.close()
        ws_thread.join(timeout=2.0)
    finally:
        if stream and stream.is_active():
            stream.stop_stream()
        if stream:
            stream.close()
        if audio:
            audio.terminate()
        print("Cleanup complete. Exiting.")


if __name__ == "__main__":
    run()
