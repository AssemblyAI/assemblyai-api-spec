# Extract Code Blocks — Reusable LLM Prompt

## How to Use This Prompt

### Option A: Process a single file
```
Claude, read the file at [MDX_FILE_PATH] and follow the instructions in scripts/extract-code-blocks-prompt.md to extract its code blocks.
```

### Option B: Process an entire section
```
Claude, process all MDX files in fern/pages/audio-intelligence/ following the instructions in scripts/extract-code-blocks-prompt.md. Skip any *-response.mdx files.
```

### Option C: Process a list of specific files
```
Claude, process these files following the instructions in scripts/extract-code-blocks-prompt.md:
- fern/pages/audio-intelligence/auto-chapters.mdx
- fern/pages/audio-intelligence/content-moderation.mdx
- fern/pages/audio-intelligence/entity-detection.mdx
```

---

## Extraction Instructions

You are extracting inline code blocks from MDX documentation files into separate native-language files and replacing them with Fern `<Code src="...">` references. Read the plan at `docs/code-extraction-plan.md` for full context.

### Step 1: Read the MDX file

Read the complete file content. Identify every code block by scanning for:
- Triple-backtick fenced code blocks (` ``` `)
- Code blocks inside `<Tabs>` / `<Tab>` components
- Code blocks inside `<CodeBlocks>` components
- Code blocks inside JSX comments (`{/* ... */}`)
- Code blocks inside `<Accordion>`, `<Step>`, or other wrapper components

Do NOT touch:
- `<Json>` components (leave completely as-is)
- `<Markdown src="...">` includes (leave as-is)
- Inline code (single backticks)
- Non-code content (prose, callouts, tables, etc.)

### Step 2: Classify each code block

For each code block, determine:

1. **Wrapper type**: `Tabs` (inside `<Tabs>`/`<Tab>`), `CodeBlocks` (inside `<CodeBlocks>`), `standalone` (no wrapper), or `commented-out` (inside `{/* */}`)
2. **Language**: From the fence language identifier (e.g., `python`, `javascript`, `bash`, `json`)
3. **Variant**: From the Tab's `language` attribute or the code block's `title` attribute (e.g., `python-sdk`, `javascript-sdk`, `csharp`)
4. **Attributes**: `highlight`, `maxLines`, `wordWrap`, `title` values
5. **Has surrounding prose**: Whether the Tab/wrapper contains prose text alongside the code (not just the code block)
6. **Line count**: Number of lines in the code block
7. **Section purpose**: A semantic slug describing what this code block does in the context of the page (e.g., `quickstart`, `api-request`, `enable-feature`, `step1-setup`, `example-output`)

### Step 3: Decide what to extract

**EXTRACT** (create external file):
- Any code block >= 3 lines
- Any code block inside a `<Tabs>` or `<CodeBlocks>` wrapper (even if < 3 lines, for consistency within the group)
- Commented-out code blocks (still extract the file)

**LEAVE INLINE** (do not extract):
- Code blocks < 3 lines that are standalone (not in Tabs/CodeBlocks), such as:
  - `pip install assemblyai`
  - `npm install assemblyai`
  - Single config lines
- `<Json>` components
- Inline code (single backticks)
- Plain text blocks that are just URLs or short strings

### Step 4: Determine file paths

For each code block to extract, compute the file path:

**Directory**: `{mdx_dir}/snippets/{page_name}/`
- `{mdx_dir}` = directory containing the MDX file
- `{page_name}` = MDX filename without `.mdx` extension, using hyphens (e.g., `auto-chapters`)

**Filename**: `{section}.{variant}.{ext}` or `{section}.{ext}`
- `{section}` = semantic slug for the code block's purpose (e.g., `quickstart`, `api-request`, `step1-setup`)
- `{variant}` = language/SDK variant identifier (omit for single-language standalone blocks):
  - `python-sdk`, `python`, `javascript-sdk`, `javascript`, `csharp`, `ruby`, `php`, `java`, `golang`
  - For competitor migration pages: `aws`, `dg`, `gladia`, `google`, `openai`, `aai`
- `{ext}` = native file extension based on the fence language

**Extension mapping**:
| Fence language | Extension |
|---|---|
| `python` | `.py` |
| `javascript` | `.js` |
| `typescript` | `.ts` |
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
| `xml` | `.xml` |
| `html` | `.html` |
| `css` | `.css` |
| `sql` | `.sql` |

**Assigning section slugs**: When a page has multiple distinct groups of code blocks (e.g., a "Quickstart" section and a "Get subtitles" section), assign unique slugs based on the surrounding heading or the purpose of the code. Common slugs:
- `quickstart` — the main/first example on the page
- `enable-feature` — code that enables a specific feature
- `api-request` — a curl/HTTP request example
- `api-response` — an API response example
- `example-output` — sample output text
- `step1-setup`, `step2-transcribe`, `step3-results` — for step-by-step guides
- `{feature-name}` — when the code demonstrates a sub-feature (e.g., `speaker-filter`, `word-search`)

When multiple code block groups exist on one page and they all serve similar purposes in different sections, use the section heading as the slug (kebab-case).

### Step 5: Create the snippet files

For each code block to extract:
1. Create the directory if it doesn't exist: `mkdir -p {mdx_dir}/snippets/{page_name}/`
2. Write the code content to the file — extract ONLY the code, not the fence markers or attributes
3. Preserve the exact code content (indentation, comments, blank lines)
4. Do NOT add any headers, comments, or metadata to the snippet file — just the raw code

### Step 6: Update the MDX file

Apply these transformation rules:

#### Rule 1: `<Tabs>` with code-only Tabs → `<CodeBlocks>` + `<Code src>`

If ALL tabs in a `<Tabs>` group contain ONLY a code block (no prose, no callouts, no other content), replace the entire `<Tabs>` structure:

```jsx
<CodeBlocks>
  <Code
    src="./snippets/{page_name}/{section}.{variant}.{ext}"
    title="{Tab title}"
    language="{fence_language}"
    highlight="{highlight_value}"
  />
  <Code
    src="./snippets/{page_name}/{section}.{variant2}.{ext2}"
    title="{Tab title 2}"
    language="{fence_language_2}"
  />
</CodeBlocks>
```

Notes:
- Transfer `title` from the Tab's `title` attribute
- Transfer `highlight` from the code fence's `{N}` or `highlight={N}` attribute
- Transfer `maxLines` from the code fence
- Do NOT include `groupId` — `<CodeBlocks>` handles language sync automatically
- Only include attributes that were present on the original code block

#### Rule 2: `<Tabs>` with prose + code → Keep `<Tabs>`, use `<Code src>` inside

If ANY tab contains prose or other content alongside the code block, keep the `<Tabs>`/`<Tab>` structure but replace the inline code:

```jsx
<Tabs groupId="language">
  <Tab language="python-sdk" title="Python SDK" default>

  Enable the feature by setting `feature` to `True`.

  <Code
    src="./snippets/{page_name}/{section}.{variant}.{ext}"
    language="{fence_language}"
    highlight="{highlight_value}"
  />

  </Tab>
</Tabs>
```

Notes:
- Keep all Tab attributes (`language`, `title`, `default`)
- Keep all prose/callout content inside the Tab unchanged
- Only replace the code fence with `<Code src>`
- Do NOT add `title` to the `<Code>` when inside a `<Tab>` (the Tab already has the title)

#### Rule 3: Existing `<CodeBlocks>` with inline fences → `<CodeBlocks>` + `<Code src>`

Replace inline fences inside `<CodeBlocks>` with `<Code src>`:

```jsx
<CodeBlocks>
  <Code
    src="./snippets/{page_name}/{section}.{variant}.{ext}"
    title="{fence_title}"
    language="{fence_language}"
    highlight="{highlight_value}"
    maxLines={maxLines_value}
  />
</CodeBlocks>
```

Notes:
- Transfer `title` from the fence's `title="..."` attribute
- Transfer all other attributes

#### Rule 4: Standalone blocks >= 3 lines → `<Code src>`

Replace the fenced code block with:

```jsx
<Code
  src="./snippets/{page_name}/{section}.{ext}"
  language="{fence_language}"
/>
```

Notes:
- No `title` unless the original fence had a `title` attribute
- No variant in the filename (standalone blocks are single-language)

#### Rule 5: Standalone blocks < 3 lines → Leave as-is

Do not modify short standalone code blocks. Leave the triple-backtick fence in place.

#### Rule 6: Commented-out code → Extract file, comment the `<Code>` reference

```jsx
{/* <Code
  src="./snippets/{page_name}/{section}.{variant}.{ext}"
  title="{title}"
  language="{fence_language}"
/> */}
```

### Step 7: Verify your work

After modifying the file, check:

1. Every `<Code src="...">` references a file that was created
2. No extractable code blocks (>= 3 lines, or inside Tabs/CodeBlocks) remain inline
3. All prose, callouts (`<Note>`, `<Warning>`, `<Info>`, `<Tip>`), accordions, steps, cards, and other non-code content is preserved exactly
4. No imports or frontmatter at the top of the MDX file were removed
5. The JSX is valid (all tags properly opened and closed)
6. `<Code>` components have a self-closing tag (`/>`)

---

## Complete Example

### Input: `fern/pages/audio-intelligence/auto-chapters.mdx` (simplified)

```mdx
---
title: "Auto Chapters"
---

import { LanguageTable } from "../../assets/components/LanguagesTable";

## Quickstart

<Tabs groupId="language">
<Tab language="python-sdk" title="Python SDK" default>

Enable Auto Chapters by setting `auto_chapters` to `True` in the transcription config.

```python {8}
import assemblyai as aai

aai.settings.api_key = "<YOUR_API_KEY>"

audio_file = "https://assembly.ai/wildfires.mp3"

config = aai.TranscriptionConfig(
  auto_chapters=True
)

transcript = aai.Transcriber().transcribe(audio_file, config)

for chapter in transcript.chapters:
  print(f"{chapter.start}-{chapter.end}: {chapter.headline}")
```

</Tab>
<Tab language="javascript-sdk" title="JavaScript SDK">

Enable Auto Chapters by setting `auto_chapters` to `true` in the transcription config.

```javascript {10}
import { AssemblyAI } from "assemblyai";

const client = new AssemblyAI({
  apiKey: "<YOUR_API_KEY>",
});

const audioFile = "https://assembly.ai/wildfires.mp3";

const params = {
  audio: audioFile,
  auto_chapters: true,
};

const run = async () => {
  const transcript = await client.transcripts.transcribe(params);
  for (const chapter of transcript.chapters) {
    console.log(`${chapter.start}-${chapter.end}: ${chapter.headline}`);
  }
};

run();
```

</Tab>
</Tabs>

## API reference

```bash
curl https://api.assemblyai.com/v2/transcript \
  --header "Authorization: YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "audio_url": "https://assembly.ai/wildfires.mp3",
    "auto_chapters": true
  }'
```

```plain title="Example output"
250-28840: Smoke from hundreds of wildfires in Canada is triggering air quality alerts
28840-56840: The air quality index in Baltimore is considered unhealthy
```
```

### Output

**Files created**:
- `fern/pages/audio-intelligence/snippets/auto-chapters/quickstart.python-sdk.py`
- `fern/pages/audio-intelligence/snippets/auto-chapters/quickstart.javascript-sdk.js`
- `fern/pages/audio-intelligence/snippets/auto-chapters/api-request.sh`
- `fern/pages/audio-intelligence/snippets/auto-chapters/example-output.txt`

**Modified MDX**:
```mdx
---
title: "Auto Chapters"
---

import { LanguageTable } from "../../assets/components/LanguagesTable";

## Quickstart

<Tabs groupId="language">
<Tab language="python-sdk" title="Python SDK" default>

Enable Auto Chapters by setting `auto_chapters` to `True` in the transcription config.

<Code
  src="./snippets/auto-chapters/quickstart.python-sdk.py"
  language="python"
  highlight="{8}"
/>

</Tab>
<Tab language="javascript-sdk" title="JavaScript SDK">

Enable Auto Chapters by setting `auto_chapters` to `true` in the transcription config.

<Code
  src="./snippets/auto-chapters/quickstart.javascript-sdk.js"
  language="javascript"
  highlight="{10}"
/>

</Tab>
</Tabs>

## API reference

<Code
  src="./snippets/auto-chapters/api-request.sh"
  language="bash"
/>

<Code
  src="./snippets/auto-chapters/example-output.txt"
  language="plain"
  title="Example output"
/>
```

**Snippet file contents**:

`snippets/auto-chapters/quickstart.python-sdk.py`:
```python
import assemblyai as aai

aai.settings.api_key = "<YOUR_API_KEY>"

audio_file = "https://assembly.ai/wildfires.mp3"

config = aai.TranscriptionConfig(
  auto_chapters=True
)

transcript = aai.Transcriber().transcribe(audio_file, config)

for chapter in transcript.chapters:
  print(f"{chapter.start}-{chapter.end}: {chapter.headline}")
```

`snippets/auto-chapters/quickstart.javascript-sdk.js`:
```javascript
import { AssemblyAI } from "assemblyai";

const client = new AssemblyAI({
  apiKey: "<YOUR_API_KEY>",
});

const audioFile = "https://assembly.ai/wildfires.mp3";

const params = {
  audio: audioFile,
  auto_chapters: true,
};

const run = async () => {
  const transcript = await client.transcripts.transcribe(params);
  for (const chapter of transcript.chapters) {
    console.log(`${chapter.start}-${chapter.end}: ${chapter.headline}`);
  }
};

run();
```

`snippets/auto-chapters/api-request.sh`:
```bash
curl https://api.assemblyai.com/v2/transcript \
  --header "Authorization: YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "audio_url": "https://assembly.ai/wildfires.mp3",
    "auto_chapters": true
  }'
```

`snippets/auto-chapters/example-output.txt`:
```
250-28840: Smoke from hundreds of wildfires in Canada is triggering air quality alerts
28840-56840: The air quality index in Baltimore is considered unhealthy
```

---

## Edge Case Reference

### Tabs without `groupId`
Some `<Tabs>` lack `groupId="language"`. If the tabs represent language variants, convert to `<CodeBlocks>`. If they represent non-language grouping (OS/platform), keep `<Tabs>`/`<Tab>` but still extract code to `<Code src>`.

### Tabs with `<Info>`, `<Warning>`, `<Note>` inside
These count as "prose" — keep the `<Tabs>`/`<Tab>` structure (Rule 2).

### Tabs with `<Steps>` + `<Step>` inside
If Steps contain code blocks >= 3 lines, extract them. If Steps contain 1-2 line install commands, leave inline.

### Multiple `<Tabs>` groups on one page
Assign unique section slugs based on the surrounding heading or purpose (e.g., `quickstart` for the first, `speaker-filter` for a later section).

### `title=` on code fences inside `<CodeBlocks>`
Transfer the `title` to the `<Code>` component's `title` attribute.

### Code blocks with `wordWrap`
Transfer as `wordWrap` attribute on `<Code>`.

### `python-sdk` vs `python` variants
These are DIFFERENT variants. `python-sdk` uses the AssemblyAI Python SDK (`import assemblyai as aai`). `python` uses raw `requests`/`urllib`. They get separate files.

### Code inside `<Accordion>` components
Extract code from within Accordions the same way as standalone code. The `<Accordion>` wrapper stays.
