# Experiment protocol

1. Run the local analytical reproduction and exact branch-map verification.
2. Capture a backend snapshot immediately before compilation.
3. Compile coherent and dynamic candidates with the same optimization level and
   seed policy.
4. Run a backend-derived noisy simulation before using physical hardware.
5. For physical runs, keep shot count, backend, calibration time, and compiler
   settings identical across paired candidates.
6. Report unmitigated values first. Any mitigation must be reported separately.
7. Preserve each cloud job ID and the corresponding backend snapshot.
8. Repeat across multiple calibration snapshots if making calibration-sensitivity
   claims.
9. Keep logical metrics and backend-native metrics in separate columns.
10. Do not populate hardware-result tables from analytical proxies.
