#!/usr/bin/env python3
"""Capture a reproducible backend snapshot from IBM Quantum.

Credentials are read by QiskitRuntimeService from its standard account store.
"""
from pathlib import Path
import argparse, sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from lafs_mct.backend_io import capture_ibm_backend, write_json

p = argparse.ArgumentParser()
p.add_argument("--backend", default=None, help="Backend name; omit for least-busy dynamic backend")
p.add_argument("--output", default="data/generated/ibm_backend_snapshot.json")
args = p.parse_args()

from qiskit_ibm_runtime import QiskitRuntimeService
service = QiskitRuntimeService()
backend = service.backend(args.backend) if args.backend else service.least_busy(
    operational=True, simulator=False, dynamic_circuits=True
)
payload = capture_ibm_backend(backend)
write_json(ROOT / args.output, payload)
print(f"Captured {backend.name} -> {ROOT / args.output}")
