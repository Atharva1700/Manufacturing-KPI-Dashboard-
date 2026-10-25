import csv
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import build_extract  # noqa: E402
import simulate  # noqa: E402


@pytest.fixture(scope="module")
def data_dir(tmp_path_factory):
    return simulate.simulate(tmp_path_factory.mktemp("kpi"))


@pytest.fixture(scope="module")
def conn(data_dir):
    return build_extract.load_db(data_dir)


@pytest.fixture(scope="module")
def raw(data_dir):
    return list(csv.DictReader(open(data_dir / "line_week.csv")))


def test_line_week_kpis_match_hand_arithmetic(conn, raw):
    """Each row recomputed from the raw feed in plain Python."""
    got = {(r[0], r[1]): r for r in conn.execute(
        "SELECT line_id, week_start, scrap_rate, yield, cost_per_unit FROM v_line_week_kpi")}
    assert len(got) == len(raw) == 36
    for r in raw:
        n_in, good, scrap = int(r["units_in"]), int(r["units_good"]), int(r["units_scrap"])
        cost = float(r["material_cost"]) + float(r["labor_cost"]) + float(r["overhead_cost"])
        _, _, rate, y, cpu = got[(r["line_id"], r["week_start"])]
        assert rate == pytest.approx(scrap / n_in)
        assert y == pytest.approx(good / n_in)
        assert cpu == pytest.approx(cost / good)


def test_yield_and_scrap_rate_add_to_one(conn):
    bad = conn.execute("SELECT COUNT(*) FROM v_line_week_kpi WHERE abs(scrap_rate + yield - 1) > 1e-9").fetchone()[0]
    assert bad == 0


def test_company_kpis_are_volume_weighted_not_averaged(conn, raw):
    """Company scrap rate per week must be total scrap over total units, not the mean of line rates."""
    week = raw[0]["week_start"]
    rows = [r for r in raw if r["week_start"] == week]
    scrap = sum(int(r["units_scrap"]) for r in rows) / sum(int(r["units_in"]) for r in rows)
    got = conn.execute("SELECT scrap_rate FROM v_week_kpi WHERE week_start = ?", (week,)).fetchone()[0]
    assert got == pytest.approx(scrap)


def test_planted_trends_show_up(conn):
    """LINE-2 scrap should be clearly higher after week 7; LINE-3 cost per unit higher after week 9."""
    l2_early = [r[0] for r in conn.execute(
        "SELECT scrap_rate FROM v_line_week_kpi WHERE line_id='LINE-2' ORDER BY week_start")][:6]
    l2_late = [r[0] for r in conn.execute(
        "SELECT scrap_rate FROM v_line_week_kpi WHERE line_id='LINE-2' ORDER BY week_start")][6:]
    assert sum(l2_late) / len(l2_late) > 1.4 * sum(l2_early) / len(l2_early)

    l3 = [r[0] for r in conn.execute(
        "SELECT cost_per_unit FROM v_line_week_kpi WHERE line_id='LINE-3' ORDER BY week_start")]
    # The planted rise is 15% on material, about half of unit cost: expect roughly +8%, test for +5%.
    assert sum(l3[8:]) / 4 > 1.05 * sum(l3[:8]) / 8


def test_extract_files_are_written(data_dir, tmp_path, monkeypatch):
    monkeypatch.setattr(build_extract, "HERE", tmp_path)
    build_extract.main([str(data_dir)])
    lines = (tmp_path / "tableau" / "kpi_line_week.csv").read_text().splitlines()
    assert lines[0].split(",")[:3] == ["line_id", "week_start", "units_in"]
    assert len(lines) == 37  # header + 36 rows
    assert (tmp_path / "preview" / "dashboard_preview.png").stat().st_size > 1000
