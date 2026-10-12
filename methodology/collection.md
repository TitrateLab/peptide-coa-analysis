# Where the records come from

Every row behind this repository is a published lab-report entry: one certificate of analysis or lab panel result for one peptide vial, as issued by a testing laboratory, that TitrateLab has collected, extracted and published with a per-record page at https://titratelab.com/coa. The repository never publishes those rows. It publishes aggregates computed from them.

## Source categories

Each entry carries a source. Sources are grouped into four categories, and the manifest reports how many included records fall into each (`coverage.source_categories`).

| Category | What it means |
|---|---|
| Independent lab public portals | Records read from a laboratory's own public results portal, where the laboratory publishes certificates its clients chose to make public. The laboratory, not TitrateLab, is the publisher of record. |
| Independent lab panel reports | Records from a testing service that sends vials to a panel of laboratories and publishes the results. The panel laboratories are anonymized by the service and appear here as one group. |
| Third-party aggregators and vendor libraries | Records collected from other public certificate collections, including vendors' own published certificate libraries. These are public documents, but the collection was not made by the laboratory. |
| Community and buyer submissions | Certificates shared publicly in buyer communities or submitted to TitrateLab by members. The certificate is public evidence; the submitter is not identified anywhere. |

Category membership is decided by the source field at build time. The rule is in `scripts/data/build_public_lab_snapshot.py` in the TitrateLab codebase and is reproduced in `schema/data-dictionary.md`.

## What a record is and is not

- A record is one published entry. Two entries can describe the same physical certificate (see `deduplication.md`).
- A record is not a random sample of the market. Vials are tested because someone chose to test them, and published because someone chose to publish them. Selection effects are real and unmeasured.
- A record says what a laboratory reported about one vial on one date. It does not establish the safety, quality or suitability of a product, a batch or a vendor.

## What is deliberately not collected into this repository

- Private chat content, usernames, upload-account metadata and internal notes. Those never enter the projection this repository is built from.
- Vendor, manufacturer, client, batch and certificate identity. The per-record pages on titratelab.com show the client printed on a public report; this repository does not (see `privacy-boundary.md`).

## Freshness

- The source projection is rebuilt from the live corpus every ten minutes.
- Releases are cut monthly. The version string is the date of the newest record observed when the release was built (`observed_through` in the manifest), not the date the files were written.
- `data/latest/` always equals the newest directory under `data/releases/`. Older releases are never rewritten.
