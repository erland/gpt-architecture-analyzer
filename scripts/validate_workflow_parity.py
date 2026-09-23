#!/usr/bin/env python3
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
wf=(ROOT/".github/workflows/build-distributions.yml").read_text(encoding="utf-8")
errors=[]

required=[
    "scripts/lint_gpt_project.py",
    "python3 -m pytest -q -p no:cacheprovider",
    "scripts/validate_instruction_adherence.py",
    "scripts/build_distributions.py",
    "scripts/validate_distributions.py",
    "scripts/validate_runtime_parity.py",
    "scripts/validate_release_readiness.py",
    "scripts/project_hygiene.py --project-root . --mode final",
    "scripts/verify_reproducible_build.py",
]
for marker in required:
    if marker not in wf:
        errors.append(f"workflow missing: {marker}")

for artifact in (
    "architecture-analyzer-project-v${VERSION}.zip",
    "architecture-analyzer-chat-v${VERSION}.zip",
    "architecture-analyzer-custom-gpt-v${VERSION}.zip",
    "architecture-analyzer-claude-v${VERSION}.zip",
    "architecture-analyzer-opencode-v${VERSION}.zip",
    "SHA256SUMS.txt",
    "DELIVERY-MANIFEST.json",
):
    if artifact not in wf:
        errors.append(f"release upload missing: {artifact}")

if "github.event.release.tag_name" not in wf:
    errors.append("release tag must remain authoritative version source")

if errors:
    print("WORKFLOW PARITY: FAIL")
    for e in errors: print("-",e)
    raise SystemExit(1)
print("WORKFLOW PARITY: PASS")
