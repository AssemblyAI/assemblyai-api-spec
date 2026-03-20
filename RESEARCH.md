# Research: universal-streaming-english Built-in Formatting Rollout — Documentation Changes

## Current State

### Files — Core Streaming Docs (Original Scope)

| File | Purpose |
|------|---------|
| `fern/pages/speech-to-text/universal-streaming/universal-streaming-overview.mdx` | Main Universal Streaming page — quickstart, core concepts, Turn object field definitions, immutable transcription explanation |
| `fern/pages/speech-to-text/universal-streaming/universal-streaming-messages.mdx` | Message Sequence Breakdown — step-by-step JSON example messages for a full turn, including the separate end-of-turn formatting message |
| `fern/pages/speech-to-text/universal-streaming/turn-detection.mdx` | Turn Detection page — semantic/acoustic detection, config presets, disable options, `end_of_turn` field |
| `fern/pages/speech-to-text/universal-streaming/multilingual.mdx` | Multilingual Streaming page — language detection, "Understanding formatting" sections for multilingual and Whisper-RT models |

### Files — Broken Code Examples (Expanded Scope)

`turn_is_formatted` used as end-of-turn proxy — broken because it is now `true` on partials too.

**Pattern A — Raw Python** (`formatted = data.get('turn_is_formatted', False)` → `if formatted:`):

| File | Lines |
|------|-------|
| `fern/pages/getting-started/transcribe-streaming-audio.mdx` | 138, 1164 |
| `fern/pages/speech-to-text/universal-streaming/universal-streaming-keyterms.mdx` | 151, 433 |
| `fern/pages/speech-to-text/universal-streaming/streaming-diarization-and-multichannel.mdx` | 683, 1197 |
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

**Pattern B — Raw JavaScript** (`const formatted = data.turn_is_formatted` → `if (formatted):`):

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

**Pattern C — Python SDK** (`if event.turn_is_formatted:`):

| File | Lines |
|------|-------|
| `fern/pages/getting-started/transcribe-streaming-audio.mdx` | 1277 |
| `fern/pages/speech-to-text/universal-streaming/universal-streaming-keyterms.mdx` | 597 |
| `fern/pages/speech-to-text/universal-streaming/streaming-diarization-and-multichannel.mdx` | 1523 |
| `fern/pages/guides/cookbooks/streaming-stt/v2_to_v3.mdx` | 383 |
| `fern/pages/guides/cookbooks/streaming-stt/v2_to_v3_js.mdx` | 397 |
| `fern/pages/use-cases/medical-scribe-best-practices.mdx` | 581, 584 |

**Pattern D — Broken logic: `if event.end_of_turn and not event.turn_is_formatted:`** (condition will never fire because `turn_is_formatted` is now always `true`):

| File | Lines |
|------|-------|
| `fern/pages/guides/cookbooks/streaming-stt/noise_reduction_streaming.mdx` | 70, 177 |
| `fern/pages/guides/cookbooks/streaming-stt/terminate_realtime_programmatically.mdx` | 60, 177 |

### Files — Outdated Prose (Expanded Scope)

| File | Line | What's wrong |
|------|------|--------------|
| `fern/pages/use-cases/voice-agent-best-practices.mdx` | 512 | Claims `end_of_turn` and `turn_is_formatted` always match on U3-Pro — needs broadening to all streaming models, and a warning that `turn_is_formatted` is not a turn-end signal |
| `fern/pages/guides/cookbooks/streaming-stt/universal_to_u3_pro_streaming.mdx` | 59 | Comparison table row describes old English model behavior (separate formatting message) |

---

## What Changed (Technical Summary)

| Field / Behavior | Old | New |
|---|---|---|
| `turn_is_formatted` | `true` only on the final "formatting" message appended after `end_of_turn: true` | `true` on **every** Turn message (partials + finals) when `format_turns=true` |
| Partial turn messages | Always `turn_is_formatted: false` | `turn_is_formatted: true` (formatted inline by model) |
| Final turn message | `turn_is_formatted: false` on `end_of_turn: true`, then a **second message** with `turn_is_formatted: true` | Single `end_of_turn: true` message with `turn_is_formatted: true` — **no separate formatting message** |
| Formatting mechanism | Secondary post-processing service (added latency); only received finalized turns | In-model; zero additional latency |
| `format_turns` default | `false` — formatting was opt-in | **`true`** — formatting is on by default; set `format_turns=false` to opt out |
| `format_turns=false` | Returns unformatted output | Still returns unformatted output (routes through "unformatter" service — unchanged for callers) |

**Critical for customers:** Anyone using `turn_is_formatted=true` as a proxy for detecting end-of-turn will break. `end_of_turn` is the correct and only reliable signal.

**Default change:** `format_turns` now defaults to `true`. Customers who have not set this parameter will now receive formatted output. Customers who want unformatted output must explicitly set `format_turns=false`.

---

## Specific Changes Needed Per File

### 1. `universal-streaming-overview.mdx` — Main Page

#### A. `turn_is_formatted` field definition (line 837)

**Current text:**
> `turn_is_formatted`: Boolean indicating if the text in the transcript field is formatted. Text formatting is enabled when `format_turns` is set to `true`. It adds punctuation as well as performs casing and inverse text normalization to display various entities, such as dates, times, and phone numbers, in a human-friendly format

**What's wrong:** No indication that `turn_is_formatted` is now `true` on partials, not just finals. The old implicit meaning (formatted = final) is no longer true.

**What to add:**

- Clarify that with `universal-streaming-english`, `turn_is_formatted` will be `true` on every message (partial and final) when `format_turns=true`. Do **not** use it to detect end-of-turn; use `end_of_turn` instead.
- Add a note covering `format_turns=false`: when set to `false`, output routes through an unformatter service and all results — partial and final — are returned without punctuation or casing for the entire session. `turn_is_formatted` will be `false` on all messages. This behavior is unchanged.

---

#### B. Immutable transcription section (lines 862–869)

**Current text:**
> When an end of the current turn is detected, you then receive a message with `end_of_turn` being `true`. Additionally, if you enable text formatting, you will also receive a transcription response with `turn_is_formatted` being `true`.
>
> ```
> → hello my name is zack (unformatted)
> → Hello my name is Zack. (formatted)
> ```

**What's wrong:** This implies a two-step message sequence where (1) an unformatted `end_of_turn=true` message arrives, then (2) a separate `turn_is_formatted=true` message arrives. This is the old secondary-service model. It is no longer accurate for `universal-streaming-english`.

**What's needed:** Update the explanation and example. The example should show that partial results are already formatted, and the `end_of_turn=true` message is itself formatted. There is no separate trailing formatting message.

---

#### C. Quickstart code examples — Python (lines 234–241) and JavaScript (lines 595–601)

**Current logic in both examples:**
```python
if formatted:  # turn_is_formatted
    print('\r' + ' ' * 80 + '\r', end='')
    print(transcript)
else:
    print(f"\r{transcript}", end='')
```

**What's wrong:** Both examples use `turn_is_formatted` to decide whether to print on a new line (final) vs. overwrite the current line (partial). With the new model, `turn_is_formatted` is `true` on every message, so every partial would print on its own new line — breaking the intended UX.

**What's needed:** The examples need to switch to using `end_of_turn` to distinguish final from partial turns. For example:
```python
if data.get('end_of_turn'):
    print('\r' + ' ' * 80 + '\r', end='')
    print(transcript)
else:
    print(f"\r{transcript}", end='')
```
This is also the customer-facing migration guidance they need.

---

### 2. `universal-streaming-messages.mdx` — Message Sequence

#### A. "End of turn formatting" sections — both occurrences (lines 342–395 and lines 748–799)

**Current text (first occurrence, line 344):**
> Once the turn ends, if formatting is enabled there will be an additional message where `"turn_is_formatted":True` comes back. This will format the final message.
>
> Since LLMs can parse unformatted text, waiting for this message is NOT recommended for voice agents as it adds additional latency. It is recommended for other use cases like closed captioning where the transcript will be displayed to the end user.

**What's wrong:**
1. The "additional message" framing is entirely the old model. With the new model, `turn_is_formatted: true` is on the `end_of_turn: true` message itself — there is no second trailing message.
2. The "adds additional latency" rationale was tied to the secondary service. With in-model formatting, there is no added latency for partials. (A note about voice agent latency may still be appropriate, but the mechanism is different.)

**What's needed:**
- Remove or replace both "End of turn formatting" sections. There is no longer a separate trailing message; the `end_of_turn: true` message is itself `turn_is_formatted: true`.
- Update the latency note: formatting no longer adds latency because it is done in-model.
- The two example JSON payloads showing the "formatting message" with `turn_is_formatted: true` arriving after `end_of_turn: true` need to be revised to show that the `end_of_turn: true` message itself is formatted, with no additional message following.

---

#### B. All partial turn JSON examples (throughout the file)

**Current state:** All partial turn messages show `"turn_is_formatted": false` (lines 57, 79, 103, 138, 181, 229, 403, 424, 451, 488, 529, 578, 638, 699).

**What's needed:** All partial turn JSON examples need to be updated to `"turn_is_formatted": true` to reflect the new behavior.

---

#### C. Best practices — "Avoid using `format_turns`" (line 807)

**Current text:**
> Avoid using `format_turns` as it will significantly increase latency. LLMs don't need formatting so you can just pass raw text as soon as its ready.

**What's wrong:** The latency concern was based on the secondary service. With in-model formatting, `format_turns` no longer significantly increases latency. The general advice (voice agents can skip formatting) may still apply, but the reason has changed.

**What's needed:** Update or remove the latency claim. Voice agent recommendation to skip formatting may still be appropriate for other reasons (LLMs don't need it), but "significantly increase latency" is no longer accurate.

---

### 3. `turn-detection.mdx` — Turn Detection Page

This page currently does not mention `turn_is_formatted` at all. The existing content correctly centers `end_of_turn` as the detection signal.

**What's needed:**
- Add an explicit callout or note that `end_of_turn` is the **canonical and only reliable signal** for detecting turn end.
- Clarify that `turn_is_formatted` should **not** be used for this purpose — it will now be `true` on every turn message (partial and final) when `format_turns=true` with `universal-streaming-english`.

**Suggested placement:** Near the top of the "Overview" section or as a note in the "Important notes" section (after line 160).

---

### 4. `multilingual.mdx` — "Understanding formatting" (multilingual model section, lines 731–742)

**Current text:**
> The multilingual model produces transcripts with punctuation and capitalization already built into the model outputs. [...] While the API still returns the `turn_is_formatted` parameter to maintain interface consistency with other streaming models, the multilingual model doesn't perform additional formatting operations. All transcripts from the multilingual model are already formatted as they're generated.
>
> In the future, this built-in formatting capability will be extended to our English-only streaming model as well.

**What's wrong:**
- The last sentence ("In the future, this built-in formatting capability will be extended to our English-only streaming model as well.") is now false — the rollout is happening now, not in the future.

**What's needed:**
- Remove or update that sentence. Replace with language indicating the `universal-streaming-english` model now also applies formatting natively (rollout complete / in progress), making this consistent behavior across all streaming models.

---

## Existing Patterns

### How `turn_is_formatted` is used in code examples (old pattern, now wrong)
```python
# overview page — Python quickstart (line 234-241)
formatted = data.get('turn_is_formatted', False)
if formatted:
    print('\r' + ' ' * 80 + '\r', end='')
    print(transcript)   # new line for final formatted turn
else:
    print(f"\r{transcript}", end='')  # overwrite for partial
```

### Recommended new pattern (using `end_of_turn`)
```python
end_of_turn = data.get('end_of_turn', False)
if end_of_turn:
    print('\r' + ' ' * 80 + '\r', end='')
    print(transcript)
else:
    print(f"\r{transcript}", end='')
```

### How the U3-Pro page handles `turn_is_formatted` (reference, not in scope)
`fern/pages/speech-to-text/universal-streaming/u3-pro-message-sequence.mdx` — U3-RT-Pro already shows `turn_is_formatted: true` on end-of-turn consistently. Not in scope for this change but validates the "formatted on final" pattern that now applies to universal-streaming-english too.

---

## Constraints & Dependencies

- **Rollout state:** 25% → 100% imminent. Changes should be written as if fully rolled out (no "in beta" / "some users" hedging).
- **`format_turns=false` unchanged:** Customers who set `format_turns=false` will continue to receive unformatted output. This path is unaffected.
- **No diagram assets:** The message sequence page uses JSON payloads, not graphical diagrams, so no images need updating — only text and JSON examples.
- **Whisper-RT not affected:** The "Understanding formatting" section for Whisper Streaming (`multilingual.mdx` lines 836–849) describes a different model and is unaffected by this rollout. The latency warning for Whisper-RT formatting can remain.
- **Multilingual model not affected:** `universal-streaming-multilingual` already had native formatting. Only the sentence claiming English-only is "in the future" needs to be removed.
- **Customer impact (Airgram pattern):** The highest-risk customer pattern is: listen for `turn_is_formatted=true`, treat it as end-of-turn signal, fire downstream logic. This pattern breaks immediately at 100% rollout. The warning and migration guidance in the docs must be prominent.

---

## API Definition Files

Two Fern definition files also need updates. These drive the generated API reference.

### `fern/.definition/universalStreaming.yml` — `format_turns` parameter (line 134)

**Current:**

```yaml
format_turns:
  default: "false"
  docs: Whether to return formatted final transcripts.
  type: optional<StreamingFormatTurns>
```

**New `docs` value:**

```yaml
docs: Whether to return formatted transcripts. When enabled, formatting is applied to all turns — including partial results — not just final turns.
```

### `fern/.definition/__package__.yml` — `turn_is_formatted` field in `TurnPayload` (lines 609–612)

**Current:**

```yaml
turn_is_formatted:
  docs: >-
    Whether this turn has been formatted. For Universal-3 Pro Streaming,
    this always matches `end_of_turn`.
  type: boolean
```

**New `docs` value:**

```yaml
docs: >-
  Whether this turn has been formatted. When `format_turns=true`, this is `true` on all turns — including partial results — and should not be used as an end-of-turn signal. Use `end_of_turn` to detect when a turn has completed.
```
