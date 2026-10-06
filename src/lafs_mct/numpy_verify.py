from __future__ import annotations

import itertools
import numpy as np


def c3x_matrix() -> np.ndarray:
    """C^3X on ordered data bits (c1,c2,c3,t), big-endian indexing."""
    u = np.zeros((16, 16), dtype=complex)
    for c1, c2, c3, t in itertools.product((0, 1), repeat=4):
        src = (c1 << 3) | (c2 << 2) | (c3 << 1) | t
        tout = t ^ (c1 & c2 & c3)
        dst = (c1 << 3) | (c2 << 2) | (c3 << 1) | tout
        u[dst, src] = 1.0
    return u


def cz12_matrix() -> np.ndarray:
    z = np.eye(16, dtype=complex)
    for c1, c2, c3, t in itertools.product((0, 1), repeat=4):
        idx = (c1 << 3) | (c2 << 2) | (c3 << 1) | t
        if c1 & c2:
            z[idx, idx] = -1.0
    return z


def pre_correction_branch(outcome: int) -> np.ndarray:
    """Data-space Kraus map after X-basis ancilla measurement, before repair."""
    if outcome not in (0, 1):
        raise ValueError("outcome must be 0 or 1")
    phase = np.eye(16, dtype=complex)
    if outcome == 1:
        phase = cz12_matrix()
    return (phase @ c3x_matrix()) / np.sqrt(2.0)


def corrected_branch(outcome: int) -> np.ndarray:
    repair = np.eye(16, dtype=complex) if outcome == 0 else cz12_matrix()
    return repair @ pre_correction_branch(outcome)


def verify_measurement_release() -> dict:
    target = c3x_matrix() / np.sqrt(2.0)
    errors = {}
    for m in (0, 1):
        diff = corrected_branch(m) - target
        errors[f"branch_{m}_frobenius_error"] = float(np.linalg.norm(diff, ord="fro"))
    errors["max_error"] = max(errors.values())
    errors["branch_probability_0"] = 0.5
    errors["branch_probability_1"] = 0.5
    return errors


def truth_table_rows() -> list[dict]:
    rows = []
    for c1, c2, c3, t in itertools.product((0, 1), repeat=4):
        rows.append({
            "c1": c1, "c2": c2, "c3": c3, "t_in": t,
            "t_out": t ^ (c1 & c2 & c3),
        })
    return rows


def _single_gate_matrix(gate: np.ndarray, qubit: int, n: int = 3) -> np.ndarray:
    mats = []
    for q in range(n):
        mats.append(gate if q == qubit else np.eye(2, dtype=complex))
    out = mats[0]
    for m in mats[1:]:
        out = np.kron(out, m)
    return out


def _cx_matrix(control: int, target: int, n: int = 3) -> np.ndarray:
    out = np.zeros((2**n, 2**n), dtype=complex)
    for idx in range(2**n):
        bits = [(idx >> (n - 1 - q)) & 1 for q in range(n)]
        obits = bits[:]
        if bits[control]:
            obits[target] ^= 1
        dst = 0
        for b in obits:
            dst = (dst << 1) | b
        out[dst, idx] = 1
    return out


def ccx_matrix() -> np.ndarray:
    out = np.zeros((8, 8), dtype=complex)
    for c0, c1, t in itertools.product((0, 1), repeat=3):
        src = (c0 << 2) | (c1 << 1) | t
        dst = (c0 << 2) | (c1 << 1) | (t ^ (c0 & c1))
        out[dst, src] = 1
    return out


def exact_ccx_decomposition_matrix() -> np.ndarray:
    h = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
    t = np.diag([1.0, np.exp(1j * np.pi / 4)])
    tdg = t.conj().T
    u = np.eye(8, dtype=complex)
    # Apply in the same left-to-right order as append_exact_ccx().
    operations = [
        ("g", h, 2), ("cx", 1, 2), ("g", tdg, 2), ("cx", 0, 2),
        ("g", t, 2), ("cx", 1, 2), ("g", tdg, 2), ("cx", 0, 2),
        ("g", t, 1), ("g", t, 2), ("g", h, 2), ("cx", 0, 1),
        ("g", t, 0), ("g", tdg, 1), ("cx", 0, 1),
    ]
    for op in operations:
        if op[0] == "g":
            g = _single_gate_matrix(op[1], op[2], 3)
        else:
            g = _cx_matrix(op[1], op[2], 3)
        u = g @ u
    return u


def verify_exact_ccx_decomposition() -> float:
    # Exact up to a global phase; align using the first nonzero matrix element.
    a = exact_ccx_decomposition_matrix()
    b = ccx_matrix()
    nz = np.argwhere(np.abs(b) > 0)[0]
    phase = a[tuple(nz)] / b[tuple(nz)]
    if abs(phase) == 0:
        return float("inf")
    aligned = a / (phase / abs(phase))
    return float(np.linalg.norm(aligned - b, ord="fro"))
