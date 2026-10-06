from __future__ import annotations


def _qiskit():
    from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
    return QuantumCircuit, QuantumRegister, ClassicalRegister


def append_exact_ccx(qc, c0, c1, target):
    """Append a standard exact 7-T, 6-CX, 2-H CCX decomposition."""
    qc.h(target)
    qc.cx(c1, target)
    qc.tdg(target)
    qc.cx(c0, target)
    qc.t(target)
    qc.cx(c1, target)
    qc.tdg(target)
    qc.cx(c0, target)
    qc.t(c1)
    qc.t(target)
    qc.h(target)
    qc.cx(c0, c1)
    qc.t(c0)
    qc.tdg(c1)
    qc.cx(c0, c1)


def coherent_c3x_reference(measure_output: bool = True):
    QuantumCircuit, QuantumRegister, ClassicalRegister = _qiskit()
    q = QuantumRegister(5, "q")  # c1,c2,c3,a,t
    out = ClassicalRegister(1, "out")
    qc = QuantumCircuit(q, out, name="c3x_coherent")
    c1, c2, c3, a, t = q
    append_exact_ccx(qc, c1, c2, a)
    append_exact_ccx(qc, a, c3, t)
    append_exact_ccx(qc, c1, c2, a)
    if measure_output:
        qc.measure(t, out[0])
    return qc


def dynamic_c3x_reference(measure_output: bool = True, reset_ancilla: bool = True):
    QuantumCircuit, QuantumRegister, ClassicalRegister = _qiskit()
    q = QuantumRegister(5, "q")
    m = ClassicalRegister(1, "release")
    out = ClassicalRegister(1, "out")
    qc = QuantumCircuit(q, m, out, name="c3x_dynamic")
    c1, c2, c3, a, t = q
    append_exact_ccx(qc, c1, c2, a)
    append_exact_ccx(qc, a, c3, t)
    qc.h(a)
    qc.measure(a, m[0])
    with qc.if_test((m, 1)):
        qc.cz(c1, c2)
    if reset_ancilla:
        qc.reset(a)
    if measure_output:
        qc.measure(t, out[0])
    return qc


def prepare_basis_case(qc, c1: int, c2: int, c3: int, t: int):
    bits = (c1, c2, c3, t)
    qmap = (0, 1, 2, 4)
    for bit, qidx in zip(bits, qmap):
        if bit:
            qc.x(qidx)
    return qc
