# Data dictionary

## `data/source/paper_resource_counts.csv`
The analytical source table used by the manuscript. `N_CX` is logical CX count,
`N_T` is T/T-dagger count, and `D_T` is T depth. `family` is one of `Static_S`,
`Dynamic_D2`, or `Mixed_D23`.

## Generated analytical files
- `latency_break_even_thresholds.csv`: normalized crossover threshold for each
  dynamic family relative to the static family.
- `reliability_break_even.csv`: exact and first-order measurement-error
  thresholds for the isolated cleanup comparison.
- `c3x_truth_table.csv`: exhaustive 16-case truth table of the four data qubits.
- `measurement_release_verification.json`: branch-map matrix verification.

## Hardware records
Hardware outputs are deliberately absent until a cloud job is run. The template
`data/templates/hardware_results_template.csv` lists the fields that should be
recorded for each run. Preserve raw job IDs and backend snapshots with every
reported result.
