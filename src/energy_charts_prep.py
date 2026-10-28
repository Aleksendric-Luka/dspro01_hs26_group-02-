import csv
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

# Pfad zu deiner CSV anpassen
input_file = Path("data/energy_charts_ch_2024-01-01_2026-10-28.csv")
output_file = input_file.with_name(f"{input_file.stem}_zurich.csv")

zurich = ZoneInfo("Europe/Zurich")

with (
    input_file.open("r", encoding="utf-8-sig", newline="") as source,
    output_file.open("w", encoding="utf-8", newline="") as target,
):
    reader = csv.DictReader(source)
    writer = csv.DictWriter(
        target,
        fieldnames=["timestamp", "load", "solar"],
    )
    writer.writeheader()

    for row in reader:
        timestamp = datetime.fromtimestamp(
            int(row["unix_seconds"]),
            tz=zurich,
        )

        writer.writerow({
            "timestamp": timestamp.isoformat(timespec="seconds"),
            "load": row["load"],
            "solar": row["solar"],
        })

print(f"Neue CSV erstellt: {output_file.resolve()}")