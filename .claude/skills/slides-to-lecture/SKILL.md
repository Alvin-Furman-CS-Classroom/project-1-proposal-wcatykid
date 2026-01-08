# Slides to Lecture Converter

Convert pre-exported slide images into PathMX `.lecture.md` markdown files using vision analysis to extract conceptual content.

## When to Use

Use this skill when the user wants to:
- Convert exported slide images to PathMX lecture format
- Create markdown-based lecture content from visual presentations
- Extract the conceptual "spine" of a presentation (not literal transcription)

## Input Format

The skill expects a folder containing exported slide images:
- Images should be named with numeric ordering (e.g., `Slide1.png`, `Slide2.png`, ... or `slide_001.png`, `slide_002.png`, ...)
- Supported formats: PNG, JPG, JPEG
- Export slides from PowerPoint: File → Export → Change File Type → PNG

Example folder structure:
```
admin/materials/1 Propositonal Logic/
├── Slide1.png
├── Slide2.png
├── Slide3.png
...
└── Slide64.png
```

## Duplicate Detection

Before processing, check if this lecture has already been converted:

1. Derive the expected output filename from the source folder name
2. Check if `paths/lectures/[topic].lecture.md` already exists
3. If it exists, read the frontmatter to verify it matches the source

**If already converted:**
- Inform the user: "This lecture has already been converted to `paths/lectures/[topic].lecture.md`"
- Ask if they want to reconvert (overwrite) or skip
- Only proceed if user explicitly confirms reconversion

**To force reconversion**, the user should say something like:
- "reconvert the propositional logic slides"
- "regenerate the lecture file"
- "overwrite the existing lecture"

## Process

### Step 1: Check for existing conversion

Before processing slides:
1. Determine output path: `paths/lectures/[topic].lecture.md`
2. If file exists, stop and ask user for confirmation before overwriting

### Step 2: Locate slide images

Given a folder path, find all image files and sort them by slide number:
- Parse the numeric portion of filenames to determine order
- Handle both `SlideN.png` and `slide_NNN.png` naming conventions

### Step 2: Analyze each slide with vision

For each slide image:

1. Read the image using the Read tool (Claude has native vision support)
2. Apply the prompt template from `.claude/skills/slides-to-lecture/prompts/ai-slides.prompt.md`
3. Extract the YAML response with concept name, summary, key ideas, etc.

### Step 3: Assemble the .lecture.md file

Combine all slide analyses into a single markdown file:

1. **YAML frontmatter** with title, source folder, conversion date, type
2. **Overview paragraph** synthesizing the lecture's purpose
3. **Slide sections** separated by `---` thematic breaks
4. Each section has a concept-based heading (not "Slide N")

### Step 4: Copy slide images

Copy all slide images to a local subdirectory:
1. Create `paths/lectures/[topic]/slides/` directory
2. Copy all slide images from source folder to this directory
3. This keeps assets co-located with the lecture file

Example:
```
paths/lectures/
├── propositional-logic.lecture.md
└── propositional-logic/
    └── slides/
        ├── Slide1.png
        ├── Slide2.png
        └── ...
```

### Step 5: Write output

Save to `paths/lectures/[topic].lecture.md` where topic is derived from the source folder name:
- "1 Propositonal Logic" → "propositional-logic.lecture.md"
- "2 Uninformed Search" → "uninformed-search.lecture.md"

## Output Format

```markdown
---
title: "Propositional Logic"
source: "admin/materials/1 Propositonal Logic"
download: "../materials/1 Propositonal Logic.pptx"
converted: "2026-01-08"
type: lecture
slides: 64
---

# Propositional Logic

> **[Download PowerPoint][pptx]**

Brief overview paragraph describing the lecture's core purpose and what students will learn.

---

## Logic in AI: Historical Overview

[Title slide introducing the historical context of logic in AI.] [1]

---

## Knowledge Representation in AI

Conceptual summary of what this slide teaches, focusing on ideas not literal text.

**Key Ideas:**
- First conceptual point
- Second conceptual point

[2]

---

## Propositional Syntax

Next concept section continues...

**Key Ideas:**
- Atomic propositions and connectives
- Recursive sentence construction

[3]

---

[... additional slides ...]

[pptx]: ../../materials/1%20Propositonal%20Logic.pptx
[1]: ./propositional-logic/slides/Slide1.png
[2]: ./propositional-logic/slides/Slide2.png
[3]: ./propositional-logic/slides/Slide3.png
```

### Link Definition Notes

- **PowerPoint link**: `[pptx]` links to original presentation in materials folder
- **Slide references**: Each section ends with `[N]` linking to the local slide image copy
- **Clean paths**: Images are co-located in `./[topic]/slides/` for portability
- **Player integration**: Renderers can use these references to display slide images alongside content

## Handling Special Slides

- **Title slides**: Include as the document title/header, skip as separate section
- **Transition slides**: Can be condensed or merged with following content
- **Diagram-heavy slides**: Describe the diagram conceptually, note if recreation recommended
- **Example slides**: Mark as examples, preserve the pedagogical intent
- **Continuation slides**: Merge with previous slide's content when a concept spans multiple slides

## Error Handling

- If the folder doesn't exist, report the error clearly
- If no images are found in the folder, report available file types
- If a slide image fails to process, note it and continue with remaining slides
