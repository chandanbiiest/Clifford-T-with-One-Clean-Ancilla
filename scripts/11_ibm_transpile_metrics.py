#!/usr/bin/env python3
"""Compile coherent and dynamic C3X references to an IBM backend Target."""
from pathlib import Path
import argparse, json, sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from lafs_mct.qiskit_circuits import coherent_c3x_reference, dynamic_c3x_reference

from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService

p = argparse.ArgumentParser()
p.add_argument("--backend", default=None)
p.add_argument("--optimization-level", type=int, default=2)
p.add_argument("--output", default="data/generated/ibm_transpile_metrics.json")
args = p.parse_args()

service = QiskitRuntimeService()
backend = service.backend(args.backend) if args.backend else service.least_busy(
    operational=True, simulator=False, dynamic_circuits=True
)
pm = generate_preset_pass_manager(backend=backend, optimization_level=args.optimization_level)

circuits = {
    "coherent": coherent_c3x_reference(measure_output=True),
    "dynamic": dynamic_c3x_reference(measure_output=True),
}
result = {"backend_id": backend.name, "optimization_level": args.optimization_level, "circuits": {}}
for name, qc in circuits.items():
    isa = pm.run(qc)
    counts = {str(k): int(v) for k, v in isa.count_ops().items()}
    twoq = 0
    for item in isa.data:
        if len(item.qubits) == 2:
            twoq += 1
    entry = {
        "depth": int(isa.depth()),
        "size": int(isa.size()),
        "two_qubit_count": int(twoq),
        "operation_counts": counts,
        "num_qubits": int(isa.num_qubits),
        "num_clbits": int(isa.num_clbits),
        "qasm3_export_note": "Use qiskit.qasm3.dumps(isa) if a text archive is required."
    }
    if name == "coherent":
        try:
            entry["estimated_duration_s"] = float(isa.estimate_duration(backend.target, unit="s"))
        except Exception as exc:
            entry["estimated_duration_s"] = None
            entry["duration_note"] = str(exc)
    else:
        entry["estimated_duration_s"] = None
        entry["duration_note"] = "Control-flow timing should be taken from backend execution/scheduler timing rather than simple-circuit duration estimation."
    result["circuits"][name] = entry

out = ROOT / args.output
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
