# churnlab

A reproducible churn prediction project (ESILV MLOps). A telecommunications
company wants to identify customers who are likely to leave its service.
The target column is `Churn` (`Yes`/`No`); the model inputs are everything
else (tenure, contract type, charges, services subscribed, etc.) except the
customer identifier.

## Environment setup

Requires Python 3.11 or 3.12 and [uv](https://docs.astral.sh/uv/).

```sh
uv sync --locked
uv run python -c "import churnlab; print(churnlab.__version__)"
```

## Dataset

The project uses the IBM Telco Customer Churn CSV, pinned to a specific
commit of IBM's example repository:

- Source: https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/1fd6fd70906479be1712e64cfc0ea89f58466629/data/Telco-Customer-Churn.csv
- Expected SHA-256: `16320c9c1ec72448db59aa0a26a0b95401046bef5d02fd3aeb906448e3055e91`

Fetch the snapshot and verify it:

```sh
uv run python scripts/download_data.py
uv run python scripts/inspect_telco.py
```

The inspection script re-checks the hash and writes a small overview report
to `reports/tp01_data_overview.json`.

## Project layout

- `src/churnlab/` — importable data, training and serving code for the churn model.
- `scripts/` — executable commands for the workflow (download data, inspect data, record environment).
- `data/raw/` — the original input snapshot and its source/hash metadata (`telco.csv` itself is not committed; re-download it with `scripts/download_data.py`).
- `evidence/` — small, non-sensitive artifacts produced for TP submissions.

## About this dataset

This is a single **customer snapshot**: one row per customer, as of one
point in time. It is not a dated customer event log, and it is not the
result of a randomized retention experiment. Do not treat it as having a
time axis or a treatment/control assignment — any such structure would
have to be invented, not observed, from this data.
