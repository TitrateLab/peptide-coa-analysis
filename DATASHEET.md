# Datasheet

Structured after Gebru et al., "Datasheets for Datasets" (2021), so a researcher can judge fitness for use without reading the whole repository. Counts live in `data/latest/manifest.json` and the README; this page states definitions and decisions that do not change between releases.

## Motivation

- **Why it exists.** Public peptide lab reports are scattered across laboratory portals, vendor libraries and buyer communities. No aggregate view of them existed that stated its method and could be reproduced. TitrateLab maintains the underlying corpus for its evidence products and publishes these aggregates so claims about purity, quantity and testing practice can be checked against data rather than anecdote.
- **Who built it.** TitrateLab, an independent intelligence layer for the peptide market. TitrateLab sells access to evidence and tools; it sells no peptides and takes no payment from vendors or laboratories to appear in this data.
- **Funding.** TitrateLab's own revenue. No grant, sponsor or vendor funding.

## Composition

- **Unit of observation.** One published lab-report entry: one certificate or panel result for one vial, as issued by a testing laboratory. The released files aggregate those entries; no row describes a single report.
- **Tables.** Compound; compound by month; laboratory label; laboratory by month; month. Columns are defined in `schema/data-dictionary.md`.
- **Scope.** Entries that resolve to a recognized canonical peptide name or an all-recognized blend. Non-peptide analytical work (bacteriostatic water, vitamins, hormones) and unresolved names are excluded and counted in the manifest.
- **Time span.** Test dates from the earliest month that clears the cell floor to the newest full month before the release's observed-through date. The newest months keep growing in later releases as laboratories publish and collectors catch up.
- **Missing data.** Published per field in `manifest.json` under `missing_data`. Shares are always computed over records that have the field; the denominator is stated beside every share in the analyses.
- **Sensitive content.** None. No person, vendor, client, batch or certificate is identifiable. Laboratory names are business names printed on public reports. Every cell holds at least `minimum_cell_size` records.
- **Relationship to the full corpus.** The manifest reports the total published entries and the distinct certificate identifiers behind the aggregates, with the key spelled out. Per-record data is available through TitrateLab's website and Data API, not here.

## Collection process

- **Sources.** Laboratory public portals, a testing service's anonymized panel reports, third-party public certificate collections and vendor libraries, and certificates shared publicly in buyer communities or submitted by TitrateLab members. Source categories and counts are in the manifest; the category definitions are in `methodology/collection.md`.
- **Mechanism.** Automated collection of public documents, optical character recognition and structured extraction, then canonical-name resolution with ambiguous cases routed to human review rather than merged by guess.
- **Sampling.** None. The corpus is everything collected, which is itself whatever was tested and published by choice. It is not a probability sample of any population of vials, vendors or laboratories.
- **Timeframe.** Continuous collection since 2025 with retrospective coverage of older public reports; the release's observed-through timestamp is in the manifest.
- **Consent and ethics.** Public lab reports are public source evidence published by the laboratory or by the party that commissioned the test. Private community content, submitter identity and upload metadata never enter the projection this dataset is built from.

## Preprocessing, cleaning and labelling

- **Canonical names.** Printed compound names resolve to one canonical name per compound; blends are kept only when every component resolves. Rules in `methodology/canonicalization.md`.
- **Laboratory labels.** Printed laboratory names with one documented alias rule, one panel-group rule for anonymized panel laboratories, and a floor fold into "Other labs". Recorded per release under `lab_dimension` in the manifest.
- **Purity.** Results above zero enter means and medians; results at zero are counted separately as zero-identity results; missing results are counted as missing.
- **Quantity.** Deviation from the printed label in percent. A separate batch claim is never substituted.
- **Endotoxin.** A record counts as carrying a result when any endotoxin outcome is present, including "below detection".
- **Suppression.** Cells below the floor are omitted. Laboratories below the floor fold into "Other labs". Sentinel groups below the floor are dropped and counted.
- **Raw data.** Not distributed. The extraction corpus with per-record provenance stays inside TitrateLab; see "Distribution".

## Uses

- **Intended.** Describing the public evidence base for peptide testing: how often quantity matches the label, how often endotoxin is tested, how purity results are distributed, how testing volume and the laboratory mix change over time, and comparing those across compounds.
- **Suitable with care.** Longitudinal comparisons, because collection coverage changed over time; the early series reflects what had been collected, not what had been tested.
- **Not suitable.** Ranking vendors or products (no vendor dimension exists, by design). Estimating market-wide rates (not a sample). Judging the safety, quality or suitability of any product, batch or vendor. Anything presented as medical advice.
- **Known biases.** Selection by whoever chose to test and publish; laboratory coverage that is near-complete for one public portal and partial elsewhere; pooling of methods and laboratories within a compound; extraction error that is reported as missingness rather than corrected in the release.

## Distribution

- **Where.** This repository, `data/latest/` and `data/releases/<version>/`; the same files are attached to each GitHub release and archived on Zenodo when a DOI exists.
- **License.** Data and analysis under CC BY 4.0; code under MIT. Attribute as "TitrateLab, peptide-coa-analysis release <version>, https://github.com/TitrateLab/peptide-coa-analysis" or use `CITATION.cff`.
- **Fees and restrictions.** None for the released files. Per-record and vendor-identified data is available only through TitrateLab's Data API under its own terms.

## Maintenance

- **Who.** TitrateLab. Questions and corrections through the issue templates in this repository or the contact form at titratelab.com.
- **Cadence.** Monthly releases on the first of the month. Releases are immutable; a correction ships in the next release and is recorded in `CHANGELOG.md`.
- **Versioning.** The version string is the observed-through date of the release. `data/latest/` always equals the newest release directory. A release more than 45 days old is a defect; an automated probe raises it.
- **Reproducibility.** `scripts/build_release.py` renders every number and chart from the release files; `notebooks/reproduce-charts.ipynb` does the same interactively. Both run with only `matplotlib` and `jinja2`.
