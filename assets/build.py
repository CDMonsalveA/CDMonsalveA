"""Generate the SVG artwork used by the profile README.

    python assets/build.py

Every image is written in a light and a dark version; README.md picks the
right one with <picture>. Edit the data below and re-run to update the images.
Only the Python standard library is needed.
"""

from __future__ import annotations

import math
import random
from pathlib import Path
from types import SimpleNamespace
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent

SANS = "'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"

# GitHub Primer colors, so the art sits naturally on both GitHub themes.
THEMES = {
    "light": SimpleNamespace(
        bg="#ffffff", bg2="#f3f6fa", panel="#ffffff", border="#d0d7de", text="#1f2328",
        muted="#59636e", faint="#8c959f", grid="#c9d1d9",
        sky="#0969da", violet="#8250df", amber="#bf8700", green="#1a7f37",
    ),
    "dark": SimpleNamespace(
        bg="#0d1117", bg2="#161b22", panel="#161b22", border="#30363d", text="#e6edf3",
        muted="#9198a1", faint="#6e7681", grid="#30363d",
        sky="#4493f8", violet="#ab7df8", amber="#d29922", green="#3fb950",
    ),
}

PYTHON = "#3572A5"  # GitHub's language color for Python

# ----------------------------------------------------------------------------
# Content
# ----------------------------------------------------------------------------

STAGES = [
    ("sky", "database", "Collect", "& engineer data",
     ["Web scraping", "ETL pipelines", "SQL & Spark", "Social-media data"]),
    ("violet", "network", "Model", "& predict",
     ["Machine learning", "Deep learning", "Forecasting", "Anomaly detection"]),
    ("amber", "optimize", "Optimize", "& decide",
     ["LP / MIP models", "Location–allocation", "Scheduling", "Pricing strategy"]),
    ("green", "dashboard", "Deliver", "& automate",
     ["BI dashboards", "Web apps & APIs", "Workflow automation", "Docker & cloud"]),
]

IMPACT = [
    ("violet", "+184%", "organic brand growth", "Rafael Center · BI & web"),
    ("sky", "+54%", "revenue via referrals", "D’Vanity · 3× retention"),
    ("amber", "−16%", "lower import costs", "InsumosDJL · open data"),
    ("green", "12", "professionals led", "web, data & marketing"),
]

PROJECTS = {
    "machine-analyser": dict(
        name="machine_analyser", pill="v0.1.0", icon="repo",
        lines=["Detects machine states, segments production",
               "cycles and flags the anomalous ones."],
        tags=["pandas", "Plotly", "pytest", "MkDocs"],
        footer="Python", footer_color=PYTHON, meta="tests · docs · CI",
    ),
    "ai-or-workflow": dict(
        name="AI_OR_Workflow", pill="Thesis", icon="repo",
        lines=["Clustering & regression meet facility-location",
               "models (CFLP/UFLP): the code behind my thesis."],
        tags=["PuLP", "scikit-learn", "GeoPandas", "statsmodels"],
        footer="Python", footer_color=PYTHON, meta="operations research × AI",
    ),
    "estatesearch": dict(
        name="estateSearch", pill="WIP", icon="repo",
        lines=["Search → download → process → rank pipeline",
               "for UK property listings."],
        tags=["httpx", "parsel", "JMESPath", "Poetry"],
        footer="Python", footer_color=PYTHON, meta="web scraping",
    ),
    "rafaelcenter": dict(
        name="rafaelcenter.org", pill="Live", icon="globe",
        lines=["Website, brand, BI & marketing automation for an",
               "emotional-support center, built with 12 people."],
        tags=["WordPress", "Analytics", "Automation", "Branding"],
        footer="Website", footer_color=None, meta="2024 – 2025",
    ),
}

# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------

BASE_CSS = f"""
.sans {{ font-family: {SANS}; }}
.mono {{ font-family: {MONO}; }}
"""

MOTION_OFF = "@media (prefers-reduced-motion: reduce) { * { animation: none !important; } }"


def doc(w: int, h: int, title: str, desc: str, css: str, body: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">\n'
        f"<title id=\"title\">{escape(title)}</title>\n"
        f"<desc id=\"desc\">{escape(desc)}</desc>\n"
        f"<style>{BASE_CSS}{css}\n{MOTION_OFF}\n</style>\n"
        f"{body}\n</svg>\n"
    )


def text_width(s: str, size: float, factor: float = 0.55) -> float:
    """Rough width estimate; layouts leave enough slack for font differences."""
    return len(s) * size * factor


def icon(kind: str, color: str) -> str:
    """32x32 line icons drawn for this README."""
    def lines(width: float = 2.4) -> str:
        return (f'<g fill="none" stroke="{color}" stroke-width="{width}" '
                'stroke-linecap="round" stroke-linejoin="round">')

    if kind == "database":
        return (f'{lines()}<ellipse cx="16" cy="7" rx="10" ry="4"/>'
                '<path d="M6 7v18c0 2.2 4.5 4 10 4s10-1.8 10-4V7"/>'
                '<path d="M6 16c0 2.2 4.5 4 10 4s10-1.8 10-4"/></g>')
    if kind == "network":
        layers = [[9, 23], [4, 16, 28], [10, 22]]
        xs = [4, 16, 28]
        edges = "".join(
            f'<line x1="{xs[i]}" y1="{a}" x2="{xs[i + 1]}" y2="{b}"/>'
            for i in range(2) for a in layers[i] for b in layers[i + 1]
        )
        dots = "".join(
            f'<circle cx="{xs[i]}" cy="{y}" r="3" fill="{color}"/>'
            for i in range(3) for y in layers[i]
        )
        return f'{lines(1.6)}{edges}</g>{dots}'
    if kind == "optimize":
        return (f'{lines()}<path d="M4 28V13l9-8 15 6-4 17z"/>'
                '<path d="M17 2l14 16" stroke-dasharray="3 3" stroke-width="1.8"/></g>'
                f'<circle cx="28" cy="11" r="4" fill="{color}"/>')
    if kind == "dashboard":
        return (f'{lines()}<rect x="3" y="4" width="26" height="20" rx="3"/>'
                '<path d="M9 19v-4M14 19v-8M19 19v-5M24 19V9"/>'
                '<path d="M12 29h8M16 24v5"/></g>')
    if kind == "repo":
        return (f'{lines(2)}<path d="M7 4h17a2 2 0 0 1 2 2v20a2 2 0 0 1-2 2H9a3 3 0 0 1-3-3V6"/>'
                '<path d="M6 25a3 3 0 0 1 3-3h17"/><path d="M11 4v11l3-2 3 2V4"/></g>')
    if kind == "globe":
        return (f'{lines(2)}<circle cx="16" cy="16" r="12"/>'
                '<ellipse cx="16" cy="16" rx="5" ry="12"/><path d="M4 16h24M6 9.5h20M6 22.5h20"/></g>')
    if kind == "pin":
        return (f'{lines(2.6)}<path d="M16 29s-9-8.5-9-15a9 9 0 0 1 18 0c0 6.5-9 15-9 15z"/>'
                '<circle cx="16" cy="14" r="3.2"/></g>')
    raise ValueError(kind)


def warehouse(x: float, y: float, fill: str, door: str) -> str:
    return (f'<path d="M{x - 13} {y + 11}V{y - 3}L{x} {y - 13}L{x + 13} {y - 3}V{y + 11}z" fill="{fill}"/>'
            f'<rect x="{x - 4.5}" y="{y + 1}" width="9" height="10" rx="1.5" fill="{door}"/>')


# ----------------------------------------------------------------------------
# Images
# ----------------------------------------------------------------------------

def header(t: SimpleNamespace) -> str:
    W, H = 1200, 320
    rng = random.Random(11)
    depots = [(836, 92), (1062, 76), (930, 234), (1122, 226)]
    stores: list[tuple[float, float]] = []
    while len(stores) < 26:
        p = (rng.uniform(724, 1172), rng.uniform(30, 292))
        if all(math.dist(p, d) > 44 for d in depots) and all(math.dist(p, s) > 30 for s in stores):
            stores.append(p)

    routes, dots = [], []
    for i, (x, y) in enumerate(stores):
        dx, dy = min(depots, key=lambda d: math.dist((x, y), d))
        routes.append(f'<line class="route" x1="{x:.1f}" y1="{y:.1f}" x2="{dx}" y2="{dy}" '
                      f'style="animation-delay:-{i * 0.29 % 2:.2f}s"/>')
        dots.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.6" fill="{t.sky}"/>')
    hubs = "".join(
        f'<circle class="halo" cx="{x}" cy="{y}" r="24" fill="none" stroke="{t.amber}" stroke-width="2" '
        f'style="animation-delay:-{i * 0.8:.1f}s"/>' + warehouse(x, y, t.amber, t.bg2)
        for i, (x, y) in enumerate(depots)
    )

    css = f"""
.route {{ stroke: {t.sky}; stroke-opacity: .5; stroke-width: 1.6; stroke-dasharray: 3 5; animation: flow 2s linear infinite; }}
.halo {{ transform-box: fill-box; transform-origin: center; animation: halo 3.2s ease-out infinite; }}
.cursor {{ animation: blink 1.1s steps(1) infinite; }}
@keyframes flow {{ to {{ stroke-dashoffset: -16; }} }}
@keyframes halo {{ from {{ transform: scale(.45); opacity: .7; }} to {{ transform: scale(1.35); opacity: 0; }} }}
@keyframes blink {{ 50% {{ opacity: 0; }} }}
"""
    formula = "min Σ c·x + Σ f·y"
    fx = 262
    body = f"""<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{t.bg2}"/><stop offset="1" stop-color="{t.bg}"/></linearGradient>
  <radialGradient id="glow" cx=".78" cy=".5" r=".42"><stop offset="0" stop-color="{t.sky}" stop-opacity=".14"/><stop offset="1" stop-color="{t.sky}" stop-opacity="0"/></radialGradient>
  <pattern id="dots" width="18" height="18" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.2" fill="{t.grid}"/></pattern>
  <radialGradient id="fade"><stop offset=".35" stop-color="#fff"/><stop offset="1" stop-color="#000"/></radialGradient>
  <mask id="fadeMask"><rect x="660" y="0" width="540" height="{H}" fill="url(#fade)"/></mask>
  <clipPath id="frame"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="18"/></clipPath>
</defs>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="18" fill="url(#bg)" stroke="{t.border}"/>
<g clip-path="url(#frame)">
  <rect width="{W}" height="{H}" fill="url(#glow)"/>
  <rect x="660" y="0" width="540" height="{H}" fill="url(#dots)" mask="url(#fadeMask)"/>
  <!-- stores assigned to their nearest depot: a capacitated facility location problem, like my thesis -->
  <g>{"".join(routes)}</g>
  <g>{"".join(dots)}</g>
  <g>{hubs}</g>
</g>
<g class="sans">
  <text x="64" y="84" font-size="15" font-weight="700" letter-spacing="3" fill="{t.sky}">HOLA · HI, I’M</text>
  <text x="61" y="146" font-size="60" font-weight="800" fill="{t.text}">Cristian Monsalve</text>
  <text x="64" y="190" font-size="25" font-weight="600" fill="{t.text}">Mid Data Scientist · AI <tspan font-weight="400" fill="{t.muted}">at</tspan> <tspan fill="{t.sky}">NielsenIQ</tspan></text>
  <text x="64" y="232" font-size="19" fill="{t.muted}">Industrial engineer turning data into decisions with</text>
  <text x="64" y="258" font-size="19" fill="{t.muted}">machine learning + operations research.</text>
  <g transform="translate(60 276) scale(.62)">{icon("pin", t.muted)}</g>
  <text x="86" y="293" font-size="16" fill="{t.muted}">Bogotá, Colombia</text>
</g>
<circle cx="{fx - 14}" cy="288" r="2" fill="{t.faint}"/>
<text x="{fx}" y="293" class="mono" font-size="15" fill="{t.amber}">{escape(formula)}</text>
<rect class="cursor" x="{fx + len(formula) * 9.1 + 4:.0f}" y="279" width="8" height="17" rx="1" fill="{t.amber}"/>"""
    return doc(W, H, "Cristian Monsalve — Mid Data Scientist · AI at NielsenIQ",
               "Header: industrial engineer turning data into decisions with machine learning and operations "
               "research, based in Bogotá, Colombia. Animated network of stores routed to depots.",
               css, body)


def what_i_do(t: SimpleNamespace) -> str:
    CW, GAP, CH = 264, 48, 320
    W = 4 * CW + 3 * GAP
    parts = []
    for i, (tone, kind, title, subtitle, items) in enumerate(STAGES):
        c = getattr(t, tone)
        x = i * (CW + GAP)
        bullets = "".join(
            f'<circle cx="{x + 31}" cy="{198 + j * 30}" r="3.5" fill="{c}"/>'
            f'<text x="{x + 44}" y="{204 + j * 30}" font-size="18" fill="{t.muted}">{escape(item)}</text>'
            for j, item in enumerate(items)
        )
        parts.append(f"""<g class="sans">
  <rect x="{x + 1}" y="1" width="{CW - 2}" height="{CH - 2}" rx="18" fill="{t.panel}" stroke="{t.border}"/>
  <rect x="{x + 24}" y="24" width="56" height="56" rx="14" fill="{c}" fill-opacity=".14"/>
  <g transform="translate({x + 36} 36)">{icon(kind, c)}</g>
  <text x="{x + CW - 24}" y="48" text-anchor="end" class="mono" font-size="15" fill="{t.faint}">0{i + 1}</text>
  <text x="{x + 24}" y="128" font-size="30" font-weight="700" fill="{t.text}">{escape(title)}</text>
  <text x="{x + 24}" y="156" font-size="18" font-weight="600" fill="{c}">{escape(subtitle)}</text>
  <line x1="{x + 24}" y1="176" x2="{x + CW - 24}" y2="176" stroke="{t.border}"/>
  {bullets}
</g>""")
        if i < 3:
            cx = x + CW + GAP / 2
            parts.append(f'<g class="nudge" style="animation-delay:-{i * 0.4:.1f}s" fill="none" stroke="{t.faint}" '
                         f'stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round">'
                         f'<path d="M{cx - 11} 160h18M{cx + 1} 153l7 7-7 7"/></g>')
    css = """
.nudge { animation: nudge 1.8s ease-in-out infinite; }
@keyframes nudge { 50% { transform: translateX(5px); } }
"""
    desc = "; ".join(f"{i + 1}. {s[2]} {s[3]}: {', '.join(s[4])}" for i, s in enumerate(STAGES))
    return doc(W, CH, "What I do: from raw data to decisions", desc, css, "\n".join(parts))


def impact(t: SimpleNamespace) -> str:
    TW, GAP, TH = 282, 24, 188
    W = 4 * TW + 3 * GAP
    tiles = []
    for i, (tone, number, label, source) in enumerate(IMPACT):
        c = getattr(t, tone)
        x = i * (TW + GAP)
        tiles.append(f"""<g class="sans">
  <rect x="{x + 1}" y="1" width="{TW - 2}" height="{TH - 2}" rx="18" fill="{t.panel}" stroke="{t.border}"/>
  <rect x="{x + 24}" y="26" width="5" height="50" rx="2.5" fill="{c}"/>
  <text x="{x + 42}" y="72" font-size="52" font-weight="800" fill="{c}">{escape(number)}</text>
  <text x="{x + 24}" y="120" font-size="21" font-weight="600" fill="{t.text}">{escape(label)}</text>
  <text x="{x + 24}" y="152" font-size="18" fill="{t.muted}">{escape(source)}</text>
</g>""")
    desc = "; ".join(f"{n} {l} ({s})" for _, n, l, s in IMPACT)
    return doc(W, TH, "Impact highlights", desc, "", "\n".join(tiles))


def project_card(t: SimpleNamespace, p: dict) -> str:
    W, H = 560, 214
    pill_w = text_width(p["pill"], 14, 0.6) + 24
    chips, cx = [], 28
    for tag in p["tags"]:
        w = text_width(tag, 16, 0.56) + 26
        chips.append(f'<rect x="{cx:.0f}" y="134" width="{w:.0f}" height="30" rx="15" fill="{t.sky}" fill-opacity=".12"/>'
                     f'<text x="{cx + w / 2:.0f}" y="154" text-anchor="middle" font-size="16" fill="{t.sky}">{escape(tag)}</text>')
        cx += w + 8
    if p["footer_color"]:
        marker = f'<circle cx="34" cy="188" r="6" fill="{p["footer_color"]}"/>'
    else:
        marker = f'<g transform="translate(27 181) scale(.44)">{icon("globe", t.green)}</g>'
    lines = "".join(
        f'<text x="28" y="{90 + k * 26}" font-size="18" fill="{t.muted}">{escape(line)}</text>'
        for k, line in enumerate(p["lines"])
    )
    body = f"""<g class="sans">
  <rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14" fill="{t.panel}" stroke="{t.border}"/>
  <g transform="translate(26 26) scale(.72)">{icon(p["icon"], t.muted)}</g>
  <text x="58" y="47" font-size="25" font-weight="700" fill="{t.sky}">{escape(p["name"])}</text>
  <rect x="{W - 28 - pill_w:.0f}" y="26" width="{pill_w:.0f}" height="26" rx="13" fill="none" stroke="{t.border}"/>
  <text x="{W - 28 - pill_w / 2:.0f}" y="44" text-anchor="middle" font-size="14" font-weight="600" fill="{t.muted}">{escape(p["pill"])}</text>
  {lines}
  {"".join(chips)}
  {marker}
  <text x="48" y="194" font-size="16" fill="{t.muted}">{escape(p["footer"])} <tspan fill="{t.faint}">· {escape(p["meta"])}</tspan></text>
</g>"""
    return doc(W, H, p["name"], " ".join(p["lines"]) + " Tags: " + ", ".join(p["tags"]) + ".", "", body)


def main() -> None:
    (OUT / "projects").mkdir(exist_ok=True)
    for mode, t in THEMES.items():
        (OUT / f"header-{mode}.svg").write_text(header(t), encoding="utf-8")
        (OUT / f"what-i-do-{mode}.svg").write_text(what_i_do(t), encoding="utf-8")
        (OUT / f"impact-{mode}.svg").write_text(impact(t), encoding="utf-8")
        for slug, project in PROJECTS.items():
            (OUT / "projects" / f"{slug}-{mode}.svg").write_text(project_card(t, project), encoding="utf-8")
    print(f"SVGs written to {OUT}")


if __name__ == "__main__":
    main()
