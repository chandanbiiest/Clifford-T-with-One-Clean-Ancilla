# LAFS-MCT reproducibility package

This repository accompanies the manuscript **“Latency- and Fidelity-Aware
Static–Dynamic Clifford+T Synthesis of Multi-Controlled Toffoli Gates with One
Clean Ancilla.”** It is organized so that analytical claims can be reproduced
locally and cloud experiments can be run without mixing measured data with
analytical proxies.

## What is included

- fixed analytical resource tuples used by the paper;
- exact reproduction of the normalized latency crossover values;
- exact product-form and first-order reliability crossover calculation;
- an independent matrix-level verification of the one-clean-ancilla C3X
  measurement-release identity;
- Qiskit builders for coherent and measurement-release C3X reference circuits;
- IBM Quantum backend-snapshot, transpilation, backend-derived simulation, and
  physical-run scripts;
- Azure Quantum target listing and submission examples;
- a current Microsoft Quantum resource-estimation configuration example;
- empty hardware-result templates so that no unexecuted experiment is represented
  as measured data.

## Quick start: local reproducibility

```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
pip install -r requirements-core.txt
python scripts/01_reproduce_analytical.py
python scripts/02_verify_measurement_release.py
python scripts/03_plot_break_even.py
pytest -q
```

Expected key values are:

- `n=16`, static versus mixed normalized latency threshold: `48.4`;
- exact isolated measurement-error crossover for epsilon_T=1e-4 and
  epsilon_CX=1e-3: about `0.002398140524` (`0.239814%`);
- corrected branch-map Frobenius error for both measurement outcomes: numerical
  zero to floating-point precision.

## IBM Quantum experiments

Install:

```bash
pip install -r requirements-ibm.txt
```

Then use the standard Qiskit Runtime credential store and run, for example:

```bash
python scripts/10_ibm_capture_backend.py --backend BACKEND_NAME
python scripts/11_ibm_transpile_metrics.py --backend BACKEND_NAME
python scripts/12_ibm_noisy_basis_sweep.py --backend BACKEND_NAME --shots 4096
python scripts/13_ibm_hardware_run.py --backend BACKEND_NAME --family both --shots 4096
```

The current IBM dynamic-circuit workflow uses mid-circuit measurement and
classical feedforward. For dynamic candidates, measured scheduler timing should
be preferred over a simple static-circuit duration estimator.

## Azure Quantum experiments

Install:

```bash
pip install -r requirements-azure.txt
```

Set the workspace connection string only in your local environment, never in the
repository:

```bash
export AZURE_QUANTUM_CONNECTION_STRING='...'
python scripts/20_azure_list_targets.py
python scripts/21_azure_submit_openqasm.py --target TARGET_NAME --qasm circuit.qasm
```

Provider availability and accepted circuit formats are workspace dependent.

## Resource estimation

Run:

```bash
python scripts/30_resource_estimator_example.py
```

This writes the architecture/error-correction settings used as the starting
point for fault-tolerant projection. A physical-resource table should only be
reported after the selected logical candidate has been translated into the
resource estimator's application model and the estimation has actually run.

## Reproducibility policy

Analytical values, simulator results, and physical-hardware results are kept in
separate files. Hardware files are initially templates and must remain empty
until the corresponding jobs complete. Every reported physical run should retain
its job ID, backend identifier, calibration snapshot, shot count, compiler
configuration, and seed policy.

## Repository structure

```text
configs/          model and example backend parameters
data/source/      fixed source values used by the analytical study
data/generated/   outputs created by scripts
data/templates/   empty schemas for future measured results
docs/             experiment protocol and data dictionary
scripts/          reproducibility and cloud experiment entry points
src/lafs_mct/     reusable implementation
tests/           local regression tests
```

## Suggested archival practice

Use GitHub for version control and issue tracking, then archive the exact
submission release in a DOI-minting repository. Cite the immutable release in
the final manuscript so that later code changes do not alter the submitted
artifact.

## Continuous checks and circuit exchange files

A small GitHub Actions workflow in `.github/workflows/ci.yml` reruns the local
analytical and matrix-level tests on every push or pull request. Structural
OpenQASM references are provided under `circuits/qasm/`; target-specific
compilation remains the responsibility of the selected provider backend.
