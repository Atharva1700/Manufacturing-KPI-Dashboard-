# Metric definitions

Every number on the dashboard, with its source and formula. The data is made up.

**Source.** `data/line_week.csv`: one row per production line and week, with units in, units
good, units scrapped, and three cost lines (material, labor, overhead). In the warehouse this
would be the weekly production and cost extract. In Tableau it is `tableau/kpi_line_week.csv`.

**Units in.** Units that started on the line in the week.

**Units good.** Units that passed final inspection.

**Units scrapped.** Units removed from the process as scrap.

Units in = units good + units scrapped in this data (no work in progress is carried over).

| Metric | Definition | Formula | Tableau calculated field |
|---|---|---|---|
| Scrap rate | Share of units in that were scrapped | units scrapped ÷ units in | `Scrap Rate` |
| Yield | Share of units in that were good | units good ÷ units in | `Yield` |
| Cost per good unit | Total cost spent per good unit | (material + labor + overhead) ÷ units good | `Cost per Good Unit` |

Yield and scrap rate always add to 100%. The tests check this on every row.

**How totals are computed.** Company and period figures are ratios of totals: total scrap ÷ total
units in, and so on. They are not averages of the line percentages. An average of line rates gives
a small line the same weight as a large one, so it misstates the company figure. The tests check
the company scrap rate against the volume-weighted value.

**Period.** Weekly figures use the week starting Monday. The period figures use all twelve weeks
(weeks starting 3 Aug to 19 Oct 2026, data as made up).

**Line.** LINE-1, LINE-2, LINE-3.

**Trend.** A line's average over the first six weeks compared with the last six. The dashboard
shows the weekly values, so the trend is visible without this summary.

## What the made-up data shows

These are features of the simulation, written in to test the dashboard. They are not findings.

- LINE-2 scrap rate averages 5.6% in weeks 1 to 6 and 8.6% in weeks 7 to 12.
- LINE-3 cost per good unit averages about $11.90 in weeks 1 to 8 and about $12.80 in weeks 9 to 12.
  The rise comes from material cost, which was set 15% higher from week 9.
