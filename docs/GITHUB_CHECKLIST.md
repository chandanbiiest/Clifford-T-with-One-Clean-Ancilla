# Repository release checklist

- Commit source code, fixed analytical source data, configuration files, and tests.
- Do not commit cloud credentials, connection strings, or access tokens.
- Tag the exact release used for manuscript submission (for example `v1.0.0`).
- Create an archival release with a persistent DOI using a repository service such
  as Zenodo, or deposit the dataset/code in a suitable archival platform.
- Put the persistent DOI in the manuscript when available.
- Preserve cloud job IDs and backend calibration snapshots for hardware claims.
- Record Python and package versions in the release notes.
