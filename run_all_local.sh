#!/usr/bin/env bash
set -euo pipefail
python scripts/01_reproduce_analytical.py
python scripts/02_verify_measurement_release.py
python scripts/03_plot_break_even.py
pytest -q
