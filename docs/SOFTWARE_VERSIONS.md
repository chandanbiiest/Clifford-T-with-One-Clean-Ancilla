# Recommended software versions

The local analytical scripts require only the core requirements file.

For IBM Quantum experiments, the repository targets the current documented
Qiskit dynamic-circuit interface with:

- `qiskit~=2.5.2`
- `qiskit-ibm-runtime~=0.47.0`
- `qiskit-aer==0.17.2`

For Azure Quantum and Microsoft Quantum resource estimation, install the current
QDK package with the `azure`, `qiskit`, and `qre` extras. Record the exact
resolved package versions in the release notes when experiments are run.
