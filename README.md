# churnlab

A reproducible churn prediction project (ESILV MLOps). The goal: a telecom
company wants to know which customers are likely to leave, so it can act
before they do. The target column is `Churn` (`Yes`/`No`). Everything else
in the dataset (tenure, contract type, charges, services subscribed, etc.)
is a potential model input, except the customer ID, which just identifies
the row.

## Environment setup

Requires Python 3.11 or 3.12 and [uv](https://docs.astral.sh/uv/).

```sh
uv sync --locked
uv run python -c "import churnlab; print(churnlab.__version__)"
```

## Dataset

We use the IBM Telco Customer Churn CSV, pinned to a specific commit of
IBM's example repository so everyone works from the exact same bytes:

- Source: https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/1fd6fd70906479be1712e64cfc0ea89f58466629/data/Telco-Customer-Churn.csv
- Expected SHA-256: `16320c9c1ec72448db59aa0a26a0b95401046bef5d02fd3aeb906448e3055e91`

To fetch the snapshot and check it against that hash:

```sh
uv run python scripts/download_data.py
uv run python scripts/inspect_telco.py
```

`inspect_telco.py` recomputes the hash, fails loudly if it doesn't match,
and writes a small overview report to `reports/tp01_data_overview.json`.

## Project layout

- `src/churnlab/`: the importable package, data/training/serving code lives here.
- `scripts/`: the runnable commands for the workflow, downloading data, inspecting it, recording the environment.
- `data/raw/`: the original snapshot plus its source and hash metadata. The CSV itself isn't committed; run `scripts/download_data.py` to get it back.
- `evidence/`: small, non-sensitive files produced for TP submissions.

## About this dataset

This is a single customer snapshot, one row per customer, at one point in
time. It's not a dated event log, and it's not the output of a randomized
retention experiment. So don't read a time axis or a treatment/control
split into it. If you want that kind of structure, you'd have to build it
yourself, it isn't in the data.
