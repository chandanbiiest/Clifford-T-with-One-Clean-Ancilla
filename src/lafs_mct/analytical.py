from __future__ import annotations

from pathlib import Path
import pandas as pd

from .metrics import latency_break_even


def load_resource_counts(path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    required = {"n", "family", "N_CX", "N_T", "D_T"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"missing columns: {sorted(missing)}")
    return df


def break_even_table(df: pd.DataFrame, tau_t: float = 1.0, tau_cx: float = 0.2) -> pd.DataFrame:
    rows = []
    for n, group in df.groupby("n"):
        by_family = group.set_index("family")
        s = by_family.loc["Static_S"]
        for fam in ("Dynamic_D2", "Mixed_D23"):
            c = by_family.loc[fam]
            rows.append({
                "n": int(n),
                "comparison": f"Static_S_to_{fam}",
                "threshold": latency_break_even(s.D_T, c.D_T, s.N_CX, c.N_CX, tau_t, tau_cx),
                "tau_T": tau_t,
                "tau_CX": tau_cx,
            })
    return pd.DataFrame(rows).sort_values(["n", "comparison"]).reset_index(drop=True)
