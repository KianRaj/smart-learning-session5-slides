#!/usr/bin/env python3
"""
Build the lecture slide deck for:

    Session 4 — The Integrated AI Workflow (capstone)

Content lives here (one place). Run this to regenerate the HTML:

    python _build_slides.py

Output:  index.html   (open / share this)
Shared:  assets/slides.css , assets/slides.js
Real screenshots (self-hosted): assets/img/
"""
import os, html

HERE = os.path.dirname(os.path.abspath(__file__))

FONTS = ("https://fonts.googleapis.com/css2?"
         "family=Archivo:wght@700;800;900&"
         "family=IBM+Plex+Sans:wght@400;500;600&"
         "family=IBM+Plex+Mono:wght@400;500;600&display=swap")

INK, PEN, RED, YEL, MUT, LINE, GRN = (
    "#17233B", "#2B4FD8", "#E4572E", "#FFE066", "#6E7688", "#E7E4DB", "#2E9E5B")
PUR = "#7C4DFF"

# ---------- render helpers ----------
def slide(*body, cls=""):
    return f'<section class="slide {cls}"><div class="inner">' + "".join(body) + "</div></section>"

def eyebrow(tag):   return f'<p class="eyebrow">Session 4 <span class="dot">•</span> {tag}</p>'
def h1(t):   return f"<h1>{t}</h1>"
def h2(t):   return f"<h2>{t}</h2>"
def lead(t): return f'<p class="lead">{t}</p>'
def p(t):    return f"<p>{t}</p>"
def muted(t):return f'<p class="muted">{t}</p>'

def cards(items, cols=3):
    inner = "".join(
        f'<div class="card">{("<span class=k>"+k+"</span>") if k else ""}'
        f'<h3>{t}</h3><p>{d}</p></div>' for k, t, d in items)
    return f'<div class="cards c{cols}">{inner}</div>'

def tick(items):  return '<ul class="tick">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"
def steps(items): return '<ol class="steps">' + "".join(f"<li>{i}</li>" for i in items) + "</ol>"
def rows(pairs):
    r = "".join(f'<div class="row"><span class="lbl">{k}</span><span>{v}</span></div>' for k, v in pairs)
    return f'<div class="rows">{r}</div>'
def flash(txt):  return f'<div class="flash">{txt}</div>'
def two(a, b):   return f'<div class="two"><div>{a}</div><div>{b}</div></div>'
def tags(items, on=()):
    return '<div class="tags">' + "".join(
        f'<span class="tag {"on" if t in on else ""}">{t}</span>' for t in items) + "</div>"
def prompt(text, tag="prompt"):
    return (f'<div class="prompt-box"><span class="pl">{tag}</span>'
            f'<span class="pt">{html.escape(text)}</span></div>')
def handoff(title, note, chip):
    return ('<div class="handoff"><p class="eyebrow">Now — hands-on</p>'
            f'<div class="big">{title}</div><p class="muted">{note}</p>'
            f'<span class="file">{chip}</span></div>')
def shot(src, url, cap="", crop=False):
    dots = "".join(f'<i style="background:{c}"></i>' for c in ("#E4572E", "#FFC93C", "#2E9E5B"))
    cap = f'<div class="cap">{cap}</div>' if cap else ""
    cls = "imgwrap crop" if crop else "imgwrap"
    return (f'<div class="shot"><div class="bar">{dots}<span class="url">{url}</span></div>'
            f'<div class="{cls}"><img src="assets/img/{src}" alt="{url} screenshot"></div>{cap}</div>')

# ---------- viz helpers ----------
def viz(svg, cap="", legend=None):
    leg = ""
    if legend:
        leg = '<div class="viz-legend">' + "".join(
            f'<span><i style="background:{c}"></i>{t}</span>' for c, t in legend) + "</div>"
    cap = f'<div class="cap">{cap}</div>' if cap else ""
    return f'<div class="viz">{svg}{cap}{leg}</div>'

def _defs():
    return (f'<defs>'
            f'<marker id="a" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="{MUT}"/></marker>'
            f'<marker id="aw" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="{INK}"/></marker>'
            f'</defs>')

def _arrow(x1, y1, x2, y2, color=MUT, mid="a"):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="2" marker-end="url(#{mid})"/>'

STAGES = [("1 · RESEARCH", "Gemini", PEN, "research notes"),
          ("2 · ORGANIZE", "NotebookLM", RED, "cited study notes"),
          ("3 · PRESENT", "Gamma", GRN, "deck (PDF)"),
          ("4 · DESIGN", "Figma", PUR, "title-screen mockup")]

def viz_pipeline():
    """The master diagram: 4 tool stages + the artifact each hands to the next,
    with a verification/ethics band underneath spanning the whole flow."""
    s = _defs()
    x = 14; y = 46; w = 172; gap = 52
    for i, (stage, tool, col, out) in enumerate(STAGES):
        s += f'<text x="{x+w/2}" y="{y-14}" text-anchor="middle" font-size="11" fill="{MUT}" class="mono">{stage}</text>'
        s += f'<rect x="{x}" y="{y}" width="{w}" height="64" rx="12" fill="{col}"/>'
        s += f'<text x="{x+w/2}" y="{y+38}" text-anchor="middle" font-size="17" fill="#fff" font-weight="700">{tool}</text>'
        s += f'<rect x="{x+10}" y="{y+76}" width="{w-20}" height="30" rx="15" fill="#fff" stroke="{col}"/>'
        s += f'<text x="{x+w/2}" y="{y+95}" text-anchor="middle" font-size="11" fill="{INK}" class="mono">{out}</text>'
        if i < 3:
            s += _arrow(x+w+4, y+32, x+w+gap-6, y+32, INK, "aw")
        x += w + gap
    total_w = x - gap
    # ethics band
    s += f'<rect x="14" y="176" width="{total_w-14}" height="44" rx="10" fill="rgba(255,224,102,.45)" stroke="#EAD98A"/>'
    s += (f'<text x="{(total_w+14)/2}" y="203" text-anchor="middle" font-size="14" fill="{INK}" font-weight="600">'
          f'⚖️ At every stage: verify claims · cite sources · disclose AI use</text>')
    svg = f'<svg viewBox="0 0 {total_w+14} 236">{s}</svg>'
    return viz(svg, "One project, four stages — each tool hands a concrete artifact to the next. Ethics runs under all of it.")

def viz_verify():
    """Verification loop: AI answer → find the source → check → cite (or discard)."""
    s = _defs()
    nodes = [("AI gives a claim", 110, PEN), ("find the source", 340, RED),
             ("does it check out?", 570, YEL)]
    for label, cx, col in nodes:
        tcol = INK if col == YEL else "#fff"
        s += f'<rect x="{cx-95}" y="52" width="190" height="52" rx="12" fill="{col}"/>'
        s += f'<text x="{cx}" y="{cx==570 and 74 or 84}" text-anchor="middle" font-size="13.5" fill="{tcol}" font-weight="600">{label}</text>'
        if cx == 570:
            s += f'<text x="{cx}" y="94" text-anchor="middle" font-size="11" fill="{INK}" class="mono">read the passage yourself</text>'
    s += _arrow(207, 78, 243, 78, INK, "aw")
    s += _arrow(437, 78, 473, 78, INK, "aw")
    # two outcomes
    s += _arrow(610, 106, 680, 150, GRN, "a")
    s += f'<rect x="600" y="152" width="180" height="44" rx="10" fill="rgba(46,158,91,.15)" stroke="{GRN}"/>'
    s += f'<text x="690" y="179" text-anchor="middle" font-size="13" fill="{INK}">✓ use it — <tspan font-weight="700">and cite it</tspan></text>'
    s += _arrow(530, 106, 460, 150, RED, "a")
    s += f'<rect x="330" y="152" width="200" height="44" rx="10" fill="rgba(228,87,46,.12)" stroke="{RED}"/>'
    s += f'<text x="430" y="179" text-anchor="middle" font-size="13" fill="{INK}">✗ no source? <tspan font-weight="700">don\'t use it</tspan></text>'
    svg = f'<svg viewBox="0 0 800 212">{s}</svg>'
    return viz(svg, "The verification loop — run EVERY AI claim through it before it enters your project.")

def viz_rubric():
    """Assessment weights as horizontal bars."""
    items = [("Prompt engineering (evidence in all tools)", 20, PEN),
             ("Research quality (Gemini)", 15, PEN),
             ("Organization &amp; citations (NotebookLM)", 20, RED),
             ("Presentation (Gamma deck)", 20, GRN),
             ("Design asset (Figma)", 10, PUR),
             ("Integrity + reflection", 15, INK)]
    s = ""; y = 26
    for label, pct, col in items:
        s += f'<text x="330" y="{y+15}" text-anchor="end" font-size="13.5" fill="{INK}">{label}</text>'
        s += f'<rect x="345" y="{y}" width="330" height="20" rx="6" fill="#EFEDE5"/>'
        s += f'<rect x="345" y="{y}" width="{330*pct/25}" height="20" rx="6" fill="{col}"/>'
        s += f'<text x="{350+330*pct/25+8}" y="{y+15}" font-size="12.5" fill="{MUT}" class="mono">{pct}%</text>'
        y += 34
    svg = f'<svg viewBox="0 0 750 {y+4}">{s}</svg>'
    return viz(svg, "How the mini project is graded — prompt engineering and integrity carry as much weight as the artifacts.")

def viz_timeline():
    """Project process: 4 stages with time + deliverable, as a horizontal timeline."""
    s = _defs()
    data = [("Research", "Gemini", "15 min", "5+ facts, each with a source to check", PEN),
            ("Organize", "NotebookLM", "20 min", "summary + 5 MCQs, all cited", RED),
            ("Present", "Gamma", "20 min", "8–10 slide deck → PDF", GRN),
            ("Design", "Figma", "15 min", "poster / title-screen mockup", PUR)]
    x = 20; w = 205; y = 60
    s += f'<line x1="30" y1="{y}" x2="{20+4*w-30}" y2="{y}" stroke="{LINE}" stroke-width="3"/>'
    for i, (stage, tool, t, deliv, col) in enumerate(data):
        cx = x + i*w + 80
        s += f'<circle cx="{cx}" cy="{y}" r="17" fill="{col}"/>'
        s += f'<text x="{cx}" y="{y+5}" text-anchor="middle" font-size="13" fill="#fff" font-weight="700">{i+1}</text>'
        s += f'<text x="{cx}" y="{y-34}" text-anchor="middle" font-size="15" font-weight="700" fill="{INK}">{stage}</text>'
        s += f'<text x="{cx}" y="{y-16}" text-anchor="middle" font-size="11.5" fill="{MUT}" class="mono">{tool} · {t}</text>'
        s += f'<rect x="{cx-92}" y="{y+34}" width="184" height="56" rx="10" fill="#fff" stroke="{col}"/>'
        s += f'<text x="{cx}" y="{y+56}" text-anchor="middle" font-size="10.5" fill="{MUT}" class="mono">DELIVERABLE</text>'
        # wrap deliverable text
        words = deliv.split(); mid = len(words)//2
        l1, l2 = " ".join(words[:mid]), " ".join(words[mid:])
        s += f'<text x="{cx}" y="{y+72}" text-anchor="middle" font-size="11.5" fill="{INK}">{l1}</text>'
        s += f'<text x="{cx}" y="{y+86}" text-anchor="middle" font-size="11.5" fill="{INK}">{l2}</text>'
    svg = f'<svg viewBox="0 0 {20+4*w} 170">{s}</svg>'
    return viz(svg, "~70 minutes of tool time + 10 minutes for the reflection. Each stage ends with something you can show.")

# ============================================================
#  SLIDES
# ============================================================
SLIDES = [
  # 1 — title
  slide(
    eyebrow("Smart Learning Series · capstone"),
    h1("The Integrated<br>AI Workflow"),
    lead("You've met the tools one by one. Today you chain them into "
         "<mark>one complete academic workflow</mark> — and use it ethically."),
    tags(["Gemini", "NotebookLM", "Gamma", "Figma AI", "Mode: mini project"],
         on=["Mode: mini project"]),
    muted("Press → / Space to advance · ← to go back · F for fullscreen"),
  ),
  # 2 — why + objective
  slide(
    eyebrow("Why & what"),
    h2("No tool works alone"),
    two(
      p("Real academic work isn't “use one AI tool”. It's a <b>chain</b>: research "
        "feeds organization, organization feeds the presentation, the presentation "
        "needs design — and <b>every link needs verification</b>.") +
      flash("Today's outcome: a <b>mini project</b> that runs through all four tools, "
            "plus a short reflection on responsible AI use."),
      tick([
        "<b>Research</b> a topic with Gemini.",
        "<b>Organize</b> the knowledge in NotebookLM (with citations).",
        "<b>Present</b> it with Gamma.",
        "<b>Design</b> a visual asset with Figma.",
        "<b>Verify, cite and disclose</b> at every step.",
      ]),
    ),
  ),
  # 3 — master pipeline
  slide(
    eyebrow("The workflow · visualize it"),
    h2("One project, four stages"),
    viz_pipeline(),
    muted("Memorise this picture — it's the whole session. Each stage produces an artifact the next stage consumes."),
  ),
  # 5 — stage 1 research
  slide(
    eyebrow("Stage 1 · Research — Gemini"),
    h2("Research: explore fast, trust nothing yet"),
    two(
      shot("gemini_home.jpg", "gemini.google.com",
           "Use Gemini to explore the topic fast — then treat every claim as unverified.", crop=True) +
      flash("<b>Stage output:</b> 5+ key facts / ideas — each with a source you can check."),
      prompt("I'm a 2nd-year CSE student researching 'AI in healthcare' for a seminar. "
             "Give me: the 5 most important subtopics, 3 real applications, and the "
             "key debates. For each, name a source I can verify.", "research") +
      prompt("What are the strongest arguments AGAINST deploying AI diagnosis "
             "systems? Cite where each argument comes from.", "counter-view"),
    ),
  ),
  # 6 — stage 2 organize
  slide(
    eyebrow("Stage 2 · Organize — NotebookLM"),
    h2("Organize: keep only what's checked"),
    two(
      shot("nblm_citations.jpg", "notebooklm.google.com → chat",
           "Every answer cites your uploaded sources — click and check the passage."),
      shot("nblm_studio.jpg", "notebooklm.google.com → Studio",
           "One-click study assets from the sources you collected in Stage 1."),
    ),
    flash("<b>Stage output:</b> a notebook with your sources + a cited summary and 5 MCQs. "
          "Prompt pattern: <i>“From my sources only, …”</i>"),
  ),
  # 7 — stage 3 present
  slide(
    eyebrow("Stage 3 · Present — Gamma"),
    h2("Present: your notes become a deck"),
    two(
      shot("gamma_step_prompt.jpg", "gamma.app → Generate",
           "Paste your NotebookLM summary as the outline — Gamma designs the deck."),
      shot("gamma_step_images.jpg", "gamma.app → image source",
           "Pick visuals per card — AI images, web images or illustrations."),
    ),
    flash("<b>Stage output:</b> an 8–10 slide deck exported as PDF. One idea per slide; "
          "the facts come from Stage 2, already verified."),
  ),
  # 8 — stage 4 design
  slide(
    eyebrow("Stage 4 · Design — Figma"),
    h2("Design: one strong visual"),
    two(
      shot("figma_step2_layout.jpg", "figma.com → canvas",
           "Block out a poster or title screen for your project — frame, boxes, text."),
      shot("figma_step3_connect.jpg", "figma.com → Prototype",
           "Optional stretch: wire two screens together into a clickable flow."),
    ),
    flash("<b>Stage output:</b> a title-screen / poster mockup (screenshot it). "
          "Reuse your deck's colours so the project feels like one thing."),
  ),
  # 9 — verification
  slide(
    eyebrow("Ethics · visualize it"),
    h2("Verify before you use"),
    viz_verify(),
    p("AI sounds confident even when it's wrong. One simple rule: <b>if you haven't "
      "checked the source, it doesn't go in your project.</b> NotebookLM shows its sources; "
      "for Gemini, YOU find and check them."),
  ),
  # 10 — integrity
  slide(
    eyebrow("Ethics"),
    h2("Citations &amp; academic integrity"),
    two(
      cards([("do", "Work with integrity",
              "Cite every source (author, title, link); rewrite AI text in your own words; "
              "keep your prompts — they're your work log; disclose which tools you used where.")], cols=1),
      cards([("don't", "Cross these lines",
              "Don't submit AI output unread; don't invent or trust uncited facts; don't upload "
              "confidential material; don't present AI work as entirely your own.")], cols=1),
    ),
    flash("End your project with an <b>AI contribution statement</b> — one paragraph: "
          "<i>which tool did what, and what you did yourself</i>. That's the professional standard."),
  ),
  # 12 — project process timeline
  slide(
    eyebrow("Hands-on · the mini project"),
    h2("Your mini project — the process"),
    viz_timeline(),
    two(
      p("Pick <b>one topic</b> from your branch — e.g. <i>AI in healthcare · renewable "
        "microgrids · smart-city traffic</i> — and run it through all four stages. "
        "<b>Save your best prompt at every stage</b> — they go in your submission.") ,
      flash("This mini project is the <b>assessment for the whole programme</b>. "
            "Falling behind? Shrink the artifact, not the verification — a small, "
            "cited project beats a big, unchecked one."),
    ),
  ),
  # 13 — assessment rubric
  slide(
    eyebrow("Assessment · visualize it"),
    h2("How your project is graded"),
    viz_rubric(),
    muted("Evidence of prompt engineering = the prompts you saved at each stage, pasted into your submission."),
  ),
  # 14 — reflection
  slide(
    eyebrow("Hands-on · reflection"),
    h2("Reflection: responsible AI usage"),
    p("Finish with <b>5–8 sentences</b> answering:"),
    tick([
      "Where did AI <b>save you time</b> — and where did it <b>mislead</b> you?",
      "Which claims did you have to <b>correct or discard</b> after verification?",
      "What did <b>you</b> contribute that the tools could not?",
      "Would your project pass an oral exam — can you <b>defend every slide</b>?",
    ]),
    flash("Honest reflections score higher than perfect-sounding ones — the point is "
          "showing you <b>stayed in charge</b> of the tools."),
  ),
  # 15 — submission
  slide(
    eyebrow("Deliverable"),
    h2("What to submit — one PDF"),
    two(
      tick([
        "Topic + your <b>5 best prompts</b> (one per stage minimum)",
        "Gemini research notes <b>with sources</b>",
        "NotebookLM screenshot + cited summary + 5 MCQs",
        "Gamma deck <b>share link + PDF export</b>",
      ]),
      tick([
        "Figma mockup screenshot",
        "<b>AI contribution statement</b> (one paragraph)",
        "<b>Reflection</b> on responsible AI use (5–8 sentences)",
      ]),
    ),
    flash("Order them as listed, one PDF → <b>RollNo_Name_Session4.pdf</b>"),
  ),
  # 17 — wrap
  slide(
    handoff("Four tools. One workflow. Your project.",
            "Research with Gemini · organize with NotebookLM · present with Gamma · "
            "design with Figma — verify, cite and disclose throughout.",
            "gemini.google.com · notebooklm.google.com · gamma.app · figma.com"),
    tags(["you can research &amp; fact-check", "hours of busywork → minutes",
          "professional decks &amp; designs", "AI use others can trust"]),
    muted("That's what this programme leaves you with. Use the workflow in your next real "
          "assignment — that's where it compounds. Submission deadline as announced in class."),
    cls="handoff-slide",
  ),
]

# ============================================================
#  PAGE SHELL + WRITE
# ============================================================
def page():
    body = "\n".join(SLIDES)
    nav = ('<div class="nav"><button class="up" title="Previous (↑)">↑</button>'
           '<button class="down" title="Next (↓)">↓</button></div>')
    chrome = ('<div class="margin-line"></div><div class="progress"></div>'
              '<div class="counter"></div>'
              '<div class="brand">KIET · Smart Learning · Session 4</div>' + nav)
    return f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Session 4 — The Integrated AI Workflow</title>
<meta name="description" content="Capstone: chain Gemini, NotebookLM, Gamma and Figma into one ethical academic workflow.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="assets/slides.css">
</head><body>
<div class="stage">
{body}
</div>
{chrome}
<script src="assets/slides.js"></script>
</body></html>"""

def main():
    with open(os.path.join(HERE, "index.html"), "w", encoding="utf-8") as f:
        f.write(page())
    print("wrote index.html  (", len(SLIDES), "slides )")

if __name__ == "__main__":
    main()
