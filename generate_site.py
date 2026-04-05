#!/usr/bin/env python3
from __future__ import annotations

import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LEVELS = [
    ("foundation", "Foundation"),
    ("proficient", "Proficient"),
    ("excellence", "Excellence"),
]


def title_from_slug(slug: str) -> str:
    title = slug.removeprefix("lo-yr9-")
    return title.replace("-", " ").title()


def collect_objectives() -> list[dict]:
    objectives = []
    for folder in sorted(ROOT.glob("lo-yr9-*")):
        if not folder.is_dir():
            continue
        pdfs = []
        for level, label in LEVELS:
            pdf_path = folder / f"{level}-questions.pdf"
            if pdf_path.exists():
                pdfs.append({
                    "level": level,
                    "label": label,
                    "href": f"./{folder.name}/{pdf_path.name}",
                })
        if pdfs:
            objectives.append({
                "slug": folder.name,
                "title": title_from_slug(folder.name),
                "pdfs": pdfs,
            })
    return objectives


def render_index(objectives: list[dict]) -> str:
    jump_links = "\n          ".join(
        f'<a href="#{html.escape(item["slug"])}">{html.escape(item["title"])}</a>'
        for item in objectives
    )

    sections = []
    for objective in objectives:
        cards = []
        for pdf in objective["pdfs"]:
            cards.append(
                f'''<a class="worksheet-card" href="{html.escape(pdf["href"])}" target="_blank" rel="noopener noreferrer">
            <span class="worksheet-level">{html.escape(pdf["label"])}</span>
            <span class="worksheet-arrow">Open PDF ↗</span>
          </a>'''
            )
        sections.append(
            f'''<section id="{html.escape(objective["slug"])}" class="objective-section">
        <div class="section-heading">
          <p class="eyebrow">Learning objective</p>
          <h2>{html.escape(objective["title"])}</h2>
        </div>
        <div class="worksheet-grid">
          {''.join(cards)}
        </div>
      </section>'''
        )

    return f'''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Mana Maths</title>
    <meta name="description" content="Mana Maths worksheet PDFs organised by learning objective." />
    <link rel="canonical" href="https://manamaths.co.nz/" />
    <link rel="stylesheet" href="./styles.css" />
  </head>
  <body>
    <main class="page-shell">
      <section class="hero">
        <p class="eyebrow">Mana Maths</p>
        <h1>Worksheet PDFs, in one clean place.</h1>
        <p class="lead">Projector-friendly maths worksheets organised by learning objective.</p>
      </section>

      <nav class="jump-links" aria-label="Learning objectives">
        {jump_links}
      </nav>

      {''.join(sections)}
    </main>
  </body>
</html>
'''


def main() -> int:
    objectives = collect_objectives()
    if not objectives:
        raise SystemExit("No worksheet PDFs found.")
    (ROOT / "index.html").write_text(render_index(objectives), encoding="utf-8")
    print(f"Generated site for {len(objectives)} learning objectives.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
