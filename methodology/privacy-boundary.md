# What this repository never publishes

This repository is vendor-blind by construction. The boundary is enforced at build time in the code that writes the files, and checked again by `scripts/build_release.py --check` before every commit, not applied as a filter at read time.

## Never in any file

- Vendor, manufacturer, brand or storefront names.
- The client name printed on a certificate.
- Batch or lot identifiers.
- Certificate identifiers: laboratory test numbers, verification URLs, document hashes, image links.
- Submitter identity or upload metadata of any kind.
- Community names, channel identifiers, usernames, message text.
- Internal notes, review decisions, confidence scores on individual records.

The check in `scripts/build_release.py` fails the build if a column with any of those names appears in a release table.

## Always applied

- **Aggregates only.** One row per compound, per laboratory, per month, or per compound-month and laboratory-month cell. Never one row per certificate.
- **Minimum cell size.** Every cell carries at least the number of records given by `minimum_cell_size` in the manifest (ten at the time of writing). Smaller cells are omitted, and laboratories below the floor are folded into "Other labs" rather than dropped so totals still reconcile.
- **Printed label only.** Quantity deviation is measured against the label printed on the vial. A separate batch claim is not substituted.

## Why vendor-blind here when the website shows the client

Public lab reports are public evidence. The per-record pages at https://titratelab.com/coa show the laboratory, the client and the batch exactly as printed on the public report, because that information is part of the document the laboratory published and a reader is entitled to inspect it.

An aggregate by vendor is a different object. It reads as a ranking, it strips the per-record context that makes a public report defensible, and it can be built from a corpus that is not a random sample of any vendor's output. TitrateLab publishes vendor-level evidence only where each underlying record can be inspected, with its provenance, on the website or through the Data API. A spreadsheet of vendor averages with no way back to the documents is not that, so it is not released here.

## Laboratories are named

Laboratories are businesses that put their name on the document and publish it. Naming them is part of attribution, and TitrateLab publishes laboratory profiles at https://titratelab.com/labs. The laboratory dimension follows the alias, panel-group and floor-fold rules in `canonicalization.md`.

## If you believe something crossed the line

Open an issue with the "Report a wrong number" template and say which file and row. If the matter is sensitive, use the contact form at https://titratelab.com/contact instead of a public issue.
