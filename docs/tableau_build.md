# Building the Tableau dashboard

The `.twb` workbook is **not included**. Tableau Desktop was not available when this was built,
so the workbook was never opened or checked. This guide gives the steps to build it in about an
hour, and the formulas to type in. The data and the formulas are checked by the tests; the layout
is checked by the preview image.

## 1. Connect the data

1. Connect to a text file and choose `tableau/kpi_line_week.csv`.
2. Check the field types: `week_start` as **Date**, `line_id` as **String**, the rest as **Number**.
3. Rename the data source `KPI Line Week`.

## 2. Create the calculated fields

Use Analysis → Create Calculated Field. These aggregate correctly at any level (line, company,
period), because they divide sums and do not average ratios.

```
Scrap Rate
SUM([Units Scrapped]) / SUM([Units In])

Yield
SUM([Units Good]) / SUM([Units In])

Cost per Good Unit
(SUM([Material Cost]) + SUM([Labor Cost]) + SUM([Overhead Cost])) / SUM([Units Good])
```

Set the default number formats: scrap rate and yield as **Percentage, 1 decimal**; cost per good
unit as **Currency, 2 decimals**.

## 3. Build the sheets

| Sheet | Columns | Rows | Mark | Notes |
|---|---|---|---|---|
| Scrap trend | `Week Start` (continuous) | `Scrap Rate` | Line | Colour by `Line ID` |
| Yield trend | `Week Start` | `Yield` | Line | Colour by `Line ID` |
| Cost trend | `Week Start` | `Cost per Good Unit` | Line | Colour by `Line ID`; add a reference line for the company average |
| Period summary | `Line ID` | `Scrap Rate`, `Yield`, `Cost per Good Unit` | Text table | Whole period, no date filter |

## 4. Assemble the dashboard

1. New dashboard, fixed size 1200 × 800.
2. Put the period summary across the top as the headline row.
3. Put the three trend sheets below it, side by side.
4. Add a **Line ID** filter to all sheets (Show filter, multiple values).
5. Add a **Week Start** range filter (a slider) on the dashboard, applied to the trend sheets only.
6. Add a text object at the bottom: "Made-up data. Definitions: docs/metric_definitions.md."

## 5. Check before sharing

- Period scrap rate for LINE-2 should show 6.6%; yield 93.4%; cost per good unit $12.17.
- Company scrap rate for the first week should show 4.5%.
- If any figure differs, check the calculated fields first, then the filters.

## Publishing

Publish to Tableau Cloud or Tableau Server, or export as PDF from Tableau Desktop. Neither was
attempted here.
