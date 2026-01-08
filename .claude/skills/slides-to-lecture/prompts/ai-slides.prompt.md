# Slide Analysis Prompt

You are analyzing a lecture slide to extract its conceptual content for conversion to a PathMX `.lecture.md` file.

## Context

This slide is from a CSC-343 Artificial Intelligence course at Furman University. The goal is NOT to transcribe the slide literally, but to extract the **conceptual spine** -- the underlying ideas and teaching intent.

## Your Task

Analyze this slide image and provide:

### 1. Concept Name
A brief, descriptive name for what this slide teaches. Use a real concept name like "Resolution Inference" or "A* Heuristic Requirements" -- NOT generic labels like "Introduction" or "Slide 5".

If this is a title slide, section divider, or transition slide, indicate that with `slide_type: title` or `slide_type: transition`.

### 2. Conceptual Summary
2-4 sentences explaining what this slide is teaching. Focus on:
- The core concept or idea being presented
- Why this matters in the context of AI
- How it connects to broader themes

### 3. Key Ideas
Extract 2-5 key conceptual points. These should be:
- Ideas, not bullet point transcriptions
- Complete thoughts that would make sense standalone
- Ordered by conceptual importance, not slide position

### 4. Visual Elements (if applicable)
If the slide contains diagrams, graphs, code, or other visual elements that convey meaning:
- Describe what they illustrate conceptually
- Note any relationships or flows shown
- Mention if a figure would be valuable to recreate

### 5. Prerequisite Concepts
List any concepts that a reader should understand before this section.

### 6. Connections
Note connections to:
- Previous concepts in the lecture
- Future concepts this builds toward
- Related topics from other areas of AI

## Output Format

Respond with YAML in a code block:

```yaml
concept_name: "[Descriptive concept name]"
slide_type: "[content|title|transition|example|diagram]"
summary: |
  [2-4 sentence conceptual summary]
key_ideas:
  - "[Idea 1]"
  - "[Idea 2]"
  - "[Idea 3]"
visual_elements:
  has_visual: [true|false]
  description: "[What the visual conveys, if present]"
  recreate_recommended: [true|false]
prerequisites:
  - "[Prerequisite concept 1]"
connections:
  builds_on: "[Previous concept or null]"
  leads_to: "[Next concept or null]"
  related_topics: "[Related AI topics]"
```

## Guidelines

- **Think pedagogically**: What is the teaching intent?
- **Be concise**: Quality over quantity
- **Preserve meaning**: Capture what matters, skip decoration
- **Note gaps**: If information seems incomplete, note it
- **Flag examples**: Distinguish worked examples from core concepts
- **Skip boilerplate**: Title-only slides can have minimal output
- **Infer context**: Use your knowledge of AI to fill in implied context
