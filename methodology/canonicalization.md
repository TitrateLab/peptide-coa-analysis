# How names are resolved

A certificate prints a compound name the way the laboratory or the client wrote it. Aggregating by compound requires one canonical name per compound. The same is true, with stricter rules, for laboratory names.

## Compounds

1. The printed compound name is resolved to a canonical peptide name using TitrateLab's canonical name table. Spelling variants, trade names, case differences and common abbreviations resolve to one name (for example "BPC 157", "bpc-157" and "Body Protection Compound 157" are one compound).
2. Blends are allowed only when every component resolves. "BPC-157 + TB-500" is a compound in this dataset; a blend with an unrecognized component is not.
3. Rows whose name does not resolve, and rows for analytical work that is not a peptide (bacteriostatic water, vitamins, hormones, OCR category labels), are excluded. They are counted in `coverage.excluded_noncanonical_or_invalid_records` so the exclusion is visible.
4. A compound with fewer records than the minimum cell size is excluded from every table. Its records are counted in `coverage.excluded_small_cell_records`.

The canonical name table is maintained in the TitrateLab codebase. Ambiguous names are routed to operator review rather than merged by guess. The public files only ever carry names that resolved.

## Laboratories

Laboratory labels are the laboratory names printed on public reports. Three rules are applied at build time, all recorded in `lab_dimension` in the manifest:

1. **Alias.** A printed alias of the same laboratory collapses to one label. The current alias table has one entry: "Janoshik Analytical" is reported as "Janoshik".
2. **Panel group.** Finnrick is a testing service that sends vials to a panel of laboratories it anonymizes as "Lab A" to "Lab N". Those records are reported together as "Finnrick panel labs (anonymized)". The repository does not guess which laboratory a letter denotes.
3. **Floor fold.** A laboratory with fewer included records than the minimum cell size is folded into "Other labs" so that the laboratory table still reconciles to the included total. The number of folded laboratories and records is in the manifest.

Records with no laboratory printed are labelled "Lab not recorded" and appear only when that group clears the cell floor.

Where TitrateLab publishes a laboratory profile at https://titratelab.com/labs, the `profile_url` column links to it. A blank `profile_url` means no profile exists, not that the laboratory is in doubt.

## Months

The month dimension is the calendar month of the test date printed on the report. Records whose test date is missing or malformed are counted in `missing_data.included_records_without_test_date` and are absent from the month tables.
