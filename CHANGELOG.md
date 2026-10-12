# Changelog

Every entry is a release of `data/`. Numbers are copied from that release's `manifest.json`.

## 2026-10-12

First public release. Built from projection `20261012T021040Z`, records observed through 2026-10-12T00:23:06Z.

- 116,363 published entries; 115,076 distinct certificate identifiers (upper bound).
- 96,805 included records across 68 compounds; 17,774 excluded as non-peptide or unresolved; 124 in 54 compounds below the floor.
- 26 named laboratories; 19 folded into "Other labs".
- Tables: compounds, compound by month, laboratories, laboratory by month, months. Minimum cell size 10.
- Schema version 2. The compound table keeps the shape of the file served at titratelab.com/data; the month and laboratory tables are new in this release.

Headline figures in this release:

- 49.9% of 68,267 quantity results are within 10% of the printed label.
- 12.9% of included reports carry an endotoxin result.
- 0.77% of purity results are reported at zero (compound not identified).
- 98.4% of included reports carry a laboratory verification URL.
