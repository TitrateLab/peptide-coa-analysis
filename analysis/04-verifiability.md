# Can a reader verify a report with the laboratory?

**Verdict:** 98.4% of 96,805 included reports carry a laboratory verification URL, the link printed on the certificate that resolves to the laboratory's own copy. 1,584 carry none. By laboratory, the share depends almost entirely on whether the laboratory operates a public verification portal.

Release 2026-10-12, records observed through 2026-10-12.

## Completeness of the included records

| Field | Records without it | Share of included |
|---|---:|---:|
| Verification URL | 1,584 | 1.6% |
| Measured purity | 9,540 | 9.9% |
| Quantity versus label | 28,538 | 29.5% |
| Endotoxin result | 84,289 | 87.1% |
| Test date | 3,268 | 3.4% |

## Verification by laboratory

Laboratory labels with at least 10 included records, in order of volume. A blank profile means TitrateLab publishes no profile for that label yet.

| Laboratory | Reports | With verification URL | Profile |
|---|---:|---:|---|
| Freedom Diagnostics | 65,634 | 100.0% | [profile](https://titratelab.com/labs/freedom-diagnostics?src=github) |
| Janoshik | 13,020 | 94.1% | [profile](https://titratelab.com/labs/janoshik?src=github) |
| Finnrick panel labs (anonymized) | 12,116 | 99.9% | [profile](https://titratelab.com/labs/finnrick?src=github) |
| Chromate | 1,594 | 99.5% | [profile](https://titratelab.com/labs/chromate?src=github) |
| ILS Laboratories | 742 | 88.1% | [profile](https://titratelab.com/labs/ils-laboratories?src=github) |
| Kovera Labs | 703 | 90.5% | [profile](https://titratelab.com/labs/kovera-labs?src=github) |
| Vanguard Laboratory | 637 | 71.0% | [profile](https://titratelab.com/labs/vanguard-laboratory?src=github) |
| Lab not recorded | 407 | 84.8% |  |
| TrustPointe Analytics | 360 | 88.9% | [profile](https://titratelab.com/labs/trustpointe-analytics?src=github) |
| Peptide Test | 340 | 62.4% | [profile](https://titratelab.com/labs/peptide-test?src=github) |
| Horizon Analytical | 202 | 48.5% | [profile](https://titratelab.com/labs/horizon-analytical?src=github) |
| BioRegen | 183 | 100.0% | [profile](https://titratelab.com/labs/bioregen?src=github) |
| Accumark Labs | 152 | 98.7% | [profile](https://titratelab.com/labs/accumark-labs?src=github) |
| Testides | 135 | 93.3% | [profile](https://titratelab.com/labs/testides?src=github) |
| Krause Analytical | 89 | 75.3% | [profile](https://titratelab.com/labs/krause-analytical?src=github) |
| Ethos Analytics | 74 | 86.5% | [profile](https://titratelab.com/labs/ethos-analytics?src=github) |
| Bioviridian | 60 | 100.0% | [profile](https://titratelab.com/labs/bioviridian?src=github) |
| BioAnalytical Laboratory | 59 | 100.0% |  |
| BTLabs | 51 | 78.4% | [profile](https://titratelab.com/labs/btlabs?src=github) |
| AV Analytics | 50 | 100.0% | [profile](https://titratelab.com/labs/av-analytics?src=github) |
| MZ Biolabs | 33 | 63.6% | [profile](https://titratelab.com/labs/mz-biolabs?src=github) |
| MDx BioAnalytical Laboratory | 24 | 100.0% | [profile](https://titratelab.com/labs/mdx-bioanalytical?src=github) |
| United Laboratories | 23 | 100.0% |  |
| Prime Analytical Laboratories | 19 | 100.0% |  |
| Optiq Health Labs | 13 | 100.0% |  |
| SR BIO LABS | 12 | 100.0% |  |
| BT Laboratories | 10 | 100.0% |  |

## What the figure means

A verification URL lets anyone compare the certificate they were shown with the copy the laboratory holds. A certificate without one can still be genuine; it simply cannot be checked without contacting the laboratory. A certificate with one can still be misused, for example by presenting a real certificate for a different batch, which is why the per-record pages on titratelab.com show the client and batch as printed.

## Method

- Population: all included records.
- A record is verifiable when the extracted verification URL field is non-empty. The URL itself is never published here.
- Source columns: `verifiable_records` and `test_records` in `data/latest/compounds.csv` and `labs.csv`.

## Limitations

- The presence of a URL is recorded at extraction time. Whether the link still resolves is not re-checked for this file.
- Some laboratories print a QR code rather than a URL; extraction records what it can read.

## See the records

Open any report at [titratelab.com/coa](https://titratelab.com/coa?src=github) to follow its verification link.
