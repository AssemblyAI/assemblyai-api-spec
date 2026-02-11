# Code Block Extraction Plan

Extract inline code blocks from ~165 MDX files into separate native-language files (`.py`, `.js`, `.cs`, `.rb`, etc.) and reference them via Fern's `<Code src="...">` component.

## Design Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Multi-language code display | `<CodeBlocks>` wrapping `<Code src>` | Fern's native tabbed code display. Auto-syncs language preference site-wide. Cleaner than `<Tabs>/<Tab>`. |
| Tabs with prose + code | Keep `<Tabs>/<Tab>`, extract code to `<Code src>` | Prose is tab-specific and must stay inside the Tab. Only the code gets extracted. |
| File placement | Sibling `snippets/` directory per section | e.g., `fern/pages/audio-intelligence/snippets/auto-chapters/quickstart.python-sdk.py` |
| Short code blocks (1-2 lines) | Leave inline | Install commands, single config lines stay as triple-backtick. Extract blocks >= 3 lines. |
| `<Json>` components | Leave as-is | Already in separate `*-response.mdx` files. JSX syntax not suitable for `.json` extraction. |
| Commented-out code | Extract file, comment the `<Code>` reference | Preserves code for future use while keeping it hidden. |

---

## Component Standardization Rules

### Rule 1: Multi-language groups (code only) → `<CodeBlocks>` + `<Code src>`

**Before** (current `<Tabs>` pattern, code only):
```jsx
<Tabs groupId="language">
  <Tab language="python-sdk" title="Python SDK" default>
```python {8}
import assemblyai as aai
...
```
  </Tab>
  <Tab language="javascript-sdk" title="JavaScript SDK">
```javascript {12}
import { AssemblyAI } from "assemblyai";
...
```
  </Tab>
</Tabs>
```

**After**:
```jsx
<CodeBlocks>
  <Code
    src="./snippets/auto-chapters/quickstart.python-sdk.py"
    title="Python SDK"
    language="python"
    highlight="{8}"
  />
  <Code
    src="./snippets/auto-chapters/quickstart.javascript-sdk.js"
    title="JavaScript SDK"
    language="javascript"
    highlight="{12}"
  />
</CodeBlocks>
```

### Rule 2: Multi-language groups (prose + code) → Keep `<Tabs>`, extract code

**Before**:
```jsx
<Tabs groupId="language">
  <Tab language="python-sdk" title="Python SDK" default>
  Enable Auto Chapters by setting `auto_chapters` to `True`.
```python {8}
import assemblyai as aai
...
```
  </Tab>
</Tabs>
```

**After**:
```jsx
<Tabs groupId="language">
  <Tab language="python-sdk" title="Python SDK" default>
  Enable Auto Chapters by setting `auto_chapters` to `True`.
  <Code
    src="./snippets/auto-chapters/quickstart.python-sdk.py"
    language="python"
    highlight="{8}"
  />
  </Tab>
</Tabs>
```

### Rule 3: Existing `<CodeBlocks>` with inline fences → `<CodeBlocks>` + `<Code src>`

**Before**:
```jsx
<CodeBlocks>
```python title="Python SDK" highlight={17} maxLines=15
import assemblyai as aai
...
```
```javascript title="JavaScript SDK" highlight={19} maxLines=15
import { AssemblyAI } from "assemblyai";
...
```
</CodeBlocks>
```

**After**:
```jsx
<CodeBlocks>
  <Code
    src="./snippets/delete-transcripts/quickstart.python-sdk.py"
    title="Python SDK"
    language="python"
    highlight="{17}"
    maxLines={15}
  />
  <Code
    src="./snippets/delete-transcripts/quickstart.javascript-sdk.js"
    title="JavaScript SDK"
    language="javascript"
    highlight="{19}"
    maxLines={15}
  />
</CodeBlocks>
```

### Rule 4: Standalone blocks >= 3 lines → `<Code src>`

**Before**:
```markdown
```python
import assemblyai as aai
aai.settings.api_key = "YOUR_API_KEY"
transcript = aai.Transcriber().transcribe(audio_file)
```
```

**After**:
```jsx
<Code
  src="./snippets/batch-transcription/quickstart.py"
  language="python"
/>
```

### Rule 5: Short blocks (< 3 lines) → Leave inline

```markdown
```bash
pip install -U assemblyai
```
```
Stays as-is.

### Rule 6: Commented-out code → Extract file, comment the reference

**Before**:
```jsx
{/* <Tab language="python" title="Python SDK">
```python
import assemblyai as aai
...
```
</Tab> */}
```

**After** (extract the code to a file, comment the `<Code>` reference):
```jsx
{/* <Code
  src="./snippets/translation/quickstart.python-sdk.py"
  title="Python SDK"
  language="python"
/> */}
```

---

## File Naming Convention

**Format**: `{section}.{variant}.{ext}` or `{section}.{ext}` (no variant for single-language)

| Component | Description | Example |
|---|---|---|
| `{section}` | Semantic slug for what the code block does | `quickstart`, `api-request`, `step1-setup`, `enable-feature`, `example-output` |
| `{variant}` | Language/SDK variant, matching Tab `language` attribute | `python-sdk`, `python`, `javascript-sdk`, `javascript`, `csharp`, `ruby`, `php`, `java`, `golang` |
| `{ext}` | Native file extension | `.py`, `.js`, `.cs`, `.rb`, `.php`, `.java`, `.go`, `.sh`, `.json`, `.txt`, `.yml`, `.ts` |

**Examples**:
```
snippets/auto-chapters/quickstart.python-sdk.py
snippets/auto-chapters/quickstart.javascript-sdk.js
snippets/auto-chapters/quickstart.csharp.cs
snippets/auto-chapters/api-request.sh
snippets/auto-chapters/example-output.txt
snippets/batch-transcription/quickstart.py        # single-language, no variant
snippets/batch-transcription/step1-setup.py
snippets/aws-to-aai/comparison.aws.py             # competitor migration
snippets/aws-to-aai/comparison.aai.py
```

**Directory structure**:
```
fern/pages/audio-intelligence/
  auto-chapters.mdx
  auto-chapters-response.mdx          # untouched (uses <Json>)
  content-moderation.mdx
  snippets/
    auto-chapters/
      quickstart.python-sdk.py
      quickstart.python.py
      quickstart.javascript-sdk.js
      quickstart.javascript.js
      quickstart.csharp.cs
      quickstart.ruby.rb
      quickstart.php.php
      api-request.sh
      example-output.txt
    content-moderation/
      quickstart.python-sdk.py
      ...
```

**Language → Extension mapping**:

| Language/Fence | Extension |
|---|---|
| `python` | `.py` |
| `javascript` / `typescript` | `.js` / `.ts` |
| `csharp` | `.cs` |
| `ruby` | `.rb` |
| `php` | `.php` |
| `java` | `.java` |
| `go` / `golang` | `.go` |
| `bash` / `sh` / `curl` | `.sh` |
| `json` | `.json` |
| `yaml` / `yml` | `.yml` |
| `plain` / `text` / `txt` | `.txt` |
| `nginx` | `.conf` |

---

## `src` Path Resolution

Fern's `<Code>` component resolves `src` paths relative to the Fern docs directory (`fern/`). So for:
- MDX file: `fern/pages/audio-intelligence/auto-chapters.mdx`
- Code file: `fern/pages/audio-intelligence/snippets/auto-chapters/quickstart.python-sdk.py`

The `src` should be: `pages/audio-intelligence/snippets/auto-chapters/quickstart.python-sdk.py`

**Important**: This must be verified during the first actual extraction PR. If Fern resolves relative to the MDX file instead, paths would be `./snippets/auto-chapters/quickstart.python-sdk.py`.

---

## PR Splitting Strategy (~10 PRs)

| PR | Section | ~Files | Notes |
|---|---|---|---|
| **PR 1** | `audio-intelligence/` | 8 | Most consistent pattern (all Tabs with 7 langs). Skip `*-response.mdx` files. |
| **PR 2** | `speech-to-text/pre-recorded-audio/` | 21 | Mix of CodeBlocks (17) and Tabs (4). |
| **PR 3** | `speech-to-text/` remaining (streaming, universal-streaming, pipecat, livekit) | 18 | Includes `streaming.mdx` (very heavy, 9 Tabs groups). |
| **PR 4** | `getting-started/` + `lemur/` | 10 | High-traffic pages; test carefully. |
| **PR 5** | `llm-gateway/` + `speech-understanding/` | 10 | Includes commented-out Tab edge case (3 files). |
| **PR 6** | `guides/` top-level (not cookbooks) | 15 | Longer guides with multiple code groups per file. |
| **PR 7a** | `guides/cookbooks/core-transcription/` + `streaming-stt/` | ~51 | Mostly standalone Python-only code. |
| **PR 7b** | `guides/cookbooks/lemur/` + `audio-intelligence/` | ~16 | Standalone Python cookbooks. |
| **PR 8** | `integrations/` + `use-cases/` + `concepts/` + misc | ~31 | Everything remaining. |

---

## Verification Checklist (Per PR)

1. **All referenced files exist**: Grep for `<Code src=` and verify each path resolves
2. **No orphaned extractable code blocks**: Grep for triple-backtick blocks >= 3 lines that should have been extracted
3. **Code content preserved**: Diff extracted file content against original inline code
4. **Fern preview build**: Run `fern generate --docs --preview` to verify rendering
5. **Visual spot-check**: Open 3-5 pages and verify tabs work, syntax highlighting renders, highlight lines are correct

---

## How to Run the Extraction

Use the reusable LLM prompt at `scripts/extract-code-blocks-prompt.md`. For each file or batch of files:

1. Copy the prompt into a Claude Code session
2. Provide the MDX file path(s) for the section you're working on
3. The LLM will read each file, extract code blocks, create snippet files, and update the MDX
4. Run verification checks before committing

See the prompt file for full instructions and examples.
