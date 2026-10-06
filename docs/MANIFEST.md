# Manifest

## Local deterministic reproduction
- `scripts/01_reproduce_analytical.py`: paper resource table -> latency and reliability thresholds.
- `scripts/02_verify_measurement_release.py`: exact matrix verification of the dynamic release identity.
- `scripts/03_plot_break_even.py`: regenerates the analytical crossover plot.
- `tests/`: regression tests for key reported values and branch-map correctness.

## IBM Quantum
- `scripts/10_ibm_capture_backend.py`: saves connectivity, operation durations/errors, and qubit properties.
- `scripts/11_ibm_transpile_metrics.py`: maps coherent/dynamic C3X references to one backend Target.
- `scripts/12_ibm_noisy_basis_sweep.py`: exhaustive 16-case computational-basis sweep using a backend-derived Aer model.
- `scripts/13_ibm_hardware_run.py`: physical submission entry point; writes output only after completed jobs.

## Azure Quantum
- `scripts/20_azure_list_targets.py`: enumerates targets available in the configured workspace.
- `scripts/21_azure_submit_openqasm.py`: submits an explicit OpenQASM program to a selected target.

## Fault-tolerant projection
- `scripts/30_resource_estimator_example.py`: records the resource-estimation architecture and error-correction settings and shows the current estimator call pattern.

## Data
- `data/source/`: immutable analytical values used by the manuscript.
- `data/generated/`: locally regenerated values and plots.
- `data/templates/`: schemas for cloud measurements; no placeholder measurement is presented as an observed result.
