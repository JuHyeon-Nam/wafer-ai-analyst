from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "docs" / "assets"
FEATURES_PATH = ROOT / "data" / "processed" / "features_preview.csv"


COLORS = {
    "bg": "#F7F9FC",
    "panel": "#FFFFFF",
    "ink": "#122033",
    "muted": "#627084",
    "line": "#D8E0EA",
    "normal": "#2E7D5B",
    "review": "#D9942B",
    "priority": "#C43D4B",
    "blue": "#2E74B5",
    "purple": "#6F42C1",
}


def _font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/AppleSDGothicNeo.ttc",
        "/Library/Fonts/Arial Unicode.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size=size, index=0)
    return ImageFont.load_default()


def _draw_card(draw: ImageDraw.ImageDraw, xy: tuple[int, int, int, int], title: str, value: str, color: str) -> None:
    draw.rounded_rectangle(xy, radius=12, fill=COLORS["panel"], outline=COLORS["line"], width=2)
    x1, y1, _, _ = xy
    draw.text((x1 + 24, y1 + 20), title, font=_font(22), fill=COLORS["muted"])
    draw.text((x1 + 24, y1 + 58), value, font=_font(42, bold=True), fill=color)


def dashboard_summary(features: pd.DataFrame) -> None:
    width, height = 1400, 860
    img = Image.new("RGB", (width, height), COLORS["bg"])
    draw = ImageDraw.Draw(img)

    draw.text((60, 42), "Wafer AI Analyst Dashboard", font=_font(42, bold=True), fill=COLORS["ink"])
    draw.text(
        (60, 96),
        "Shot-level electrical feature review and process issue candidate reasoning",
        font=_font(24),
        fill=COLORS["muted"],
    )

    total = len(features)
    normal = int(features["review_status"].eq("normal").sum())
    review = int(features["review_status"].eq("review").sum())
    priority = int(features["review_status"].eq("priority").sum())
    cards = [
        ("Measurements", str(total), COLORS["blue"]),
        ("Normal", str(normal), COLORS["normal"]),
        ("Review", str(review), COLORS["review"]),
        ("Priority", str(priority), COLORS["priority"]),
    ]
    for idx, card in enumerate(cards):
        x = 60 + idx * 320
        _draw_card(draw, (x, 150, x + 280, 270), *card)

    left = (60, 330, 650, 700)
    right = (730, 330, 1340, 785)
    draw.rounded_rectangle(left, radius=14, fill=COLORS["panel"], outline=COLORS["line"], width=2)
    draw.rounded_rectangle(right, radius=14, fill=COLORS["panel"], outline=COLORS["line"], width=2)
    draw.text((90, 360), "Review Status by Device", font=_font(26, bold=True), fill=COLORS["ink"])
    draw.text((760, 360), "Top Anomaly Flags", font=_font(26, bold=True), fill=COLORS["ink"])

    grouped = features.groupby(["device", "review_status"]).size().unstack(fill_value=0)
    devices = grouped.index.tolist()
    max_count = int(grouped.sum(axis=1).max()) if len(grouped) else 1
    x0, y0 = 100, 430
    bar_w, gap = 86, 38
    scale = 210 / max_count
    for i, device in enumerate(devices):
        base_x = x0 + i * (bar_w + gap)
        y_base = 650
        start = y_base
        for status, color in [("normal", COLORS["normal"]), ("review", COLORS["review"]), ("priority", COLORS["priority"])]:
            count = int(grouped.loc[device].get(status, 0))
            h = max(0, int(count * scale))
            if h:
                draw.rectangle((base_x, start - h, base_x + bar_w, start), fill=color)
                start -= h
        draw.text((base_x, 666), str(device), font=_font(18), fill=COLORS["muted"])

    flag_counts = features["anomaly_flags"].value_counts().head(5)
    y = 430
    max_flag = int(flag_counts.max()) if len(flag_counts) else 1
    for flag, count in flag_counts.items():
        label = str(flag)
        if len(label) > 54:
            label = label[:51] + "..."
        draw.text((760, y), label, font=_font(19), fill=COLORS["ink"])
        draw.rounded_rectangle((760, y + 30, 1240, y + 48), radius=9, fill="#EAF0F8")
        draw.rounded_rectangle((760, y + 30, 760 + int(480 * count / max_flag), y + 48), radius=9, fill=COLORS["purple"])
        draw.text((1260, y + 22), str(count), font=_font(20, bold=True), fill=COLORS["muted"])
        y += 78

    img.save(ASSET_DIR / "dashboard_summary.png")


def feature_table_preview(features: pd.DataFrame) -> None:
    cols = ["device", "shot", "review_status", "anomaly_score", "anomaly_flags", "process_issue_candidates"]
    table = features.sort_values(["anomaly_score", "device", "shot"], ascending=[False, True, True])[cols].head(8).copy()
    table["anomaly_flags"] = table["anomaly_flags"].astype(str).map(lambda value: value[:32] + "..." if len(value) > 35 else value)
    table["process_issue_candidates"] = table["process_issue_candidates"].astype(str).map(
        lambda value: value[:52] + "..." if len(value) > 55 else value
    )

    width, height = 1600, 680
    img = Image.new("RGB", (width, height), COLORS["bg"])
    draw = ImageDraw.Draw(img)
    draw.text((50, 36), "Feature Table Preview", font=_font(38, bold=True), fill=COLORS["ink"])
    draw.text((50, 86), "Parsed measurement rows enriched with anomaly score and process issue candidates", font=_font(22), fill=COLORS["muted"])

    x_positions = [50, 190, 310, 500, 690, 1060]
    headers = ["device", "shot", "status", "score", "anomaly flags", "candidate issues"]
    y = 145
    draw.rounded_rectangle((40, y - 18, width - 40, y + 48), radius=10, fill="#E7EEF7")
    for x, header in zip(x_positions, headers):
        draw.text((x, y), header, font=_font(20, bold=True), fill=COLORS["ink"])

    y += 70
    for _, row in table.iterrows():
        draw.rounded_rectangle((40, y - 16, width - 40, y + 48), radius=8, fill=COLORS["panel"], outline=COLORS["line"])
        values = [
            row["device"],
            row["shot"],
            row["review_status"],
            row["anomaly_score"],
            row["anomaly_flags"],
            row["process_issue_candidates"],
        ]
        for x, value in zip(x_positions, values):
            color = COLORS["priority"] if value == "priority" else COLORS["ink"]
            draw.text((x, y), str(value), font=_font(18), fill=color)
        y += 52

    img.save(ASSET_DIR / "feature_table_preview.png")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate README preview images from a feature CSV.")
    parser.add_argument("--input", default=str(FEATURES_PATH), help="Feature CSV path.")
    args = parser.parse_args()

    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    features = pd.read_csv(args.input)
    dashboard_summary(features)
    feature_table_preview(features)
    print(f"saved README assets to {ASSET_DIR}")


if __name__ == "__main__":
    main()
