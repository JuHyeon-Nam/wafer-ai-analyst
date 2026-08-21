from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


DEFAULT_DOCS = [
    "docs/PORTFOLIO_BRIEF.md",
    "docs/INTERVIEW_PLAYBOOK.md",
    "docs/DEMO_GUIDE.md",
    "docs/DEMO_RUN_SUMMARY.md",
    "docs/FINAL_VALIDATION.md",
    "docs/RELEASE_NOTES.md",
]


def main() -> None:
    parser = argparse.ArgumentParser(description="Bundle portfolio-facing documents into one Markdown packet.")
    parser.add_argument("--output", default="docs/PORTFOLIO_PACKET.md")
    parser.add_argument("--docs", nargs="*", default=DEFAULT_DOCS)
    args = parser.parse_args()

    sections = [
        "# Wafer AI Analyst Portfolio Packet",
        "",
        f"- Generated at: `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`",
        "- Purpose: portfolio review, interview preparation, and demo rehearsal",
        "",
    ]
    for doc in args.docs:
        path = ROOT / doc
        if not path.exists():
            sections.extend([f"## Missing Document: `{doc}`", "", "This document was not found.", ""])
            continue
        sections.extend(
            [
                "---",
                "",
                f"<!-- Source: {doc} -->",
                "",
                path.read_text().strip(),
                "",
            ]
        )

    output = ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(sections).rstrip() + "\n")
    print(f"saved portfolio packet to {output.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
