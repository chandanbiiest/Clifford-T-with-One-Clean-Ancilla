#!/usr/bin/env python3
"""Demonstrate the current Microsoft Quantum resource-estimation interface.

The manuscript's logical candidates should be translated to an application
model before drawing physical-resource conclusions. This script records the
architecture and estimation settings explicitly; it is a starting point for
that translation rather than a pre-filled hardware result.
"""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
settings={
    "architecture_model":"GateBased",
    "error_rate":1e-4,
    "gate_time_ns":100,
    "measurement_time_ns":500,
    "max_error":0.01,
    "qec":"SurfaceCode",
    "factory":"RoundBasedFactory",
    "status":"configuration-only; supply an application model before estimation"
}
out=ROOT/"data/generated/resource_estimator_settings.json"
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(settings,indent=2)+"\n")
print(out)

# Current QDK pattern, intentionally left behind a guard until an application
# model for the selected LAFS-MCT candidate is supplied:
# from qdk.qre import estimate
# from qdk.qre.models import GateBased, SurfaceCode, RoundBasedFactory
# arch = GateBased(error_rate=1e-4, gate_time=100, measurement_time=500)
# results = estimate(app, arch,
#                    isa_query=SurfaceCode.q() * RoundBasedFactory.q(),
#                    max_error=0.01)
# print(results.as_frame())
