# Data dictionary

All files live in `data/latest/` (the newest release) and under `data/releases/<version>/` (every release, immutable). Every CSV is UTF-8 with a header row. Empty strings mean "not available", never zero.

## Shared statistics

These columns appear in several tables and always mean the same thing within the row's cell (a compound, a laboratory, a month, or a combination).

| Column | Type | Definition |
|---|---|---|
| `test_records` | integer | Published lab-report entries in the cell after canonical-name resolution. Always at least `minimum_cell_size`. |
| `purity_results` | integer | Records with a reported purity greater than zero. |
| `zero_identity_results` | integer | Records reported at zero purity, meaning the target compound was not identified. Kept separate from missing. |
| `mean_purity_pct` | number | Arithmetic mean of purity over `purity_results`, in percent. |
| `median_purity_pct` | number | Median purity over `purity_results`, in percent. |
| `quantity_results` | integer | Records whose tested quantity is expressed as percent deviation from the printed label. |
| `quantity_within_10pct_pct` | number | Share of `quantity_results` within plus or minus 10% of the printed label, in percent. |
| `quantity_more_than_10pct_under_label` | integer | Records whose tested quantity is more than 10% below the printed label. |
| `endotoxin_results` | integer | Records carrying any endotoxin result, including "below detection" outcomes. |
| `verifiable_records` | integer | Records carrying a laboratory verification URL. |
| `earliest_test_date` | date | Earliest printed test date in the cell, `YYYY-MM-DD`. |
| `latest_test_date` | date | Latest printed test date in the cell, `YYYY-MM-DD`. |

## `compounds.csv`

One row per canonical compound. Columns: `compound`, then every shared statistic above.

`compounds.json` holds the same rows under `compounds`, plus the manifest fields. It is byte-identical in shape to the file served at https://titratelab.com/data.

## `compound_month.csv`

One row per compound and calendar month of the printed test date. Columns: `compound`, `month` (`YYYY-MM`), `test_records`, `purity_results`, `median_purity_pct`, `quantity_results`, `quantity_within_10pct_pct`, `endotoxin_results`. Only compounds present in `compounds.csv` appear, and only months that clear the cell floor.

## `labs.csv`

One row per laboratory label. Columns: `lab`, `profile_url`, then every shared statistic. `profile_url` is the TitrateLab laboratory profile when one exists, otherwise empty. Label rules (alias, panel group, floor fold) are in `methodology/canonicalization.md` and in the manifest under `lab_dimension`.

## `lab_month.csv`

One row per laboratory label and month. Columns: `lab`, `month`, `test_records`, `purity_results`, `median_purity_pct`, `quantity_results`, `endotoxin_results`. Only labels present in `labs.csv` appear.

## `months.csv`

One row per calendar month across all included records. Columns: `month`, `test_records`, `purity_results`, `median_purity_pct`, `quantity_results`, `quantity_within_10pct_pct`, `endotoxin_results`, `verifiable_records`.

## `manifest.json`

| Key | Meaning |
|---|---|
| `dataset`, `version`, `schema_version` | Dataset name; the release version, which is the date of the newest observed record; the schema version of the files. |
| `generated_at`, `observed_through` | When the files were written; the newest record observation they include. |
| `vendor_blind`, `minimum_cell_size` | The privacy boundary parameters. |
| `projection` | The identifier and timestamps of the internal read model the release was built from. |
| `scope`, `exclusions` | Plain-language statement of what is in and out. |
| `totals.published_entries` | All published entries in the corpus, including those excluded from the tables. |
| `totals.distinct_certificate_identifiers` | Distinct values of the certificate key, with the key spelled out in `totals.certificate_identifier_key`. An upper bound on distinct certificates. |
| `coverage.*` | How many records were eligible, included, excluded below the floor, or excluded as non-canonical, and the split by source category. |
| `missing_data.*` | Completeness counts for the included records (see `methodology/quality-holds.md`). |
| `lab_dimension.*` | The alias table, the panel rule, the number of folded laboratories and records, and the number of named laboratories published. |
| `files.<name>` | Row count, byte size and SHA-256 of every table in the release. |
| `data_dictionary.*` | Short definitions of the shared statistics, duplicated here so a JSON consumer needs no Markdown. |

## Source categories

The split in `coverage.source_categories` uses these buckets. The mapping from internal source codes to buckets is maintained in TitrateLab's build script and summarized here.

| Category | Internal sources |
|---|---|
| Independent lab public portals | Laboratory-operated public results portals. |
| Independent lab panel reports | A testing service that publishes results from an anonymized laboratory panel. |
| Third-party aggregators and vendor libraries | Other public certificate collections and vendors' own published libraries. |
| Community and buyer submissions | Certificates shared publicly in buyer communities or submitted by TitrateLab members. |

## What the full data looks like

The internal read model behind these files has one row per published entry with the laboratory, printed client, printed compound, dose, purity, method, test type, test date, label and tested quantity, endotoxin fields, batch identifier, verification URL, confidence and source. None of the identity fields are released here. Query access to the per-record data is available through the Data API; see the README section "Get the full data".
