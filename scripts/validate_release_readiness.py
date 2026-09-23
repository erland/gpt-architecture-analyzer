#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
errors: list[str] = []


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


parity = subprocess.run([sys.executable, str(ROOT / "scripts" / "validate_runtime_parity.py")], cwd=ROOT)
if parity.returncode != 0:
    errors.append("runtime parity failed")

delivery_path = ROOT / "dist" / "DELIVERY-MANIFEST.json"
sums_path = ROOT / "dist" / "SHA256SUMS.txt"

if not delivery_path.is_file():
    errors.append("DELIVERY-MANIFEST.json missing")
else:
    delivery = json.loads(delivery_path.read_text(encoding="utf-8"))
    required_types = {"project_zip", "chat_zip", "custom_gpt_zip", "claude_zip", "opencode_zip"}
    types = {item.get("type") for item in delivery.get("artifacts", [])}
    if types != required_types:
        errors.append(f"delivery artifact types differ: {sorted(types)}")

checksums: dict[str, str] = {}
if not sums_path.is_file():
    errors.append("SHA256SUMS.txt missing")
else:
    for line in sums_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        digest, name = line.split(None, 1)
        checksums[name.strip()] = digest

version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
expected = [
    f"architecture-analyzer-project-v{version}.zip",
    f"architecture-analyzer-chat-v{version}.zip",
    f"architecture-analyzer-custom-gpt-v{version}.zip",
    f"architecture-analyzer-claude-v{version}.zip",
    f"architecture-analyzer-opencode-v{version}.zip",
]
for name in expected:
    path = ROOT / "dist" / name
    if not path.is_file():
        errors.append(f"missing release artifact: {name}")
        continue
    if checksums.get(name) != sha256(path):
        errors.append(f"checksum mismatch: {name}")
    try:
        with zipfile.ZipFile(path) as z:
            bad = z.testzip()
            if bad:
                errors.append(f"zip CRC failure in {name}: {bad}")
    except zipfile.BadZipFile:
        errors.append(f"invalid zip: {name}")

print(json.dumps({
    "result": "PASS" if not errors else "FAIL",
    "errors": errors,
}, ensure_ascii=False, indent=2))
raise SystemExit(1 if errors else 0)
