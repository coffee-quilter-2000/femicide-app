-- State-by-year data for the Trends section  ->  data/state_trends.csv
-- One row per state (50 + DC) per year, 1976–2024. Blank cells = no data for that year.
--
-- Replace PROJECT_ID.femicide_project with your project and dataset before running in the
-- BigQuery console. (scripts/export_state_trends.py fills it in automatically.)

SELECT
  p.state_fips,
  p.state_abb,
  p.year,
  p.pop_total,                              -- SEER / Census population
  p.pop_female,
  f.female_victims,                         -- FBI SHR female homicide victims (murder)
  f.female_victims_per_100k_women,          -- femicide rate
  c.poverty_rate,                           -- SAIPE, % of people in poverty (1989+)
  c.uninsured_rate_under65,                 -- SAHIE, % under 65 without health insurance (2006+)
  c.pct_ba_plus_25                          -- ACS / 2000 Census, % of adults 25+ with a bachelor's (2000, 2005+)
FROM `PROJECT_ID.femicide_project.population_state_year` AS p
LEFT JOIN `PROJECT_ID.femicide_project.femicide_state_rate` AS f
  ON f.state_fips = p.state_fips AND f.year = p.year
LEFT JOIN `PROJECT_ID.femicide_project.census_state_year` AS c
  ON c.state_fips = p.state_fips AND c.year = p.year
WHERE p.year BETWEEN 1976 AND 2024
ORDER BY p.state_abb, p.year
