-- KPI views. Run on SQLite after data/line_week.csv is loaded into table line_week.
-- Definitions are in docs/metric_definitions.md; the Tableau calculated fields mirror these.

-- One row per line and week, with the three KPIs.
CREATE VIEW v_line_week_kpi AS
SELECT line_id,
       week_start,
       units_in,
       units_good,
       units_scrap,
       material_cost + labor_cost + overhead_cost AS total_cost,
       CAST(units_scrap AS REAL) / units_in        AS scrap_rate,
       CAST(units_good AS REAL) / units_in         AS yield,
       (material_cost + labor_cost + overhead_cost) / units_good AS cost_per_unit
FROM line_week
WHERE units_in > 0 AND units_good > 0;

-- Company level: sums first, then ratios. Averaging line ratios would give each line equal
-- weight regardless of volume, which is wrong.
CREATE VIEW v_week_kpi AS
SELECT week_start,
       SUM(units_in)    AS units_in,
       SUM(units_good)  AS units_good,
       SUM(units_scrap) AS units_scrap,
       CAST(SUM(units_scrap) AS REAL) / SUM(units_in)  AS scrap_rate,
       CAST(SUM(units_good) AS REAL) / SUM(units_in)   AS yield,
       SUM(material_cost + labor_cost + overhead_cost) / SUM(units_good) AS cost_per_unit
FROM line_week
GROUP BY week_start;

-- Whole period by line, for the summary tiles.
CREATE VIEW v_line_period_kpi AS
SELECT line_id,
       SUM(units_in)    AS units_in,
       SUM(units_good)  AS units_good,
       SUM(units_scrap) AS units_scrap,
       CAST(SUM(units_scrap) AS REAL) / SUM(units_in)  AS scrap_rate,
       CAST(SUM(units_good) AS REAL) / SUM(units_in)   AS yield,
       SUM(material_cost + labor_cost + overhead_cost) / SUM(units_good) AS cost_per_unit
FROM line_week
GROUP BY line_id;
