import hashlib
import json
import urllib.request
from pathlib import Path

SOURCE_URL = (
    "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/"
    "1fd6fd70906479be1712e64cfc0ea89f58466629/data/Telco-Customer-Churn.csv"
)
EXPECTED_SHA256 = (
    "16320c9c1ec72448db59aa0a26a0b95401046bef5d02fd3aeb906448e3055e91"
)

target = Path("data/raw/telco.csv")
source_meta = Path("data/raw/telco.source.json")

if not target.exists():
    target.parent.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(SOURCE_URL, target)

actual_sha256 = hashlib.sha256(target.read_bytes()).hexdigest()
if actual_sha256 != EXPECTED_SHA256:
    raise ValueError(
        f"Source hash mismatch: expected {EXPECTED_SHA256}, got {actual_sha256}"
    )

source_meta.write_text(
    json.dumps({"source_url": SOURCE_URL, "sha256": actual_sha256}, indent=2),
    encoding="utf-8",
)
print(f"OK: {target} matches expected sha256 {actual_sha256}")
