from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from typing import Any


def _jsonable(value: Any):
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, (list, tuple)):
        return [_jsonable(x) for x in value]
    if isinstance(value, dict):
        return {str(k): _jsonable(v) for k, v in value.items()}
    return str(value)


def capture_ibm_backend(backend) -> dict:
    target = backend.target
    cmap = getattr(backend, "coupling_map", None)
    edges = [] if cmap is None else [list(e) for e in cmap.get_edges()]
    qubits = []
    for i in range(backend.num_qubits):
        try:
            qp = backend.qubit_properties(i)
            qubits.append({"index": i, "t1": qp.t1, "t2": qp.t2, "frequency": qp.frequency})
        except Exception as exc:
            qubits.append({"index": i, "error": str(exc)})
    instructions = []
    for name in sorted(target.operation_names):
        inst_map = target[name]
        for qargs, prop in inst_map.items():
            instructions.append({
                "name": name,
                "qargs": None if qargs is None else list(qargs),
                "duration_s": None if prop is None else getattr(prop, "duration", None),
                "error": None if prop is None else getattr(prop, "error", None),
            })
    return {
        "backend_id": backend.name,
        "captured_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "num_qubits": backend.num_qubits,
        "supported_instructions": sorted(getattr(backend, "supported_instructions", [])),
        "coupling_edges": edges,
        "qubits": qubits,
        "instructions": instructions,
    }


def write_json(path: str | Path, payload: dict):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(_jsonable(payload), indent=2, sort_keys=True) + "\n")
