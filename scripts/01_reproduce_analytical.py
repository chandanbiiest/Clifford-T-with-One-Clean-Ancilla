#!/usr/bin/env python3
from pathlib import Path
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from lafs_mct.analytical import load_resource_counts, break_even_table
from lafs_mct.metrics import exact_removed_work_threshold, first_order_removed_work_threshold

src = ROOT / "data/source/paper_resource_counts.csv"
out = ROOT / "data/generated"
out.mkdir(parents=True, exist_ok=True)

df = load_resource_counts(src)
thr = break_even_table(df, tau_t=1.0, tau_cx=0.2)
thr.to_csv(out / "latency_break_even_thresholds.csv", index=False)

exact = exact_removed_work_threshold(1e-4, 1e-3, 4, 2)
first = first_order_removed_work_threshold(1e-4, 1e-3, 4, 2)
pd.DataFrame([{
    "epsilon_T": 1e-4,
    "epsilon_CX": 1e-3,
    "removed_T": 4,
    "removed_CX": 2,
    "exact_measurement_error_threshold": exact,
    "first_order_threshold": first,
    "exact_percent": 100.0 * exact,
}]).to_csv(out / "reliability_break_even.csv", index=False)

print(thr.to_string(index=False))
print(f"Exact isolated measurement-error threshold: {exact:.12g} ({100*exact:.6f}%)")
