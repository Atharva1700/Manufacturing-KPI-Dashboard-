"""Loads the weekly feed, runs the KPI views, and writes the files Tableau connects to.

Writes:
  tableau/kpi_line_week.csv   one row per line and week (main Tableau data source)
  tableau/kpi_week.csv        company totals per week
  preview/dashboard_preview.png   a static render of the intended layout, for review only

Usage: python build_extract.py [data_dir]
"""

import csv
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).parent
SQL = HERE / "sql" / "kpi_views.sql"


def load_db(data_dir):
    conn = sqlite3.connect(":memory:")
    with (Path(data_dir) / "line_week.csv").open() as f:
        reader = csv.DictReader(f)
        cols = reader.fieldnames
        conn.execute(f"CREATE TABLE line_week ({', '.join(c + (' TEXT' if c in ('line_id', 'week_start') else ' REAL') for c in cols)})")
        conn.executemany(f"INSERT INTO line_week VALUES ({', '.join('?' * len(cols))})",
                         [tuple(r[c] for c in cols) for r in reader])
    conn.executescript(SQL.read_text())
    return conn


def export(conn, view, path):
    cur = conn.execute(f"SELECT * FROM {view} ORDER BY 1, 2" if view == "v_line_week_kpi"
                       else f"SELECT * FROM {view} ORDER BY 1")
    cols = [d[0] for d in cur.description]
    rows = cur.fetchall()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(cols)
        for r in rows:
            w.writerow([round(v, 4) if isinstance(v, float) else v for v in r])
    return len(rows)


def preview(conn, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    weeks = [r[0] for r in conn.execute("SELECT week_start FROM v_week_kpi ORDER BY 1")]
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.2), sharex=True)
    specs = [("scrap_rate", "Scrap rate by line", "{:.1%}"),
             ("yield", "Yield by line", "{:.1%}"),
             ("cost_per_unit", "Cost per good unit by line ($)", "${:.2f}")]
    for ax, (col, title, _) in zip(axes, specs):
        for line in ["LINE-1", "LINE-2", "LINE-3"]:
            ys = [r[0] for r in conn.execute(
                f"SELECT {col} FROM v_line_week_kpi WHERE line_id = ? ORDER BY week_start", (line,))]
            ax.plot(range(len(ys)), ys, marker="o", ms=3, label=line)
        ax.set_title(title, fontsize=11)
        ax.set_xticks(range(0, len(weeks), 2))
        ax.set_xticklabels([weeks[i][5:] for i in range(0, len(weeks), 2)], rotation=45, fontsize=8)
        ax.grid(alpha=0.3)
    axes[0].legend(fontsize=8)
    fig.suptitle("Made-up data: line trends, weekly (preview of the Tableau layout)", fontsize=11)
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=110)
    plt.close(fig)


def main(argv):
    data_dir = Path(argv[0]) if argv else HERE / "data"
    conn = load_db(data_dir)
    n1 = export(conn, "v_line_week_kpi", HERE / "tableau" / "kpi_line_week.csv")
    n2 = export(conn, "v_week_kpi", HERE / "tableau" / "kpi_week.csv")
    preview(conn, HERE / "preview" / "dashboard_preview.png")
    print(f"wrote {n1} line-week rows, {n2} company weeks, and the preview")


if __name__ == "__main__":
    main(sys.argv[1:])
