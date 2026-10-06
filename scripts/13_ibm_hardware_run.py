#!/usr/bin/env python3
"""Submit selected reference circuits to an IBM Quantum backend.

This script never creates result rows before a job actually completes.
"""
from pathlib import Path
import argparse, json, sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))
from lafs_mct.qiskit_circuits import coherent_c3x_reference, dynamic_c3x_reference
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2

p=argparse.ArgumentParser()
p.add_argument("--backend",default=None)
p.add_argument("--shots",type=int,default=4096)
p.add_argument("--family",choices=["coherent","dynamic","both"],default="both")
p.add_argument("--output",default="data/generated/ibm_hardware_job_record.json")
args=p.parse_args()
service=QiskitRuntimeService()
backend=service.backend(args.backend) if args.backend else service.least_busy(
    operational=True,simulator=False,dynamic_circuits=True
)
pm=generate_preset_pass_manager(backend=backend,optimization_level=2)
builders={"coherent":coherent_c3x_reference,"dynamic":dynamic_c3x_reference}
selected=builders if args.family=="both" else {args.family:builders[args.family]}
sampler=SamplerV2(backend)
record={"backend_id":backend.name,"shots":args.shots,"jobs":[]}
for name,builder in selected.items():
    isa=pm.run(builder(measure_output=True))
    job=sampler.run([isa],shots=args.shots)
    result=job.result()
    record["jobs"].append({
        "family":name,
        "job_id":job.job_id(),
        "status":str(job.status()),
        "result_repr":repr(result),
        "operation_counts":{str(k):int(v) for k,v in isa.count_ops().items()},
        "depth":int(isa.depth()),
    })
out=ROOT/args.output; out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(record,indent=2)+"\n")
print(out)
