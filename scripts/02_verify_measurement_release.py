#!/usr/bin/env python3
from pathlib import Path
import sys, json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from lafs_mct.numpy_verify import verify_measurement_release, truth_table_rows

out = ROOT / "data/generated"
out.mkdir(parents=True, exist_ok=True)
result = verify_measurement_release()
(out / "measurement_release_verification.json").write_text(json.dumps(result, indent=2) + "\n")
pd.DataFrame(truth_table_rows()).to_csv(out / "c3x_truth_table.csv", index=False)
print(json.dumps(result, indent=2))
if result["max_error"] > 1e-12:
    raise SystemExit("verification failed")
