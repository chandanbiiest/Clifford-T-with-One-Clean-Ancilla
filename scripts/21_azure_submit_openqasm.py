#!/usr/bin/env python3
"""Submit an OpenQASM program to a selected Azure Quantum target."""
from pathlib import Path
import argparse, json, os
from qdk.azure import Workspace

ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser()
p.add_argument("--target",required=True,help="Provider target name available in your workspace")
p.add_argument("--qasm",required=True,help="OpenQASM input file")
p.add_argument("--shots",type=int,default=500)
p.add_argument("--output",default="data/generated/azure_job_record.json")
args=p.parse_args()
connection=os.environ.get("AZURE_QUANTUM_CONNECTION_STRING")
if not connection:
    raise SystemExit("Set AZURE_QUANTUM_CONNECTION_STRING before running this script.")
workspace=Workspace.from_connection_string(connection)
target=workspace.get_targets(name=args.target)
program=Path(args.qasm).read_text()
job=target.submit(program,shots=args.shots)
job.wait_until_completed()
record={"target":args.target,"job_id":job.id,"status":job.details.status,"shots":args.shots}
if job.details.status=="Succeeded":
    try: record["results"]=job.get_results()
    except Exception as exc: record["results_note"]=str(exc)
out=ROOT/args.output; out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(record,indent=2,default=str)+"\n")
print(out)
