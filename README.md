# Manufacturing KPI Dashboard

Scrap rate, yield and cost per good unit across three production lines, for twelve weeks. This
project has the SQL that defines the metrics, the Tableau data source and calculated fields, the
documented definitions, and a rendered preview of the intended layout.

**The data is made up.** `simulate.py` builds in two effects so the trends have something to show:
LINE-2 scrap rising from week 7, and LINE-3 material cost rising 15% from week 9. They are modeled
effects, not findings.

**Not included: the Tableau workbook itself.** Tableau Desktop is not available in the build
environment, so no `.twb` was created or opened. `docs/tableau_build.md` gives the steps and
formulas to build it. The preview image shows the intended layout.

## Files

| File | Purpose |
|---|---|
| `simulate.py` | Made-up weekly production and cost data |
| `sql/kpi_views.sql` | Views: line-week KPIs, company-week KPIs, period KPIs by line |
| `build_extract.py` | Loads the data, runs the views, writes the Tableau extracts and the preview |
| `tableau/kpi_line_week.csv`, `tableau/kpi_week.csv` | Data sources for Tableau |
| `preview/dashboard_preview.png` | Static render of the trend charts (review only) |
| `docs/metric_definitions.md` | Every metric, its source and formula, and what the made-up data shows |
| `docs/tableau_build.md` | Step-by-step Tableau build with calculated fields |
| `tests/test_kpi.py` | Metric and trend checks |

## Run

```bash
python3 simulate.py
python3 build_extract.py data          # writes tableau/ and preview/
python3 -m pytest -q                   # 5 tests
```

## Results on the made-up data

| Line | Scrap rate | Yield | Cost per good unit |
|---|---|---|---|
| LINE-1 | 3.9% | 96.1% | $12.05 |
| LINE-2 | 6.6% | 93.4% | $12.17 |
| LINE-3 | 4.4% | 95.6% | $12.19 |

LINE-2 scrap averages 5.6% in weeks 1 to 6 and 8.6% in weeks 7 to 12. LINE-3 cost per good unit
rises from about $11.90 to about $12.80 after week 8.

## Verified and not verified

| Check | Result |
|---|---|
| Every line-week KPI recomputed by hand from the raw feed | pass (36 rows) |
| Yield + scrap rate = 100% on every row | pass |
| Company scrap rate is volume-weighted, not an average of line rates | pass |
| Planted LINE-2 and LINE-3 trends show up in the views | pass |
| Tableau workbook opens, renders and filters correctly | **Not verified.** The workbook was not built. |

## Limits

- Assumes units in = units good + units scrapped. Real lines carry work in progress, which this
  data does not have, so yield on a real line needs that adjustment.
- Cost is three totals per line-week. Cost by product or by step would need more detail.
- The preview is a matplotlib render of the same numbers, not a Tableau export.
