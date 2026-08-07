from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from pathlib import Path

import pandas as pd


SHOT_PATTERN = re.compile(r"(?:^|[^0-9])([0-9]+)\s*-\s*([0-9]+)(?:[^0-9]|$)")


@dataclass(frozen=True)
class Measurement:
    source_path: Path
    device: str
    shot: str | None
    table: pd.DataFrame
    metadata: dict[str, str]
    measurement_name: str | None = None

    @property
    def measurement_id(self) -> str:
        label = self.measurement_name or self.source_path.stem
        shot = self.shot or "unknown-shot"
        return f"{self.device}:{shot}:{label}"


def infer_device(path: Path) -> str:
    parts = [p.lower() for p in path.parts]
    name = path.name.lower()
    if "nmos" in parts or "nmos" in name:
        return "NMOS"
    if "diode" in parts or "diode" in name or "dio" in name:
        return "diode"
    if "resistor" in parts or name.startswith("r") or "custom r" in name:
        return "resistor"
    if "cap" in parts or "cap" in name:
        return "Cap"
    return "unknown"


def infer_shot(text: str) -> str | None:
    if "#" in text:
        text = text.rsplit("#", maxsplit=1)[-1]
    match = SHOT_PATTERN.search(text)
    if not match:
        return None
    return f"{match.group(1)}-{match.group(2)}"


def read_clarius_csv(path: Path) -> Measurement:
    """Read a Clarius-style CSV where measurement rows precede metadata rows."""
    lines = path.read_text(encoding="utf-8-sig", errors="replace").splitlines()

    measurement_lines: list[str] = []
    for line in lines:
        if not line.strip():
            break
        measurement_lines.append(line)

    rows = list(csv.reader(measurement_lines))
    if not rows:
        table = pd.DataFrame()
    else:
        header = rows[0]
        fixed_rows = []
        for row in rows[1:]:
            fixed_rows.append((row + [""] * len(header))[: len(header)])
        table = pd.DataFrame(fixed_rows, columns=header).apply(pd.to_numeric, errors="coerce")

    metadata: dict[str, str] = {}
    metadata_started = False
    for line in lines[len(measurement_lines) :]:
        if not line.strip():
            metadata_started = True
            continue
        if not metadata_started:
            continue
        row = next(csv.reader([line]))
        if len(row) >= 2:
            metadata[row[0]] = ", ".join(row[1:])

    return Measurement(
        source_path=path,
        device=infer_device(path),
        shot=infer_shot(path.stem),
        table=table,
        metadata=metadata,
        measurement_name=path.stem,
    )


def _read_xlsx_settings(path: Path) -> dict[str, dict[str, str]]:
    try:
        settings = pd.read_excel(path, sheet_name="Settings", header=None)
    except ValueError:
        return {}

    current_sheet: str | None = None
    parsed: dict[str, dict[str, str]] = {}
    for _, row in settings.iterrows():
        values = [str(v).strip() for v in row.tolist() if pd.notna(v) and str(v).strip()]
        if not values:
            continue
        if len(values) == 1 and values[0].startswith(path.stem):
            current_sheet = values[0]
            parsed.setdefault(current_sheet, {})
            continue
        if current_sheet and len(values) >= 2:
            parsed[current_sheet][values[0]] = ", ".join(values[1:])
    return parsed


def read_diode_xlsx(path: Path) -> list[Measurement]:
    """Read multi-sheet diode Excel files exported from measurement software."""
    excel = pd.ExcelFile(path)
    measurements: list[Measurement] = []
    settings = _read_xlsx_settings(path)

    for sheet in excel.sheet_names:
        if sheet.lower() in {"calc", "settings"}:
            continue
        table = pd.read_excel(path, sheet_name=sheet).apply(pd.to_numeric, errors="coerce")
        measurements.append(
            Measurement(
                source_path=path,
                device="diode",
                shot=infer_shot(sheet),
                table=table,
                metadata={"sheet": sheet, **settings.get(sheet, {})},
                measurement_name=sheet,
            )
        )
    return measurements


def load_measurements(input_path: Path) -> list[Measurement]:
    paths = [input_path] if input_path.is_file() else list(input_path.rglob("*"))
    measurements: list[Measurement] = []
    for path in sorted(paths):
        suffix = path.suffix.lower()
        if suffix == ".csv":
            measurements.append(read_clarius_csv(path))
        elif suffix == ".xlsx" and infer_device(path) == "diode":
            measurements.extend(read_diode_xlsx(path))
    return measurements


def measurements_to_metadata_frame(measurements: list[Measurement]) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for measurement in measurements:
        base = {
            "measurement_id": measurement.measurement_id,
            "source": str(measurement.source_path),
            "source_file": measurement.source_path.name,
            "device": measurement.device,
            "shot": measurement.shot,
            "measurement_name": measurement.measurement_name,
            "measurement_rows": len(measurement.table),
        }
        if measurement.metadata:
            for key, value in measurement.metadata.items():
                rows.append({**base, "metadata_key": key, "metadata_value": value})
        else:
            rows.append({**base, "metadata_key": None, "metadata_value": None})
    return pd.DataFrame(rows)


def measurements_to_curve_frame(measurements: list[Measurement]) -> pd.DataFrame:
    rows: list[pd.DataFrame] = []
    for measurement in measurements:
        if measurement.table.empty:
            continue
        table = measurement.table.copy()
        table.insert(0, "point_index", range(len(table)))
        table.insert(0, "measurement_name", measurement.measurement_name)
        table.insert(0, "shot", measurement.shot)
        table.insert(0, "device", measurement.device)
        table.insert(0, "source_file", measurement.source_path.name)
        table.insert(0, "measurement_id", measurement.measurement_id)
        rows.append(table)
    return pd.concat(rows, ignore_index=True, sort=False) if rows else pd.DataFrame()
