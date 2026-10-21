# TP01 - Answers and Evidence

## Part A - Understand the project and data

**A1. Why should the original CSV, a fitted model and the training source code have different roles in the repository?**

The raw CSV is the original input that must stay unchanged, the source code is the recipe we version in Git, and the trained model is just an output generated from both. Keeping them separate lets us know exactly which data and code produced a given model, so it can be reproduced.

**A2. Why would including `Churn` among the model inputs invalidate the prediction task?**

Because it's what we are trying to predict.

## Part B - Create and inspect the Python environment

**B2 Tasks:**

 1.requires-python = ">=3.11,<3.13"
dependencies = [
    "pandas",
    "numpy~=1.26.0",
    "scikit-learn",
]
2.name = "numpy"
version = "1.26.4"
source = { registry = "https://pypi.org/simple" }
3.One transitive dependency : scipy v1.17.1.
4. pyproject.toml states what you need, as ranges. uv.lock pins exact resolved versions with hashes, so everyone gets the same result. .venv/ is just the installed environment built from the lock file — disposable, never committed to Git.

## Part C - Inspect and fingerprint the Telco dataset

**C3. Interpret the result:**

1. Why is churn prediction a classification task?
2. What does the class balance suggest about using accuracy alone later?
3. Why can `TotalCharges` be read as an object/string column even though it represents a numeric quantity?
4. Why may `isna()` alone fail to detect a whitespace-only value?
5. Which evidence would tell a teammate that they inspected the same source file?

1.The target Churn has two values so the model predicts a category
2. About 73% of customers don't churn. So if your model just says "No" every single time, it's already right 73% of the time, without learning a thing.
3. A chunk of rows have blank spaces instead of real numbers in TotalCharges, so pandas can't treat the whole column as numeric and just falls back to reading it as text.
4.Because a space " " isn't technically missing so it's a string, just an empty-looking one. isna() only catches actual nulls, so it'll walk right past these.
5. If you and a teammate get the same SHA-256 hash, you're looking at byte-for-byte the same file. Same filename doesn't guarantee that, same hash does.

## Part D - Prove environment recreation

### D1. Before/after comparison

| Metric | Before | After | Match? |
|---|---|---|---|
| Python | 3.12.0 | 3.12.0 | Yes |
| churnlab | 0.1.0 | 0.1.0 | Yes |
| pandas | 3.0.6 | 3.0.6 | Yes |
| numpy | 1.26.4 | 1.26.4 | Yes |
| scikit-learn | 1.9.1 | 1.9.1 | Yes |

Identical package versions on both sides — this is what `pyproject.toml` + `uv.lock` guarantee: a fresh `.venv` resolves to the exact same selections.

Dataset hash (`data/raw/telco.source.json`) and inspection output (`reports/tp01_data_overview.json`) also matched the expected snapshot: 7,043 rows, 21 columns, Churn No=5,174 / Yes=1,869 (~26.54%), 0 duplicate customer IDs, 11 blank `TotalCharges` values.

The backup `.venv-backup/` was removed after verification.

### D2. What has been reproduced

| Item | Evidence produced in TP01 | Remaining limitation |
|---|---|---|
| Code | Git commit (see commit hash below) | Uncommitted edits are not identified by that commit |
| Package selections | `pyproject.toml`, `uv.lock` — recreated environment matches exactly: Python 3.12.0, churnlab 0.1.0, pandas 3.0.6, numpy 1.26.4, scikit-learn 1.9.1 (see `environment-before.json` vs `environment.json`) | Platform/interpreter selection can affect installations (we hit an x86_64/arm64 architecture mismatch during setup, unrelated to the lock file itself) |
| Installed environment | `evidence/tp01/environment-before.json` and `evidence/tp01/environment.json`, identical after `.venv` recreation | Does not capture every OS or hardware detail (e.g. the platform string still read `x86_64-i386-64bit` on this machine even after the environment was fixed, since it only reads package metadata, not actual imports) |
| Source data | Source URL and SHA-256 in `data/raw/telco.source.json`; hash `16320c9c1ec72448db59aa0a26a0b95401046bef5d02fd3aeb906448e3055e91` confirmed by `scripts/inspect_telco.py`, matching the expected inspection output (7,043 rows, 21 columns, Churn No=5,174/Yes=1,869, 0 duplicate IDs, 11 blank `TotalCharges`) in `reports/tp01_data_overview.json` | Does not establish label quality or absence of leakage |
| Trained model | Not produced in TP01 | Requires later training/configuration/artifact evidence |

## Part E - Collaborate through Git and a pull request

- PR URL: <https://github.com/ChrisaMendoza/churnlab-2026/pull/1>
- Merge commit hash: `2f1f282`
- Reviewer question: "Comment je vérifie que j'ai le même CSV ?" — answered with the SHA-256 verification steps already documented in the README (`scripts/download_data.py` + `scripts/inspect_telco.py`, expected hash `16320c9c1ec72448db59aa0a26a0b95401046bef5d02fd3aeb906448e3055e91`). No code change was needed; the README already covered it.

## Part F - Recovery exercise

- Difference between F1 and F2: TODO (fill in after performing the exercise — in short, `git restore <file>` discards unstaged edits from the working file; `git restore --staged <file>` only unstages, the working-file edit is kept)

## Remaining reproducibility limitations

- Only package selection and source data identity are verified here; no model has been trained yet.
- Hardware/platform differences (e.g. arm64 vs x86_64) are not captured by the lock file and can still break an environment even when `uv sync --locked` succeeds.
- The hash check confirms identical bytes, not that the data is free of labeling errors or leakage.
