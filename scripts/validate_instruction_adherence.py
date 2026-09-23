#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
errors: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


manifest_path = ROOT / "tests" / "test-manifest.yaml"
check(manifest_path.is_file(), "Missing tests/test-manifest.yaml")

if manifest_path.is_file():
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    suite = manifest.get("suites", {}).get("instruction_adherence", {})
    check(suite.get("type") == "behavioral", "instruction_adherence suite must be behavioral")
    check(suite.get("blocking") is True, "instruction_adherence suite must be blocking")
    path = ROOT / suite.get("path", "")
    check(path.is_dir(), "instruction_adherence path must exist")

    cases = sorted(path.glob("*.yaml")) if path.is_dir() else []
    check(len(cases) >= 5, "At least five instruction-adherence cases are required")
    ids: set[str] = set()
    for case_path in cases:
        case = yaml.safe_load(case_path.read_text(encoding="utf-8"))
        case_id = case.get("id")
        check(bool(case_id), f"{case_path.name}: missing id")
        check(case_id not in ids, f"{case_path.name}: duplicate id {case_id}")
        if case_id:
            ids.add(case_id)
        check(case.get("criticality") in {"critical", "important", "optional"},
              f"{case_path.name}: invalid criticality")
        check(bool(case.get("input")), f"{case_path.name}: input must be non-empty")
        expected = case.get("expected", {})
        check(bool(expected.get("required")), f"{case_path.name}: expected.required must be non-empty")
        check(float(case.get("scoring", {}).get("pass_threshold", 0)) >= 0.8,
              f"{case_path.name}: pass threshold must be at least 0.8")

if errors:
    print("INSTRUCTION ADHERENCE: FAIL")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print("INSTRUCTION ADHERENCE: PASS")
