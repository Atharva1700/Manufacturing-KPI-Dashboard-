"""Made-up weekly production and cost data for three lines over twelve weeks.

Two effects are built in so the trends have something to show:
  * LINE-2 scrap rises from week 7 (scrap in units goes up by about 60%).
  * LINE-3 material cost per unit rises 15% from week 9.
They are modeled effects in made-up data, not findings about any plant.
Fixed seed.
"""

import csv
import random
from datetime import date, timedelta
from pathlib import Path

SEED = 31
LINES = ["LINE-1", "LINE-2", "LINE-3"]
WEEKS = [date(2026, 8, 3) + timedelta(weeks=i) for i in range(12)]
HEADER = ["line_id", "week_start", "units_in", "units_good", "units_scrap",
          "material_cost", "labor_cost", "overhead_cost"]


def simulate(out_dir, seed=SEED):
    rng = random.Random(seed)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for line in LINES:
        base_scrap = {"LINE-1": 0.04, "LINE-2": 0.05, "LINE-3": 0.045}[line]
        for wk, week in enumerate(WEEKS, start=1):
            units_in = rng.randint(900, 1100)
            scrap_rate = base_scrap * (1 + rng.gauss(0, 0.08))
            if line == "LINE-2" and wk >= 7:
                scrap_rate *= 1.6
            units_scrap = round(units_in * scrap_rate)
            units_good = units_in - units_scrap
            material = units_in * 6.20 * (1 + rng.gauss(0, 0.02))
            if line == "LINE-3" and wk >= 9:
                material *= 1.15
            labor = units_in * 2.10 * (1 + rng.gauss(0, 0.02))
            overhead = 3100 * (1 + rng.gauss(0, 0.01))
            rows.append([line, week.isoformat(), units_in, units_good, units_scrap,
                         round(material, 2), round(labor, 2), round(overhead, 2)])
    with (out_dir / "line_week.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(HEADER)
        w.writerows(rows)
    return out_dir


if __name__ == "__main__":
    out = simulate(Path(__file__).parent / "data")
    print(f"wrote {out / 'line_week.csv'}")
