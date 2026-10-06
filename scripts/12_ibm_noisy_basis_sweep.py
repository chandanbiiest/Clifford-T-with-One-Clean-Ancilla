#!/usr/bin/env python3
"""Run all 16 computational-basis C3X cases on a backend-derived Aer model."""
from pathlib import Path
import argparse, csv, sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from lafs_mct.qiskit_circuits import coherent_c3x_reference, dynamic_c3x_reference, prepare_basis_case

from qiskit_aer import AerSimulator
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService

p = argparse.ArgumentParser()
p.add_argument("--backend", default=None)
p.add_argument("--shots", type=int, default=4096)
p.add_argument("--seed", type=int, default=314159)
p.add_argument("--output", default="data/generated/ibm_noisy_basis_sweep.csv")
args = p.parse_args()
service = QiskitRuntimeService()
backend = service.backend(args.backend) if args.backend else service.least_busy(
    operational=True, simulator=False, dynamic_circuits=True
)
sim = AerSimulator.from_backend(backend)
pm = generate_preset_pass_manager(target=sim.target, optimization_level=1)
rows=[]
for family, builder in (("coherent", coherent_c3x_reference), ("dynamic", dynamic_c3x_reference)):
    for x in range(16):
        c1=(x>>3)&1; c2=(x>>2)&1; c3=(x>>1)&1; t=x&1
        qc=builder(measure_output=True)
        # Insert preparation at circuit front by composition.
        from qiskit import QuantumCircuit
        prep=QuantumCircuit(qc.num_qubits, qc.num_clbits)
        for bit,qidx in zip((c1,c2,c3,t),(0,1,2,4)):
            if bit: prep.x(qidx)
        full=prep.compose(qc)
        isa=pm.run(full)
        job=sim.run(isa, shots=args.shots, seed_simulator=args.seed)
        counts=job.result().get_counts()
        expected=t ^ (c1 & c2 & c3)
        # Qiskit formats multiple classical registers as space-separated groups in
        # reverse register order. The output register was added last, hence it is
        # the left-most group for the dynamic circuit.
        good=0
        for key,count in counts.items():
            groups=key.split()
            observed=int(groups[0][-1])
            if observed==expected: good += count
        rows.append({"backend_id":backend.name,"family":family,"input":f"{c1}{c2}{c3}{t}",
                     "expected_target":expected,"shots":args.shots,"success_probability":good/args.shots,
                     "seed":args.seed})
out=ROOT/args.output; out.parent.mkdir(parents=True,exist_ok=True)
with out.open("w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
print(out)
