# universal-streaming-english Built-in Formatting Rollout — Documentation Updates

## Context

The `universal-streaming-english` model has been updated so that text formatting is now handled in-model rather than by a secondary post-processing service. The rollout is moving to 100% imminently. Docs currently describe the old behavior (formatting is a separate trailing message, only on final turns). These changes need to land before the rollout completes.

The highest-risk customer breakage: using `turn_is_formatted=true` as an end-of-turn signal. The docs must warn against this prominently and update code examples to use `end_of_turn` instead.

---

## Scope

**In scope:**
- `universal-streaming-overview.mdx` — field definition, immutable transcription explanation, quickstart code examples (Python + JS), Warning callout
- `universal-streaming-messages.mdx` — all partial/final JSON examples, both "End of turn formatting" sections, best practices latency note
- `turn-detection.mdx` — add canonical signal note (additive only)
- `multilingual.mdx` — remove "In the future" sentence (one-line change)

**Out of scope:**
- `u3-pro-message-sequence.mdx` — already correct
- Whisper-RT formatting sections in `multilingual.mdx` — different model, unaffected
- Any changelog or release notes page

---

## Current State

See `RESEARCH.md` for full file inventory. Key files:

| File | Lines of interest |
|------|------------------|
| `fern/pages/speech-to-text/universal-streaming/universal-streaming-overview.mdx` | 234–241 (Python handler), 595–601 (JS handler), 837 (field def), 862–869 (immutable transcription) |
| `fern/pages/speech-to-text/universal-streaming/universal-streaming-messages.mdx` | 57–629 (all partial JSON), 342–395 (first formatting section), 748–799 (second formatting section), 807 (best practices) |
| `fern/pages/speech-to-text/universal-streaming/turn-detection.mdx` | 158–163 (Important notes section) |
| `fern/pages/speech-to-text/universal-streaming/multilingual.mdx` | 742 (the "In the future" sentence) |

**Key behavioral change:** `format_turns` now defaults to `true`. The YAML definition (`fern/.definition/universalStreaming.yml` line 133) currently shows `default: "false"` — this is wrong and must be updated. Any prose describing `format_turns` as opt-in must be updated to opt-out framing.

---

## Implementation Plan

### Phase 1: `universal-streaming-overview.mdx` — Main Page

**Goal:** Fix the field definition, the immutable transcription explanation, the Warning callout, and the broken quickstart code examples.

---

#### 1a. Update `format_turns` and `turn_is_formatted` field definitions (lines ~835–837)

**File:** `fern/pages/speech-to-text/universal-streaming/universal-streaming-overview.mdx`

**`format_turns` bullet** — replace current text with:

```
- `format_turns`: Boolean controlling whether transcript output is formatted. Defaults to `true`. When `true`, formatting (punctuation, casing, inverse text normalization) is applied in-model to all turns — including partial results. Set to `false` to receive unformatted output for the entire session.
```

**`turn_is_formatted` bullet** — replace current text with:

```
- `turn_is_formatted`: Boolean indicating if the text in the `transcript` field has been formatted with punctuation, casing, and inverse text normalization (e.g. dates, times, phone numbers). Formatting is built into the model so this field will be `true` on every Turn message — including partial results. You can set `format_turns=false` and this field will be `false` on all messages. Do not use `turn_is_formatted` to detect end of turn; use `end_of_turn` instead.
```

---

#### 1b. Add Warning callout immediately after the field definitions block (after line ~850)

**File:** `fern/pages/speech-to-text/universal-streaming/universal-streaming-overview.mdx`

Add this Warning component immediately after the `words` array explanation closes and before the `### Immutable transcription` heading:

```mdx
<Warning>
  **Do not use `turn_is_formatted` to detect end of turn.** Formatting is applied in-model to all
  Turn messages — including partial results — so `turn_is_formatted` will be
  `true` throughout a session, not only at turn boundaries. Use `end_of_turn`
  to determine when a speaker's turn has completed.
</Warning>
```

---

#### 1c. Rewrite the immutable transcription section (lines 862–869)

**File:** `fern/pages/speech-to-text/universal-streaming/universal-streaming-overview.mdx`

Replace:

```
When an end of the current turn is detected, you then receive a message with `end_of_turn` being `true`. Additionally, if you enable text formatting, you will also receive a transcription response with `turn_is_formatted` being `true`.

```json
→ hello my name is zack (unformatted)
→ Hello my name is Zack. (formatted)
```
```

With:

```
When an end of the current turn is detected, you receive a message with `end_of_turn` set to `true`. Formatting is applied in-model to every Turn message, so both partial results and the final turn will have `turn_is_formatted: true`. There is no separate trailing formatting message — the `end_of_turn: true` message is itself formatted.

```json
→ Hello my name is Zack.   (end_of_turn: false)
→ Hello, my name is Zack.  (end_of_turn: true)
```
```

---

#### 1d. Fix Python quickstart code example (lines 234–241)

**File:** `fern/pages/speech-to-text/universal-streaming/universal-streaming-overview.mdx`

Replace the `on_message` handler block (the `Turn` branch):

```python
# OLD — broken: turn_is_formatted is now true on partials too
elif msg_type == "Turn":
    transcript = data.get('transcript', '')
    formatted = data.get('turn_is_formatted', False)

    # Clear previous line for formatted messages
    if formatted:
        print('\r' + ' ' * 80 + '\r', end='')
        print(transcript)
    else:
        print(f"\r{transcript}", end='')
```

With:

```python
elif msg_type == "Turn":
    transcript = data.get('transcript', '')
    end_of_turn = data.get('end_of_turn', False)

    if end_of_turn:
        print('\r' + ' ' * 80 + '\r', end='')
        print(transcript)
    else:
        print(f"\r{transcript}", end='')
```

---

#### 1e. Fix JavaScript quickstart code example (lines 595–601)

**File:** `fern/pages/speech-to-text/universal-streaming/universal-streaming-overview.mdx`

Replace the `Turn` branch in the `ws.on("message", ...)` handler:

```javascript
// OLD — broken
} else if (msgType === "Turn") {
    const transcript = data.transcript || "";
    const formatted = data.turn_is_formatted;

    if (formatted) {
        clearLine();
        console.log(transcript);
    } else {
        process.stdout.write(`\r${transcript}`);
    }
```

With:

```javascript
} else if (msgType === "Turn") {
    const transcript = data.transcript || "";
    const endOfTurn = data.end_of_turn;

    if (endOfTurn) {
        clearLine();
        console.log(transcript);
    } else {
        process.stdout.write(`\r${transcript}`);
    }
```

---

### Phase 2: `universal-streaming-messages.mdx` — Message Sequence

**Goal:** Update all JSON examples and remove both "End of turn formatting" sections that describe the now-removed trailing formatting message.

---

#### 2a. Update `turn_is_formatted` in all partial turn JSON examples

**File:** `fern/pages/speech-to-text/universal-streaming/universal-streaming-messages.mdx`

There are 14 partial turn JSON examples across the file (lines 57, 79, 103, 138, 181, 229, 403, 424, 451, 488, 529, 578, 638, 699). Each contains:

```json
"turn_is_formatted": false,
```

Every instance should be updated to:

```json
"turn_is_formatted": true,
```

This is a global find-and-replace within this file. Note: the two JSON examples in the "End of turn formatting" sections (the old trailing-message payloads) will be removed entirely in step 2c below, so they don't need individual edits.

---

#### 2b. Update `turn_is_formatted` in both `end_of_turn: true` JSON examples

**File:** `fern/pages/speech-to-text/universal-streaming/universal-streaming-messages.mdx`

There are two `end_of_turn: true` messages that currently show `"turn_is_formatted": false` (around lines 296–339 and 699–745). These also need to flip to `"turn_is_formatted": true`.

**First `end_of_turn: true` example (line ~297):**
```json
// change this:
"turn_is_formatted": false,
"end_of_turn": true,

// to:
"turn_is_formatted": true,
"end_of_turn": true,
```

**Second `end_of_turn: true` example (line ~700):**
Same change: `"turn_is_formatted": false` → `"turn_is_formatted": true`.

---

#### 2c. Remove first "End of turn formatting" section (lines 342–395)

**File:** `fern/pages/speech-to-text/universal-streaming/universal-streaming-messages.mdx`

Remove the entire section:

```
### End of turn formatting

Once the turn ends, if formatting is enabled there will be an additional message where `"turn_is_formatted":True` comes back. This will format the final message.

Since LLMs can parse unformatted text, waiting for this message is NOT recommended for voice agents as it adds additional latency. It is recommended for other use cases like closed captioning where the transcript will be displayed to the end user.

[JSON example payload with turn_is_formatted: true, end_of_turn: true, transcript: "Hi, my name is Sonny."]
```

This section describes a message that no longer exists. The `end_of_turn: true` message (updated in step 2b) is now the final message in a turn sequence. No replacement text is needed — the section is simply gone.

---

#### 2d. Remove second "End of turn formatting" section (lines 748–799)

**File:** `fern/pages/speech-to-text/universal-streaming/universal-streaming-messages.mdx`

Same as 2c — remove the entire section:

```
### End of turn formatting

Lastly we will format the transcript if formatting is enabled. Again this is only recommended for use cases where the end user will be shown the transcript as it adds some latency for voice agents.

[JSON example payload with turn_is_formatted: true, end_of_turn: true, transcript: "I am a voice agent."]
```

---

#### 2e. Update best practices latency note (line 807)

**File:** `fern/pages/speech-to-text/universal-streaming/universal-streaming-messages.mdx`

Replace:

```
- Avoid using `format_turns` as it will significantly increase latency. LLMs don't need formatting so you can just pass raw text as soon as its ready.
```

With:

```
- For voice agent pipelines, you can omit `format_turns` — LLMs process unformatted text directly, and skipping formatting keeps your handler logic simpler. If you're building a notetaking or closed captioning app where output is displayed to users, `format_turns=true` is the right choice.
```

---

### Phase 3: `turn-detection.mdx` — Add Canonical Signal Note

**Goal:** Explicitly state that `end_of_turn` is the only reliable turn-end signal. Additive only — no existing content changes.

---

#### 3a. Add note to "Important notes" section (after line 160)

**File:** `fern/pages/speech-to-text/universal-streaming/turn-detection.mdx`

Append to the existing "Important notes" bullet list:

```
- **Use `end_of_turn` to detect turn completion.** With the `universal-streaming-english` model, `turn_is_formatted` is `true` on every Turn message (partial and final) when `format_turns=true`, so it no longer signals that a turn has ended. The only reliable way to detect turn completion is `end_of_turn: true`.
```

---

### Phase 4: `multilingual.mdx` — Remove Forward-Looking Sentence

**Goal:** Remove the one sentence that describes the English formatting change as a future event, since it is now live.

---

#### 4a. Remove "In the future" sentence (line 742)

**File:** `fern/pages/speech-to-text/universal-streaming/multilingual.mdx`

Remove:

```
In the future, this built-in formatting capability will be extended to our English-only streaming model as well.
```

---

### Phase 5: API Definition Files — `format_turns` and `turn_is_formatted` Descriptions

**Goal:** Update the Fern YAML definitions that drive the generated API reference so the field descriptions reflect the new behavior.

---

#### 5a. Update `format_turns` default and docs string (line 133–135)

**File:** `fern/.definition/universalStreaming.yml`

Replace:

```yaml
format_turns:
  default: "false"
  docs: Whether to return formatted final transcripts.
  type: optional<StreamingFormatTurns>
```

With:

```yaml
format_turns:
  default: "true"
  docs: Whether to return formatted transcripts. Defaults to `true`. When enabled, formatting is applied in-model to all turns — including partial results. Set to `false` to disable formatting for the entire session.
  type: optional<StreamingFormatTurns>
```

---

### Phase 6: Fix Pattern A — Raw Python `turn_is_formatted` proxy (13 files)

**Goal:** Replace `formatted = data.get('turn_is_formatted', False)` / `if formatted:` with `if data.get('end_of_turn'):` across all raw Python code examples.

**Find (in each file listed below):**
```python
formatted = data.get('turn_is_formatted', False)

# Clear previous line for formatted messages
if formatted:
    print('\r' + ' ' * 80 + '\r', end='')
    print(transcript)
else:
    print(f"\r{transcript}", end='')
```

**Replace with:**
```python
if data.get('end_of_turn'):
    print('\r' + ' ' * 80 + '\r', end='')
    print(transcript)
else:
    print(f"\r{transcript}", end='')
```

Note: the exact surrounding code varies by file (comment wording, variable names). The key change is: remove the `formatted = data.get('turn_is_formatted', False)` line and replace the `if formatted:` condition with `if data.get('end_of_turn'):`. Preserve all other surrounding code.

**Apply to:**

| File | Lines |
|------|-------|
| `fern/pages/getting-started/transcribe-streaming-audio.mdx` | 138 |
| `fern/pages/speech-to-text/universal-streaming/universal-streaming-keyterms.mdx` | 151 |
| `fern/pages/speech-to-text/universal-streaming/streaming-diarization-and-multichannel.mdx` | 683 |
| `fern/pages/guides/webhooks-streaming.mdx` | 127 |
| `fern/pages/guides/cookbooks/streaming-stt/v2_to_v3.mdx` | 91 |
| `fern/pages/guides/cookbooks/streaming-stt/real_time_llm_gateway.mdx` | 119 |
| `fern/pages/guides/cookbooks/streaming-stt/real_time_translation.mdx` | 112 |
| `fern/pages/guides/cookbooks/streaming-stt/transcribe_system_audio.mdx` | 116 |
| `fern/pages/guides/cookbooks/streaming-stt/turn_detection_improvement_using_async.mdx` | 405 |
| `fern/pages/use-cases/meeting-notetaker-best-practices.mdx` | 384, 1394 |
| `fern/pages/use-cases/contact-center-best-practices.mdx` | 355 |
| `fern/pages/use-cases/medical-scribe-best-practices.mdx` | 569 |
| `fern/pages/guides/billing-tracking.mdx` | 281 |

---

### Phase 7: Fix Pattern B — Raw JavaScript `turn_is_formatted` proxy (11 files)

**Goal:** Replace `const formatted = data.turn_is_formatted` / `if (formatted)` with `if (data.end_of_turn)` across all raw JavaScript code examples.

**Find (in each file listed below):**
```javascript
const formatted = data.turn_is_formatted;

if (formatted) {
    clearLine();
    console.log(transcript);
} else {
    process.stdout.write(`\r${transcript}`);
}
```

**Replace with:**
```javascript
if (data.end_of_turn) {
    clearLine();
    console.log(transcript);
} else {
    process.stdout.write(`\r${transcript}`);
}
```

Note: exact surrounding code varies (some use `process.stdout.write`, some `console.log`). Key change: remove the `const formatted` line and replace `if (formatted)` with `if (data.end_of_turn)`. Preserve all other surrounding code.

**Apply to:**

| File | Lines |
|------|-------|
| `fern/pages/getting-started/transcribe-streaming-audio.mdx` | 478 |
| `fern/pages/speech-to-text/universal-streaming/universal-streaming-keyterms.mdx` | 313 |
| `fern/pages/speech-to-text/universal-streaming/streaming-diarization-and-multichannel.mdx` | 862 |
| `fern/pages/guides/webhooks-streaming.mdx` | 342 |
| `fern/pages/guides/cookbooks/streaming-stt/v2_to_v3_js.mdx` | 143 |
| `fern/pages/guides/cookbooks/streaming-stt/real_time_llm_gateway.mdx` | 393 |
| `fern/pages/guides/cookbooks/streaming-stt/real_time_translation.mdx` | 370 |
| `fern/pages/guides/cookbooks/streaming-stt/transcribe_system_audio.mdx` | 391 |
| `fern/pages/guides/cookbooks/streaming-stt/turn_detection_improvement_using_async.mdx` | 997 |
| `fern/pages/use-cases/meeting-notetaker-best-practices.mdx` | 621 |
| `fern/pages/use-cases/contact-center-best-practices.mdx` | 485 |

---

### Phase 8: Fix Pattern C — Python SDK `turn_is_formatted` proxy (6 files)

**Goal:** Replace `if event.turn_is_formatted:` with `if event.end_of_turn:` across Python SDK code examples.

**Find:**
```python
if event.turn_is_formatted:
    # handle final formatted turn
```

**Replace with:**
```python
if event.end_of_turn:
    # handle final turn
```

**Apply to:**

| File | Lines |
|------|-------|
| `fern/pages/getting-started/transcribe-streaming-audio.mdx` | 1277 |
| `fern/pages/speech-to-text/universal-streaming/universal-streaming-keyterms.mdx` | 597 |
| `fern/pages/speech-to-text/universal-streaming/streaming-diarization-and-multichannel.mdx` | 1523 |
| `fern/pages/guides/cookbooks/streaming-stt/v2_to_v3.mdx` | 383 |
| `fern/pages/guides/cookbooks/streaming-stt/v2_to_v3_js.mdx` | 397 |
| `fern/pages/use-cases/medical-scribe-best-practices.mdx` | 581, 584 |

---

### Phase 9: Fix Pattern D — Never-firing `end_of_turn and not turn_is_formatted` condition (2 files)

**Goal:** Remove the `not event.turn_is_formatted` guard that will never be `True` now that `turn_is_formatted` is always `true` when `format_turns=True`.

**Find:**
```python
if event.end_of_turn and not event.turn_is_formatted:
    # handle unformatted final
```

**Replace with:**
```python
if event.end_of_turn:
    # handle final
```

**Apply to:**

| File | Lines |
|------|-------|
| `fern/pages/guides/cookbooks/streaming-stt/noise_reduction_streaming.mdx` | 70, 177 |
| `fern/pages/guides/cookbooks/streaming-stt/terminate_realtime_programmatically.mdx` | 60, 177 |

---

### Phase 10: Fix Outdated Prose (1 file)

**Goal:** Update the Universal Streaming column in the migration comparison table to reflect that `turn_is_formatted` is no longer a separate trailing message.

---

#### 10b. `universal_to_u3_pro_streaming.mdx` — Update comparison table row (line 59)

**File:** `fern/pages/guides/cookbooks/streaming-stt/universal_to_u3_pro_streaming.mdx`

Find the `end_of_turn / turn_is_formatted` cell in the Universal Streaming column:
```
Can differ on English model — `turn_is_formatted` arrives as a separate message after `end_of_turn` (multilingual model has formatting built in, so they match)
```

Replace with:
```
The model has built in formatting so `turn_is_formatted` is `true` on all turns including partials — do not use it as a turn-end signal. Use `end_of_turn: true` to detect when a turn has completed.
```

---

## File Change Summary

### New Files

None.

### Modified Files

| File | Phase | Change |
|------|-------|--------|
| `fern/pages/speech-to-text/universal-streaming/universal-streaming-overview.mdx` | 1 | Update field def; add Warning; rewrite immutable transcription; fix Python + JS examples |
| `fern/pages/speech-to-text/universal-streaming/universal-streaming-messages.mdx` | 2 | Flip `turn_is_formatted` in all JSON examples; remove formatting sections; update best practices |
| `fern/pages/speech-to-text/universal-streaming/turn-detection.mdx` | 3 | Add `end_of_turn` canonical signal note |
| `fern/pages/speech-to-text/universal-streaming/multilingual.mdx` | 4 | Replace "In the future" sentence |
| `fern/.definition/universalStreaming.yml` | 5 | Update `format_turns` docs string |
| `fern/.definition/__package__.yml` | 5 | Update `turn_is_formatted` docs string |
| `fern/pages/getting-started/transcribe-streaming-audio.mdx` | 6, 7, 8 | Fix Pattern A (138), B (478), C (1277) |
| `fern/pages/speech-to-text/universal-streaming/universal-streaming-keyterms.mdx` | 6, 7, 8 | Fix Pattern A (151), B (313), C (597) |
| `fern/pages/speech-to-text/universal-streaming/streaming-diarization-and-multichannel.mdx` | 6, 7, 8 | Fix Pattern A (683), B (862), C (1523) |
| `fern/pages/guides/webhooks-streaming.mdx` | 6, 7 | Fix Pattern A (127), B (342) |
| `fern/pages/guides/cookbooks/streaming-stt/v2_to_v3.mdx` | 6, 8 | Fix Pattern A (91), C (383) |
| `fern/pages/guides/cookbooks/streaming-stt/v2_to_v3_js.mdx` | 7, 8 | Fix Pattern B (143), C (397) |
| `fern/pages/guides/cookbooks/streaming-stt/real_time_llm_gateway.mdx` | 6, 7 | Fix Pattern A (119), B (393) |
| `fern/pages/guides/cookbooks/streaming-stt/real_time_translation.mdx` | 6, 7 | Fix Pattern A (112), B (370) |
| `fern/pages/guides/cookbooks/streaming-stt/transcribe_system_audio.mdx` | 6, 7 | Fix Pattern A (116), B (391) |
| `fern/pages/guides/cookbooks/streaming-stt/turn_detection_improvement_using_async.mdx` | 6, 7 | Fix Pattern A (405), B (997) |
| `fern/pages/use-cases/meeting-notetaker-best-practices.mdx` | 6, 7 | Fix Pattern A (384, 1394), B (621) |
| `fern/pages/use-cases/contact-center-best-practices.mdx` | 6, 7 | Fix Pattern A (355), B (485) |
| `fern/pages/use-cases/medical-scribe-best-practices.mdx` | 6, 8 | Fix Pattern A (569), C (581, 584) |
| `fern/pages/guides/billing-tracking.mdx` | 6 | Fix Pattern A (281) |
| `fern/pages/guides/cookbooks/streaming-stt/noise_reduction_streaming.mdx` | 9 | Fix Pattern D (70, 177) |
| `fern/pages/guides/cookbooks/streaming-stt/terminate_realtime_programmatically.mdx` | 9 | Fix Pattern D (60, 177) |
| `fern/pages/guides/cookbooks/streaming-stt/universal_to_u3_pro_streaming.mdx` | 10 | Update Universal Streaming column in comparison table (turn_is_formatted row) |

---

## Open Questions

1. **Message sequence page — section structure after removal:** After removing both "End of turn formatting" sections, the turn lifecycle flows directly from "End of turn, after End of utterance" to "Session termination." Should a brief note be added at the end of the turn sequence (e.g. a Note component) explaining that with `format_turns=true` the final `end_of_turn: true` message is already formatted? Or is updating the JSON examples sufficient?

2. **Warning callout placement:** The Warning (step 1b) is planned to sit just before `### Immutable transcription`. Alternatively, it could go at the very top of the Turn object section, or as an inline note within the `turn_is_formatted` bullet itself. Is there a preferred placement in this doc's style?

3. **Quickstart code examples — Python SDK and JavaScript SDK tabs:** The raw Python/JS tabs are updated in steps 1d–1e. The SDK tabs (`Python SDK`, `JavaScript SDK`) use the `TurnEvent` abstraction and don't directly check `turn_is_formatted`, so they are likely fine as-is. Confirm these don't need changes.
