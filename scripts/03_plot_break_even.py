#!/usr/bin/env python3
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "data/generated/latency_break_even_thresholds.csv"
if not path.exists():
    raise SystemExit("Run scripts/01_reproduce_analytical.py first")
df = pd.read_csv(path)
fig, ax = plt.subplots(figsize=(6.2, 4.0))
for name, g in df.groupby("comparison"):
    ax.plot(g["n"], g["threshold"], marker="o", label=name.replace("Static_S_to_", "S vs "))
ax.set_xlabel("Number of controls, n")
ax.set_ylabel("Admissible normalized measurement + feedforward latency")
ax.grid(True, alpha=0.25)
ax.legend()
fig.tight_layout()
out = ROOT / "data/generated/latency_break_even.png"
fig.savefig(out, dpi=300)
print(out)
