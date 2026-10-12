# Entries, certificates and how they are counted

The headline unit in this repository is the published entry. A certificate count is also reported, with the key that produced it, because the two differ and the difference matters when comparing archives.

## Entry

One published lab-report entry in the TitrateLab corpus. An entry is created when a certificate is collected from a source. The same physical certificate can be collected twice, for example once from a laboratory portal and once from a buyer community, and will then exist as two entries until it is merged.

## Certificate identifier

The manifest reports `totals.distinct_certificate_identifiers`, computed over all published entries as the number of distinct values of:

```
COALESCE(verify_url, lab_name || ':' || test_id)
```

- `verify_url` is the laboratory's verification link printed on the certificate. When two entries share one, they are one certificate.
- When a certificate has no verification link, the laboratory name and the laboratory's test number stand in for it.

This key is an upper bound on the number of distinct certificates. A certificate collected twice without a verification link and with two different test numbers counts twice. The public projection carries no file hashes, so a stricter hash-based count cannot be reproduced from the released files.

## The stricter internal count

TitrateLab's internal corpus keeps file hashes. On 2026-10-01 a deduplication by file hash, artifact hash, verification URL and laboratory test number resolved 112,858 published entries to 111,805 unique certificates, so about 99% of entries were distinct certificates on that date. That measurement is published here as a dated fact, not as a live number. The live upper bound is in every release manifest.

## Why both numbers are shown

Comparing archives by "number of COAs" is only meaningful when the unit is stated. The entry count is what the per-record search on titratelab.com returns. The certificate count is what a reader who wants distinct documents needs. Both are reported with their definitions so that neither can be mistaken for the other.
