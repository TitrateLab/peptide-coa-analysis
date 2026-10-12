#!/usr/bin/env python3
"""Render README, analyses, charts and citation metadata from ``data/latest``.

Every number in the rendered Markdown comes from the release files, so a new
release regenerates the whole repository text::

    python scripts/build_release.py            # render into the repository root
    python scripts/build_release.py --check    # validate data/latest, render nothing

The check mode is what CI runs: files listed in the manifest exist and hash
correctly, every cell respects the minimum cell size, and no column could carry
a vendor, client, batch, submitter or certificate identity.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from collections import defaultdict
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "latest"
TEMPLATES = ROOT / "templates"
CHARTS = ROOT / "charts"

FORBIDDEN_COLUMNS = {
    "vendor", "vendor_id", "manufacturer", "manufacturer_id", "client", "client_raw",
    "submitter", "submitted_by", "batch", "batch_id", "certificate", "certificate_slug",
    "test_id", "verify_url", "png_url", "sample", "channel_id", "guild_id",
}
RELEASE_TABLES = ("compounds", "compound_month", "labs", "lab_month", "months")
OTHER_LAB_LABEL = "Other labs"

THEMES = {
    "light": {
        "surface": "#fcfcfb", "text": "#0b0b0b", "text2": "#52514e", "muted": "#8a8984",
        "grid": "#e9e8e4", "series": ["#2a78d6", "#eb6834", "#1baf7a", "#eda100"],
        "other": "#b9b8b2", "accent": "#2a78d6",
    },
    "dark": {
        "surface": "#1a1a19", "text": "#ffffff", "text2": "#c3c2b7", "muted": "#8d8c84",
        "grid": "#2d2d2b", "series": ["#3987e5", "#d95926", "#199e70", "#c98500"],
        "other": "#5e5d59", "accent": "#3987e5",
    },
}


# --------------------------------------------------------------------------- load


def _num(value: str) -> Any:
    if value is None or value == "":
        return None
    try:
        if "." in value:
            return float(value)
        return int(value)
    except ValueError:
        return value


def _read_csv(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8", newline="") as handle:
        rows = []
        for raw in csv.DictReader(handle):
            rows.append({k: (_num(v) if k not in ("compound", "lab", "month", "profile_url",
                                                   "earliest_test_date", "latest_test_date") else v)
                         for k, v in raw.items()})
        return rows


def load(data_dir: Path = DATA) -> dict[str, Any]:
    manifest = json.loads((data_dir / "manifest.json").read_text(encoding="utf-8"))
    out: dict[str, Any] = {"manifest": manifest}
    for name in RELEASE_TABLES:
        out[name] = _read_csv(data_dir / f"{name}.csv")
    return out


# -------------------------------------------------------------------------- check


def check(data_dir: Path = DATA) -> list[str]:
    problems: list[str] = []
    manifest_path = data_dir / "manifest.json"
    if not manifest_path.is_file():
        return [f"missing {manifest_path}"]
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    floor = int(manifest.get("minimum_cell_size", 0) or 0)
    if floor < 3:
        problems.append(f"minimum_cell_size is {floor}; expected at least 3")
    if not manifest.get("vendor_blind"):
        problems.append("manifest does not declare vendor_blind")
    for name, meta in (manifest.get("files") or {}).items():
        path = data_dir / name
        if not path.is_file():
            problems.append(f"listed file missing: {name}")
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != meta.get("sha256"):
            problems.append(f"sha256 mismatch: {name}")
    for name in RELEASE_TABLES:
        path = data_dir / f"{name}.csv"
        if not path.is_file():
            problems.append(f"missing table: {name}.csv")
            continue
        with path.open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            header = [h.lower() for h in (reader.fieldnames or [])]
            bad = sorted(set(header) & FORBIDDEN_COLUMNS)
            if bad:
                problems.append(f"{name}.csv carries identity columns: {bad}")
            for i, row in enumerate(reader, start=2):
                n = int(row.get("test_records") or 0)
                if n < floor:
                    problems.append(f"{name}.csv line {i}: test_records {n} below floor {floor}")
                    break
    version = manifest.get("version")
    release_manifest = data_dir.parent / "releases" / str(version) / "manifest.json"
    if release_manifest.is_file():
        if release_manifest.read_bytes() != manifest_path.read_bytes():
            problems.append(f"latest/manifest.json differs from releases/{version}/manifest.json")
    else:
        problems.append(f"releases/{version}/manifest.json is missing")
    return problems


# --------------------------------------------------------------------- view model


def _share(part: Any, whole: Any) -> float | None:
    if not whole:
        return None
    return 100.0 * float(part or 0) / float(whole)


def _month_add(month: str, delta: int) -> str:
    y, m = int(month[:4]), int(month[5:7])
    idx = y * 12 + (m - 1) + delta
    return f"{idx // 12:04d}-{idx % 12 + 1:02d}"


def _month_label(month: str) -> str:
    return date(int(month[:4]), int(month[5:7]), 1).strftime("%b %Y")


def _quarter(month: str) -> str:
    return f"{month[:4]} Q{(int(month[5:7]) - 1) // 3 + 1}"


def build_view(d: dict[str, Any]) -> dict[str, Any]:
    m = d["manifest"]
    cov, miss, totals = m["coverage"], m["missing_data"], m.get("totals") or {}
    compounds = sorted(d["compounds"], key=lambda r: -r["test_records"])
    included = cov["included_records"]
    purity_results = sum(r["purity_results"] for r in compounds)
    zero_results = sum(r["zero_identity_results"] for r in compounds)
    quantity_results = sum(r["quantity_results"] for r in compounds)
    endotoxin_results = sum(r["endotoxin_results"] for r in compounds)
    verifiable = sum(r["verifiable_records"] for r in compounds)
    within = sum(
        (r["quantity_within_10pct_pct"] or 0) / 100.0 * r["quantity_results"]
        for r in compounds if r["quantity_results"]
    )

    # Quantity versus label.
    q_rows = [r for r in compounds if r["quantity_results"] >= 100 and r["quantity_within_10pct_pct"] is not None]
    q_rows.sort(key=lambda r: (-r["quantity_within_10pct_pct"], -r["quantity_results"]))
    q_chart = sorted(sorted(q_rows, key=lambda r: -r["quantity_results"])[:15],
                     key=lambda r: -r["quantity_within_10pct_pct"])
    for r in compounds:
        r["under_label_share"] = _share(r["quantity_more_than_10pct_under_label"], r["quantity_results"])
        r["endotoxin_share"] = _share(r["endotoxin_results"], r["test_records"])
        r["zero_share"] = _share(r["zero_identity_results"], r["purity_results"] + r["zero_identity_results"])
        r["verifiable_share"] = _share(r["verifiable_records"], r["test_records"])

    # Endotoxin testing rate.
    e_rows = [r for r in compounds if r["test_records"] >= 300]
    e_chart = sorted(e_rows, key=lambda r: -r["endotoxin_share"])[:15]

    # Zero identity.
    z_rows = [r for r in compounds if (r["purity_results"] + r["zero_identity_results"]) >= 300]
    z_chart = sorted(z_rows, key=lambda r: -r["zero_share"])[:15]

    # Months. Cut at the last full month before observed_through.
    observed = (m.get("observed_through") or m["version"])[:7]
    last_full = _month_add(observed, -1)
    months = sorted((r for r in d["months"] if r["month"] <= last_full), key=lambda r: r["month"])
    months_24 = months[-24:]
    recent_12 = months[-12:]
    prior_12 = months[-24:-12]
    recent_total = sum(r["test_records"] for r in recent_12)
    prior_total = sum(r["test_records"] for r in prior_12)

    # Compound lines: the four largest compounds over the last 12 full months.
    cm = defaultdict(dict)
    for r in d["compound_month"]:
        cm[r["compound"]][r["month"]] = r["test_records"]
    window = [r["month"] for r in months_24]
    recent_window = set(r["month"] for r in recent_12)
    ranked = sorted(cm, key=lambda c: -sum(v for k, v in cm[c].items() if k in recent_window))
    top4 = ranked[:4]
    compound_series = {c: [cm[c].get(mo) for mo in window] for c in top4}

    # Lab mix by quarter: four largest labs plus everything else.
    lm = defaultdict(lambda: defaultdict(int))
    for r in d["lab_month"]:
        if r["month"] <= last_full:
            lm[r["lab"]][_quarter(r["month"])] += r["test_records"]
    quarters = sorted({q for lab in lm.values() for q in lab})[-8:]
    lab_totals = {lab: sum(v for q, v in qs.items() if q in quarters) for lab, qs in lm.items()}
    named = [lab for lab in sorted(lab_totals, key=lambda l: -lab_totals[l]) if lab != OTHER_LAB_LABEL]
    lab_top = named[:4]
    lab_series: dict[str, list[float | None]] = {}
    q_tot = {q: sum(lm[lab].get(q, 0) for lab in lm) for q in quarters}
    for lab in lab_top:
        lab_series[lab] = [_share(lm[lab].get(q, 0), q_tot[q]) for q in quarters]
    rest = [sum(lm[lab].get(q, 0) for lab in lm if lab not in lab_top) for q in quarters]
    lab_series["All other labs"] = [_share(v, q_tot[q]) for v, q in zip(rest, quarters)]
    labs = sorted(d["labs"], key=lambda r: -r["test_records"])
    for r in labs:
        r["endotoxin_share"] = _share(r["endotoxin_results"], r["test_records"])
        r["verifiable_share"] = _share(r["verifiable_records"], r["test_records"])
        r["share_of_included"] = _share(r["test_records"], included)

    return {
        "m": m, "cov": cov, "miss": miss, "totals": totals,
        "generated_date": m["generated_at"][:10],
        "compounds": compounds, "top_compounds": compounds[:15],
        "included": included, "purity_results": purity_results, "zero_results": zero_results,
        "quantity_results": quantity_results, "endotoxin_results": endotoxin_results,
        "verifiable": verifiable,
        "within_share": _share(within, quantity_results),
        "under_label_total": sum(r["quantity_more_than_10pct_under_label"] for r in compounds),
        "endotoxin_share": _share(endotoxin_results, included),
        "zero_share": _share(zero_results, purity_results + zero_results),
        "verifiable_share": _share(verifiable, included),
        "q_rows": q_rows, "q_best": q_rows[0] if q_rows else None, "q_worst": q_rows[-1] if q_rows else None,
        "q_chart": q_chart, "e_chart": e_chart, "e_rows": sorted(e_rows, key=lambda r: -r["endotoxin_share"]),
        "z_chart": z_chart, "z_rows": sorted(z_rows, key=lambda r: -r["zero_share"]),
        "months": months, "months_24": months_24, "last_full": last_full,
        "recent_12": recent_12, "prior_12": prior_12,
        "recent_total": recent_total, "prior_total": prior_total,
        "growth_pct": (_share(recent_total - prior_total, prior_total) if prior_total else None),
        "window": window, "compound_series": compound_series, "top4": top4,
        "quarters": quarters, "lab_series": lab_series, "lab_top": lab_top, "labs": labs,
        "labs_named": [r for r in labs if r["lab"] != OTHER_LAB_LABEL],
    }


# ------------------------------------------------------------------------- charts


def _mpl():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    matplotlib.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"],
        "svg.fonttype": "none",
        "svg.hashsalt": "titratelab/peptide-coa-analysis",  # deterministic element ids
        "axes.unicode_minus": False,
    })
    return plt


def _frame(plt, theme: dict[str, str], width: float, height: float):
    fig = plt.figure(figsize=(width, height), dpi=100)
    fig.patch.set_facecolor(theme["surface"])
    return fig


def _finish(fig, ax, theme, title, subtitle, note, left=0.30, bottom=0.14, top=0.80):
    ax.set_facecolor(theme["surface"])
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(colors=theme["text2"], labelsize=9, length=0)
    fig.text(0.02, 0.955, title, ha="left", va="top", fontsize=13, fontweight="semibold", color=theme["text"])
    fig.text(0.02, 0.905, subtitle, ha="left", va="top", fontsize=9.5, color=theme["text2"])
    fig.text(0.02, 0.025, note, ha="left", va="bottom", fontsize=8.2, color=theme["muted"])
    fig.subplots_adjust(left=left, right=0.97, bottom=bottom, top=top)


def _save(fig, name: str, mode: str, png: bool) -> None:
    CHARTS.mkdir(parents=True, exist_ok=True)
    # No timestamps in the output: an unchanged release must render byte-identical files.
    fig.savefig(CHARTS / f"{name}-{mode}.svg", format="svg", facecolor=fig.get_facecolor(),
                metadata={"Date": None, "Creator": "titratelab/peptide-coa-analysis"})
    if png and mode == "light":
        fig.savefig(CHARTS / f"{name}.png", format="png", dpi=200, facecolor=fig.get_facecolor(),
                    metadata={"Software": "titratelab/peptide-coa-analysis"})


def chart_hbar(name, rows, label_key, value_key, title, subtitle, note, fmt="{:.1f}%", xmax=None):
    plt = _mpl()
    for mode, theme in THEMES.items():
        n = len(rows)
        fig = _frame(plt, theme, 9.0, 0.38 * n + 1.9)
        ax = fig.add_subplot(111)
        labels = [r[label_key] for r in rows][::-1]
        values = [float(r[value_key] or 0) for r in rows][::-1]
        ax.barh(range(n), values, height=0.52, color=theme["accent"], zorder=3)
        ax.set_yticks(range(n))
        ax.set_yticklabels(labels, color=theme["text2"])
        top = xmax or max(values + [1.0]) * 1.18
        ax.set_xlim(0, top)
        ax.xaxis.grid(True, color=theme["grid"], linewidth=1, zorder=0)
        ax.set_axisbelow(True)
        xticks = [t for t in ax.get_xticks() if 0 <= t <= top]
        ax.set_xticks(xticks)
        ax.set_xticklabels([("{:.0f}%" if fmt.endswith("%") else fmt).format(t) for t in xticks], color=theme["text2"])
        for y, v in enumerate(values):
            ax.text(v + top * 0.012, y, fmt.format(v), va="center", ha="left", fontsize=9, color=theme["text2"])
        _finish(fig, ax, theme, title, subtitle, note, left=0.30, bottom=1.1 / (0.38 * n + 1.9), top=1 - 1.05 / (0.38 * n + 1.9))
        _save(fig, name, mode, png=True)
        plt.close(fig)


def chart_lines(name, x_labels, series, title, subtitle, note, yfmt="{:,.0f}", area=False, ylim=None, ylabel=None):
    plt = _mpl()
    for mode, theme in THEMES.items():
        fig = _frame(plt, theme, 9.0, 4.6)
        ax = fig.add_subplot(111)
        xs = list(range(len(x_labels)))
        palette = theme["series"]
        for i, (label, ys) in enumerate(series.items()):
            color = theme["other"] if label == "All other labs" else palette[i % len(palette)]
            pts = [(x, y) for x, y in zip(xs, ys) if y is not None]
            if not pts:
                continue
            px, py = zip(*pts)
            ax.plot(px, py, color=color, linewidth=2, solid_capstyle="round", solid_joinstyle="round", zorder=3)
            ax.plot([px[-1]], [py[-1]], marker="o", markersize=8, color=color, markeredgecolor=theme["surface"], markeredgewidth=2, zorder=4)
            if area and len(series) == 1:
                ax.fill_between(px, py, color=color, alpha=0.10, linewidth=0, zorder=2)
            if len(series) > 1:
                ax.text(px[-1] + 0.25, py[-1], label, va="center", ha="left", fontsize=8.5, color=theme["text2"])
        ax.set_xticks(xs[::3])
        ax.set_xticklabels([_month_label(x) if len(x) == 7 else x for x in x_labels[::3]], color=theme["text2"], rotation=0)
        ax.set_xlim(-0.5, len(xs) - 0.5 + (2.8 if len(series) > 1 else 0.6))
        if ylim:
            ax.set_ylim(*ylim)
        else:
            ax.set_ylim(0, None)
        ax.yaxis.grid(True, color=theme["grid"], linewidth=1, zorder=0)
        ax.set_axisbelow(True)
        ticks = [t for t in ax.get_yticks() if t >= 0]
        ax.set_yticks(ticks)
        ax.set_yticklabels([yfmt.format(t) for t in ticks], color=theme["text2"])
        if ylabel:
            ax.set_ylabel(ylabel, color=theme["text2"], fontsize=9)
        if len(series) > 1:
            handles = [plt.Line2D([0], [0], color=(theme["other"] if lab == "All other labs" else palette[i % len(palette)]), linewidth=2)
                       for i, lab in enumerate(series)]
            ax.legend(handles, list(series), frameon=False, loc="upper left", fontsize=8.5, labelcolor=theme["text2"], ncol=2)
        _finish(fig, ax, theme, title, subtitle, note, left=0.085, bottom=0.14, top=0.80)
        _save(fig, name, mode, png=True)
        plt.close(fig)


def chart_stacked_share(name, x_labels, series, title, subtitle, note):
    plt = _mpl()
    for mode, theme in THEMES.items():
        fig = _frame(plt, theme, 9.0, 4.8)
        ax = fig.add_subplot(111)
        xs = list(range(len(x_labels)))
        bottom = [0.0] * len(xs)
        palette = theme["series"]
        handles = []
        for i, (label, ys) in enumerate(series.items()):
            color = theme["other"] if label == "All other labs" else palette[i % len(palette)]
            vals = [float(y or 0) for y in ys]
            ax.bar(xs, vals, bottom=bottom, width=0.62, color=color, edgecolor=theme["surface"], linewidth=2, zorder=3)
            for x, (b, v) in enumerate(zip(bottom, vals)):
                if v >= 12:
                    ax.text(x, b + v / 2, f"{v:.0f}%", ha="center", va="center", fontsize=8.5,
                            color=("#ffffff" if label != "All other labs" or mode == "dark" else theme["text"]))
            bottom = [b + v for b, v in zip(bottom, vals)]
            handles.append(plt.Rectangle((0, 0), 1, 1, color=color))
        ax.set_xticks(xs)
        ax.set_xticklabels(x_labels, color=theme["text2"])
        ax.set_ylim(0, 100)
        ax.set_yticks([0, 25, 50, 75, 100])
        ax.set_yticklabels([f"{t}%" for t in [0, 25, 50, 75, 100]], color=theme["text2"])
        ax.yaxis.grid(True, color=theme["grid"], linewidth=1, zorder=0)
        ax.set_axisbelow(True)
        ax.legend(handles, list(series), frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.12),
                  fontsize=8.5, labelcolor=theme["text2"], ncol=min(5, len(series)))
        _finish(fig, ax, theme, title, subtitle, note, left=0.075, bottom=0.22, top=0.80)
        _save(fig, name, mode, png=True)
        plt.close(fig)


def render_charts(v: dict[str, Any]) -> None:
    src = f"TitrateLab vendor-blind snapshot {v['m']['version']}, minimum cell size {v['m']['minimum_cell_size']}. CC BY 4.0."
    chart_hbar(
        "quantity-within-label", v["q_chart"], "compound", "quantity_within_10pct_pct",
        "Share of tested vials within 10% of the printed label",
        f"Fifteen most-tested compounds with at least 100 quantity results. {v['quantity_results']:,} quantity results overall.",
        src, xmax=100,
    )
    chart_hbar(
        "endotoxin-testing-rate", v["e_chart"], "compound", "endotoxin_share",
        "Share of lab reports that include any endotoxin result",
        f"Compounds with at least 300 reports. Overall: {v['endotoxin_share']:.1f}% of {v['included']:,} included reports.",
        src, xmax=100,
    )
    chart_hbar(
        "zero-identity-share", v["z_chart"], "compound", "zero_share",
        "Share of purity results reported at zero",
        f"Zero means the target compound was not identified. Compounds with at least 300 purity results. Overall: {v['zero_share']:.2f}%.",
        src, fmt="{:.2f}%",
    )
    chart_lines(
        "testing-volume", v["window"], {"All included reports": [r["test_records"] for r in v["months_24"]]},
        "Published lab reports by test month",
        f"Last 24 full months to {_month_label(v['last_full'])}. Months below the cell floor are omitted.",
        src, area=True,
    )
    chart_lines(
        "compound-volume", v["window"], v["compound_series"],
        "Reports per month for the four most-tested compounds",
        f"Ranked by reports in the last 12 full months. Gaps are months below the cell floor.",
        src,
    )
    chart_stacked_share(
        "lab-mix", v["quarters"], v["lab_series"],
        "Which laboratories issued the reports, by quarter",
        "Share of included reports. Four largest laboratories by volume; everything else combined.",
        src,
    )


# ------------------------------------------------------------------------ render


def _env():
    from jinja2 import Environment, FileSystemLoader, StrictUndefined
    env = Environment(loader=FileSystemLoader(str(TEMPLATES)), undefined=StrictUndefined,
                      trim_blocks=True, lstrip_blocks=True, keep_trailing_newline=True)
    env.filters["comma"] = lambda n: f"{int(n):,}" if n is not None else "n/a"
    env.filters["pct1"] = lambda x: f"{x:.1f}%" if x is not None else "n/a"
    env.filters["pct2"] = lambda x: f"{x:.2f}%" if x is not None else "n/a"
    env.filters["num2"] = lambda x: f"{x:.2f}" if x is not None else "n/a"
    env.filters["signed1"] = lambda x: (f"{x:+.1f}%" if x is not None else "n/a")
    env.filters["monthlabel"] = _month_label
    return env


def render(v: dict[str, Any], out: Path = ROOT) -> list[Path]:
    env = _env()
    written: list[Path] = []
    targets = {
        "README.md.j2": out / "README.md",
        "CITATION.cff.j2": out / "CITATION.cff",
    }
    for tpl in sorted((TEMPLATES / "analysis").glob("*.md.j2")):
        targets[f"analysis/{tpl.name}"] = out / "analysis" / tpl.name[:-3]
    for name, target in targets.items():
        text = env.get_template(name).render(**v)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
        written.append(target)
    return written


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=DATA)
    parser.add_argument("--check", action="store_true", help="validate only")
    parser.add_argument("--no-charts", action="store_true")
    args = parser.parse_args()
    problems = check(args.data)
    if problems:
        for p in problems:
            print(f"FAIL {p}", file=sys.stderr)
        return 1
    print(f"OK data/latest validates ({args.data})")
    if args.check:
        return 0
    v = build_view(load(args.data))
    if not args.no_charts:
        render_charts(v)
        print(f"charts rendered into {CHARTS}")
    for path in render(v):
        print(f"rendered {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
