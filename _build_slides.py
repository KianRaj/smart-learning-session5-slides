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


def viz_chain():
    """Tools used separately vs chained into one workflow."""
    s = _defs()
    cols = [PEN, RED, GRN, PUR]
    names = ["Gemini", "NotebookLM", "Gamma", "Figma"]
    # left: scattered tools, 4 disconnected outputs
    for i, (n, c) in enumerate(zip(names, cols)):
        x = 30 + (i % 2) * 150; y = 40 + (i // 2) * 66
        s += f'<rect x="{x}" y="{y}" width="130" height="40" rx="9" fill="#fff" stroke="{c}" stroke-width="1.6"/>'
        s += f'<text x="{x+65}" y="{y+25}" text-anchor="middle" font-size="12.5" fill="{INK}">{n}</text>'
    s += f'<text x="170" y="185" text-anchor="middle" font-size="12.5" fill="{MUT}" class="mono">used separately → 4 loose outputs</text>'
    # divider
    s += f'<line x1="360" y1="30" x2="360" y2="190" stroke="{LINE}" stroke-width="2" stroke-dasharray="6 5"/>'
    # right: chained
    x = 395
    for i, (n, c) in enumerate(zip(names, cols)):
        s += f'<rect x="{x}" y="70" width="96" height="40" rx="9" fill="{c}"/>'
        s += f'<text x="{x+48}" y="95" text-anchor="middle" font-size="12" fill="#fff" font-weight="600">{n}</text>'
        if i < 3:
            s += _arrow(x+98, 90, x+114, 90, INK, "aw")
        x += 118
    s += f'<text x="630" y="185" text-anchor="middle" font-size="12.5" fill="{MUT}" class="mono">chained → ONE finished project</text>'
    svg = f'<svg viewBox="0 0 880 205">{s}</svg>'
    return viz(svg, "Same four tools. Alone they give you pieces; chained they give you a project.")

def viz_stage_steps(n, col, a, b, c):
    """A 3-step hands-on strip for one project stage."""
    s = _defs()
    x = 14
    for i, txt in enumerate([a, b, c]):
        w = 262
        s += f'<rect x="{x}" y="18" width="{w}" height="52" rx="10" fill="#fff" stroke="{col}" stroke-width="1.5"/>'
        s += f'<circle cx="{x+24}" cy="{44}" r="13" fill="{col}"/>'
        s += f'<text x="{x+24}" y="{49}" text-anchor="middle" font-size="12" fill="#fff" font-weight="700">{i+1}</text>'
        lines = txt.split("|")
        if len(lines) == 1:
            s += f'<text x="{x+46}" y="{49}" font-size="12.5" fill="{INK}">{lines[0]}</text>'
        else:
            s += f'<text x="{x+46}" y="{41}" font-size="12" fill="{INK}">{lines[0]}</text>'
            s += f'<text x="{x+46}" y="{57}" font-size="12" fill="{INK}">{lines[1]}</text>'
        if i < 2:
            s += _arrow(x+w+3, 44, x+w+17, 44, INK, "aw")
        x += w + 20
    svg = f'<svg viewBox="0 0 {x} 84">{s}</svg>'
    return viz(svg, f"Hands-on, stage {n} — three moves and you're done.")

def viz_statement():
    """A worked example of the AI contribution statement, as a document snippet."""
    s = f'<rect x="20" y="14" width="700" height="196" rx="12" fill="#fff" stroke="{LINE}" stroke-width="1.6"/>'
    s += f'<rect x="20" y="14" width="700" height="38" rx="12" fill="#EFEDE5"/>'
    s += f'<rect x="20" y="33" width="700" height="19" fill="#EFEDE5"/>'
    s += f'<text x="44" y="39" font-size="13" fill="{INK}" font-weight="700" class="mono">AI CONTRIBUTION STATEMENT — example</text>'
    lines = [
        ("Gemini", PEN,  "suggested subtopics and 3 applications — I verified each against the sources."),
        ("NotebookLM", RED, "generated the summary and MCQs from my uploaded sources (citations checked)."),
        ("Gamma", GRN, "produced the first draft of the deck — I rewrote the text and cut 4 slides."),
        ("Figma", PUR, "— I designed the poster myself, using AI only to fill placeholder text."),
        ("Me", INK, "chose the topic, checked every fact, wrote the conclusions and this statement."),
    ]
    y = 78
    for who, col, txt in lines:
        s += f'<rect x="44" y="{y-15}" width="94" height="22" rx="11" fill="{col}"/>'
        s += f'<text x="91" y="{y}" text-anchor="middle" font-size="11" fill="#fff" font-weight="600">{who}</text>'
        s += f'<text x="150" y="{y}" font-size="12.5" fill="{INK}">{txt}</text>'
        y += 30
    svg = f'<svg viewBox="0 0 740 224">{s}</svg>'
    return viz(svg, "Copy this shape: one line per tool saying what it did — and one line for what YOU did.")

def viz_reflection():
    """Two panels: what AI did vs what you did — the honest split."""
    def panel(x, title, col, items):
        t = f'<rect x="{x}" y="16" width="330" height="168" rx="12" fill="#fff" stroke="{col}" stroke-width="2"/>'
        t += f'<text x="{x+20}" y="46" font-size="14.5" fill="{INK}" font-weight="700">{title}</text>'
        yy = 76
        for it in items:
            t += f'<circle cx="{x+26}" cy="{yy-4}" r="3" fill="{col}"/>'
            t += f'<text x="{x+40}" y="{yy}" font-size="12.5" fill="{INK}">{it}</text>'
            yy += 30
        return t
    s = panel(20, "What AI did", PEN,
              ["fast drafts &amp; summaries", "layouts, themes, visuals", "MCQs &amp; study assets"])
    s += panel(390, "What YOU did", RED,
              ["chose &amp; framed the topic", "verified every claim", "rewrote, cut, decided"])
    s += f'<text x="370" y="105" text-anchor="middle" font-size="22" fill="{MUT}">+</text>'
    svg = f'<svg viewBox="0 0 740 200">{s}</svg>'
    return viz(svg, "Your reflection is just this picture in sentences — honest on both sides.")

def viz_pdf():
    """The submission as one ordered document stack."""
    items = [("1", "Topic + your 5 best prompts", PEN),
             ("2", "Gemini research notes, with sources", PEN),
             ("3", "NotebookLM screenshot + cited summary + 5 MCQs", RED),
             ("4", "Gamma deck — share link + PDF export", GRN),
             ("5", "Figma mockup screenshot", PUR),
             ("6", "AI contribution statement", INK),
             ("7", "Reflection on responsible AI use", INK)]
    # back sheets
    s = f'<rect x="46" y="26" width="560" height="282" rx="10" fill="#EFEDE5"/>'
    s += f'<rect x="36" y="18" width="560" height="282" rx="10" fill="#F6F4EC" stroke="{LINE}"/>'
    s += f'<rect x="26" y="10" width="560" height="288" rx="10" fill="#fff" stroke="{LINE}" stroke-width="1.6"/>'
    s += f'<text x="50" y="40" font-size="13" fill="{INK}" font-weight="700" class="mono">RollNo_Name_Session4.pdf</text>'
    y = 66
    for n, txt, col in items:
        s += f'<circle cx="{58}" cy="{y-5}" r="11" fill="{col}"/>'
        s += f'<text x="{58}" y="{y-1}" text-anchor="middle" font-size="11" fill="#fff" font-weight="700">{n}</text>'
        s += f'<text x="{80}" y="{y}" font-size="13" fill="{INK}">{txt}</text>'
        y += 33
    svg = f'<svg viewBox="0 0 640 316">{s}</svg>'
    return viz(svg, "One PDF, seven sections, in this order — grading follows the same order.")


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
    viz_chain(),
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
      viz_stage_steps(1, PEN,
        "ask Gemini with the|research prompt →",
        "pick 5+ facts, note the|source for each",
        "save prompt + notes|(they go in your PDF)"),
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
    viz_stage_steps(2, RED,
        "upload your Stage-1|sources → let it index",
        "Studio: summary · chat:|5 MCQs — check citations",
        "screenshot notebook,|save outputs"),
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
    viz_stage_steps(3, GRN,
        "paste your cited summary|→ Generate",
        "pick a theme, one idea +|one visual per slide",
        "export PDF +|copy the share link"),
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
    viz_stage_steps(4, PUR,
        "press F → frame|(pick a size)",
        "block out title, image,|button — then style it",
        "screenshot the mockup|(reuse deck colours)"),
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
    viz_statement(),
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
    two(
      viz_reflection(),
      tick([
        "Where did AI <b>save time</b> — and where did it <b>mislead</b> you?",
        "Which claims did you <b>correct or discard</b>?",
        "What did <b>you</b> add that the tools couldn't?",
        "Could you <b>defend every slide</b> in an oral exam?",
      ]),
    ),
    muted("Write 5–8 honest sentences. Honest beats perfect — show you stayed in charge of the tools."),
  ),
  # 15 — submission
  slide(
    eyebrow("Deliverable"),
    h2("What to submit — one PDF"),
    two(
      viz_pdf(),
      flash("Seven sections, <b>in this order</b>, exported as one PDF: "
            "<b>RollNo_Name_Session4.pdf</b><br><br>Tip: keep a running Google Doc open "
            "from Stage 1 — paste each artifact in as you finish it, and the submission "
            "builds itself."),
    ),
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
