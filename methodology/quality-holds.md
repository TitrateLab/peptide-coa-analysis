# Extraction quality and what the missing-data counts mean

Most records enter the corpus as images or PDFs and pass through optical character recognition and structured extraction. Extraction is imperfect. This document says how that imperfection is handled and why it is reported rather than hidden.

## Completeness is published, not assumed

Every release manifest reports, for the included records:

| Field | Meaning |
|---|---|
| `included_records_without_measured_purity` | No purity figure above zero was extracted and the record is not a zero-identity result. |
| `included_records_without_label_quantity_deviation` | The report did not state a tested quantity against a printed label, or the extraction could not pair them. |
| `included_records_without_endotoxin_result` | No endotoxin test is present on the report. This is usually because the test was not ordered, not because extraction failed. |
| `included_records_without_verification_url` | The report carries no laboratory verification link. |
| `included_records_without_test_date` | The test date is missing or malformed. |

A share computed in this repository always states its denominator. "Share of quantity results within 10% of label" is computed over records that have a quantity result, not over all records.

## Zero purity

A purity of zero is reported when the laboratory did not identify the target compound in the vial. It is kept separate from "missing" and counted as `zero_identity_results`. It is not treated as a measured purity when computing means and medians.

## Known defect classes

TitrateLab has recorded extraction defects in its own corpus over time and treats them as recurring classes rather than one-off bugs:

- duplicate test numbers for distinct documents and, conversely, one document published under two entries;
- numbers misread by OCR, which are caught by consistency checks against the printed label, the laboratory's own portal, or later re-extraction;
- unit confusions in quantity fields;
- promotional or category text extracted as a name.

The release build does not correct records. It excludes rows that do not resolve to a recognized compound, applies the cell floor, and publishes the completeness counts above. Corrections happen in the corpus and show up in the next release.

## Reporting a wrong number

Open an issue with the "Report a wrong number" template. Point at the file and line, say what you expected, and link evidence. Public lab reports are public evidence and can be linked directly. Corrections that change a published number are recorded in `CHANGELOG.md` with the release that carries them.

## Quality holds are not privacy

When a record is withheld for quality reasons, that is a data-quality decision and is described as one. It is never described as a privacy protection. Public lab reports are public source evidence.
