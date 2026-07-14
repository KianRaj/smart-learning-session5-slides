# Session 4 — The Integrated AI Workflow (capstone)

Presentation slides + mini-project assessment for the **Smart Learning** series. Built
as a lightweight, self-contained slide deck (a web page, **not** a notebook) so you can
present the workflow first, then run the assessed mini project.

> **Live slides:** https://kianraj.github.io/smart-learning-session4-slides/
>
> **Present locally:** open [`index.html`](index.html) in any browser.

## All sessions in this series

| Session | Topic | Live slides |
|---------|-------|-------------|
| 2 | Smart Learning with Google Gemini & NotebookLM | https://kianraj.github.io/smart-learning-session2-slides/ |
| 3 | AI for Presentations & Design (Gamma & Figma AI) | https://kianraj.github.io/smart-learning-session3-slides/ |
| 4 | The Integrated AI Workflow — capstone & assessment | https://kianraj.github.io/smart-learning-session4-slides/ |

## What's inside

| Part | Slides | Content |
|------|--------|---------|
| Motivation & objectives | 1–2 | Why tools must chain together; session outcomes |
| The workflow | 3 | **Master pipeline visualization** — Research → Organize → Present → Design with the ethics band |
| The toolkit | 4 | All four tools with real screenshots |
| The four stages | 5–8 | One slide per stage — real tool screens, steal-these prompts, and each stage's deliverable |
| Ethics | 9–10 | **Verification-loop visualization**; citations, integrity, the AI contribution statement |
| Mini project | 11–12 | The brief + **process-timeline visualization** (stage · tool · time · deliverable) |
| Assessment | 13 | **Visual rubric** — grading weights as bars |
| Reflection & submission | 14–15 | Responsible-AI reflection questions; the one-PDF checklist |
| Impact & wrap | 16–17 | What the programme leaves students with |

Every concept is drawn, not just told: the pipeline, the verification loop, the project
timeline and the rubric are all custom diagrams; every tool stage carries **real
in-app screenshots** (self-hosted, reused from Sessions 2–3 plus a Gemini capture).

## Present it

- **Navigate:** `→` / `Space` next · `←` back · `Home` / `End` jump · `F` fullscreen.
- **Click:** right edge of the slide = next, left edge = back. Touch = swipe.
- **Deep-link:** `index.html#3` opens the workflow diagram directly.

## The mini project (the assessment)

Students pick one topic and run it through all four stages (~70 min + 10 min reflection):

1. **Research (Gemini, 15 min)** — 5+ key facts, each with a source to check
2. **Organize (NotebookLM, 20 min)** — notebook + cited summary + 5 MCQs
3. **Present (Gamma, 20 min)** — 8–10 slide deck exported as PDF
4. **Design (Figma, 15 min)** — poster / title-screen mockup

**Submit** one PDF (`RollNo_Name_Session4.pdf`): topic + 5 best prompts, research notes
with sources, NotebookLM screenshot + cited outputs, Gamma link + PDF, Figma screenshot,
an **AI contribution statement**, and a **reflection on responsible AI use**.

**Grading:** prompt engineering 20% · research 15% · organization & citations 20% ·
presentation 20% · design 10% · integrity + reflection 15% (visualized on slide 13).

## Files

```
smart-learning-session4-slides/
├── index.html          <- the presentation (open / share this)
├── assets/
│   ├── img/             <- real tool screenshots (self-hosted)
│   ├── slides.css       <- the "notebook aesthetic" theme
│   └── slides.js        <- keyboard / click / swipe navigation
├── _build_slides.py     <- all slide content lives here; regenerates index.html
└── README.md
```

## Editing the slides

All content lives in one place — [`_build_slides.py`](_build_slides.py). Edit the
`SLIDES` list or a `viz_*` diagram, then regenerate:

```bash
python _build_slides.py
```
