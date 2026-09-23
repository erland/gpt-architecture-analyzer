#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
errors: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


cfg_path = ROOT / "gpt-project.yaml"
check(cfg_path.is_file(), "Missing gpt-project.yaml")
if cfg_path.is_file():
    cfg = yaml.safe_load(cfg_path.read_text(encoding="utf-8"))

    check(cfg.get("project", {}).get("profile") == "zip_first_advanced",
          "Project profile must be zip_first_advanced")
    robust = cfg.get("model_robustness", {})
    check(robust.get("level") == "guided", "Model robustness must be guided")
    check(robust.get("explicit_workflow") is True, "Guided workflow must be explicit")
    check(robust.get("instruction_adherence_evals") is True,
          "Instruction-adherence evals must be planned/enabled")

    expected_runtimes = {
        "chatgpt_chat",
        "chatgpt_custom",
        "claude_project",
        "opencode",
        "openai_plugin",
    }
    candidates = {
        item.get("runtime_id"): item
        for item in cfg.get("analysis", {}).get("runtime", {}).get("candidates", [])
        if isinstance(item, dict)
    }
    check(set(candidates) == expected_runtimes, "All five peer runtimes must be assessed")
    for runtime_id in ("chatgpt_chat", "chatgpt_custom", "claude_project", "opencode"):
        check(candidates.get(runtime_id, {}).get("suitability") == "ready",
              f"{runtime_id} must be assessed ready")
    check(candidates.get("openai_plugin", {}).get("suitability") == "reduced",
          "openai_plugin must be explicitly reduced")

    for key in ("capabilities", "artifacts", "workspace_state", "tools"):
        check(isinstance(cfg.get(key), dict), f"Missing platform-neutral contract: {key}")

canonical = ROOT / "canonical" / "instructions.md"
legacy = ROOT / "gpt-instructions.txt"
check(canonical.is_file(), "Missing canonical/instructions.md")
check(legacy.is_file(), "Missing gpt-instructions.txt")
if canonical.is_file() and legacy.is_file():
    check(canonical.read_bytes() == legacy.read_bytes(),
          "Step 1 must preserve the legacy instruction byte-for-byte in canonical/instructions.md")

knowledge = sorted(p for p in (ROOT / "knowledge").glob("*") if p.is_file())
check(len(knowledge) == 10, f"Expected 10 Knowledge files, found {len(knowledge)}")

for rel in (
    "schemas/capability-contract.schema.json",
    "schemas/artifact-contract.schema.json",
    "schemas/workspace-state-contract.schema.json",
    "schemas/tool-contract.schema.json",
    "PROJECT.md",
    "STATUS.md",
    "project-status.yaml",
    "docs/development-plan.md",
):
    check((ROOT / rel).is_file(), f"Missing required migration file: {rel}")

if errors:
    print("GPT PROJECT LINT: FAIL")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print("GPT PROJECT LINT: PASS")
