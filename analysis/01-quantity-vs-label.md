# How often is the tested quantity within 10% of the label?

**Verdict:** 49.9% of 68,267 quantity results are within plus or minus 10% of the printed label. By compound, among the 35 with at least 100 quantity results, the share runs from 22.2% (LL-37) to 90.1% (Glutathione). 4,473 results are more than 10% under label. Purity, by contrast, is above 99% at the median for most compounds, so the quantity figure is where vials differ.

Release 2026-10-12, records observed through 2026-10-12.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../charts/quantity-within-label-dark.svg">
  <img alt="Share of tested vials within 10% of the printed label, fifteen most-tested compounds" src="../charts/quantity-within-label-light.svg" width="900">
</picture>

## By compound

Compounds with at least 100 quantity results, ranked by the share within 10% of label.

| Compound | Quantity results | Within 10% of label | More than 10% under label |
|---|---:|---:|---:|
| Glutathione | 797 | 90.1% | 31 (3.9%) |
| AHK-Cu | 119 | 67.2% | 8 (6.7%) |
| NAD+ | 2,726 | 65.7% | 162 (5.9%) |
| Mazdutide | 111 | 60.4% | 13 (11.7%) |
| Ipamorelin | 1,659 | 56.1% | 181 (10.9%) |
| Cagrilintide | 1,143 | 55.6% | 68 (5.9%) |
| GHK-Cu | 3,997 | 55.5% | 428 (10.7%) |
| PT-141 | 1,034 | 54.6% | 99 (9.6%) |
| Tirzepatide | 10,176 | 53.8% | 582 (5.7%) |
| Melanotan II | 1,092 | 52.9% | 100 (9.2%) |
| Melanotan I | 443 | 52.4% | 10 (2.3%) |
| Thymosin Beta-4 | 143 | 52.4% | 14 (9.8%) |
| SS-31 | 1,566 | 52.1% | 82 (5.2%) |
| Retatrutide | 16,225 | 51.1% | 1,008 (6.2%) |
| MOTS-C | 3,468 | 50.8% | 100 (2.9%) |
| Thymosin Alpha-1 | 675 | 49.5% | 31 (4.6%) |
| Epithalon | 1,088 | 49.0% | 42 (3.9%) |
| Kisspeptin | 533 | 47.8% | 65 (12.2%) |
| TB-500 | 1,785 | 46.8% | 109 (6.1%) |
| CJC-1295 | 844 | 46.6% | 142 (16.8%) |
| Tesamorelin | 4,002 | 45.5% | 286 (7.1%) |
| 5-Amino-1MQ | 913 | 45.5% | 68 (7.4%) |
| GHRP-6 | 112 | 45.5% | 17 (15.2%) |
| ARA-290 | 439 | 44.6% | 10 (2.3%) |
| DSIP | 787 | 42.9% | 76 (9.7%) |
| KPV | 1,524 | 41.0% | 73 (4.8%) |
| AOD-9604 | 694 | 40.2% | 67 (9.7%) |
| Selank | 1,236 | 39.1% | 48 (3.9%) |
| BPC-157 | 3,623 | 38.9% | 291 (8.0%) |
| Semaglutide | 1,818 | 38.9% | 86 (4.7%) |
| Semax | 1,339 | 32.6% | 29 (2.2%) |
| Sermorelin | 755 | 31.5% | 34 (4.5%) |
| CJC-1295 w/ DAC | 190 | 28.9% | 10 (5.3%) |
| SNAP-8 | 206 | 27.7% | 1 (0.5%) |
| LL-37 | 207 | 22.2% | 2 (1.0%) |

## What the figure means

A laboratory that reports a tested quantity states how much of the compound it found in the vial, usually in milligrams. The printed label states how much the vial is supposed to contain. The deviation is the tested quantity relative to the label, in percent. "Within 10%" counts results between minus 10% and plus 10%.

Blends read low more often than single compounds. A blend label states the total of several components, and a laboratory that quantifies only one of them reports a shortfall that is partly an artefact of what was measured. Treat blend rows as describing the measurement, not necessarily the vial.

## Method

- Population: included records with a quantity-versus-label figure (68,267 of 96,805).
- Deviation is against the printed label only. Where a laboratory also reports deviation against a separate batch claim, that figure is not substituted.
- Cell floor: every compound row holds at least 10 records; the table above additionally requires 100 quantity results so that a share is not driven by a handful of vials.
- Source columns: `quantity_results`, `quantity_within_10pct_pct`, `quantity_more_than_10pct_under_label` in `data/latest/compounds.csv`.

## Limitations

- 28,538 included records have no quantity figure, most often because the laboratory did not quantify or the report did not print a label amount. They are absent from every share on this page.
- Quantification methods differ between laboratories, and a vial tested twice can yield two figures. The corpus records what each report printed.
- The corpus is not a random sample. Vials are sent for testing by people who chose to test them.

## See the records

Search individual reports, with laboratory, client and batch as printed, at [titratelab.com/coa](https://titratelab.com/coa?src=github). Per-record, vendor-identified queries are available through the [Data API](https://titratelab.com/developer?src=github).
