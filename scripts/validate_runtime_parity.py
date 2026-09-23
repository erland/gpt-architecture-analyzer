#!/usr/bin/env python3
from __future__ import annotations

import json
import zipfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    "chatgpt_chat",
    "chatgpt_custom",
    "claude_project",
    "opencode",
    "openai_plugin",
}
ACTIVE = {"chatgpt_chat", "chatgpt_custom", "claude_project", "opencode"}
INACTIVE = {"openai_plugin"}
CATEGORIES = {"behavior", "capability", "artifact", "workspace_state", "tool"}
errors: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


cfg = yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))
model = yaml.safe_load((ROOT / "runtime-parity.yaml").read_text(encoding="utf-8"))

check(set(model.get("registered_runtimes", [])) == EXPECTED, "runtime-parity.yaml must register all five runtimes")
check(set(model.get("compared_categories", [])) == CATEGORIES, "runtime parity categories differ")
check(set(cfg.get("runtime_parity", {}).get("registered_runtimes", [])) == EXPECTED, "gpt-project runtime parity registration differs")
check(set(cfg.get("runtime_parity", {}).get("compared_categories", [])) == CATEGORIES, "gpt-project parity categories differ")

candidates = {
    item["runtime_id"]: item
    for item in cfg.get("analysis", {}).get("runtime", {}).get("candidates", [])
}
check(set(candidates) == EXPECTED, "all five runtime candidates must be assessed")

for runtime_id in ACTIVE:
    check(candidates[runtime_id].get("suitability") == "ready", f"{runtime_id} must be ready")
    check(candidates[runtime_id].get("activate_by_default") is True, f"{runtime_id} must activate by default")
    check(model.get("runtimes", {}).get(runtime_id, {}).get("active") is True, f"{runtime_id} must be active in parity model")

for runtime_id in INACTIVE:
    check(candidates[runtime_id].get("suitability") == "reduced", f"{runtime_id} must be reduced")
    check(candidates[runtime_id].get("activate_by_default") is False, f"{runtime_id} must stay inactive")
    check(model.get("runtimes", {}).get(runtime_id, {}).get("active") is False, f"{runtime_id} must be inactive in parity model")

version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
specs = {
    "chatgpt_chat": (f"architecture-analyzer-chat-v{version}.zip", "assistant/runtime-contract.json", "assistant/instructions.txt"),
    "chatgpt_custom": (f"architecture-analyzer-custom-gpt-v{version}.zip", "runtime-contract.json", "gpt-instructions.txt"),
    "claude_project": (f"architecture-analyzer-claude-v{version}.zip", "project/runtime-contract.json", "project/instructions.md"),
    "opencode": (f"architecture-analyzer-opencode-v{version}.zip", ".opencode/architecture-analyzer/runtime-contract.json", ".opencode/architecture-analyzer/instructions.md"),
}
canonical = (ROOT / "canonical/instructions.md").read_bytes()

for runtime_id, (name, contract_path, instruction_path) in specs.items():
    path = ROOT / "dist" / name
    check(path.is_file(), f"missing built distribution: {name}")
    if not path.is_file():
        continue
    with zipfile.ZipFile(path) as z:
        names = set(z.namelist())
        check(contract_path in names, f"{runtime_id} missing runtime contract")
        check(instruction_path in names, f"{runtime_id} missing canonical instruction")
        if contract_path in names:
            contract = json.loads(z.read(contract_path))
            check(contract.get("runtime_id") == runtime_id, f"{runtime_id} runtime_id differs")
            for key in ("capabilities", "artifacts", "workspace_state", "tools"):
                check(contract.get(key) == cfg.get(key), f"{runtime_id} {key} contract drift")
        if instruction_path in names:
            check(z.read(instruction_path) == canonical, f"{runtime_id} canonical instruction drift")

report = {
    "result": "PASS" if not errors else "FAIL",
    "active": sorted(ACTIVE),
    "inactive": sorted(INACTIVE),
    "errors": errors,
}
print(json.dumps(report, ensure_ascii=False, indent=2))
raise SystemExit(1 if errors else 0)
