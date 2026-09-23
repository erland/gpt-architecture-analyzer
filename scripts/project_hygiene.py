#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path

CACHE_DIRS = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}
TEMP_FILES = {".DS_Store"}
TEMP_SUFFIXES = {".tmp", ".temp"}
HISTORICAL_RE = re.compile(r"(^|[-_.])(old|backup|bak|previous|copy|final-final|v[2-9][0-9]*)([-_.]|$)", re.IGNORECASE)


def run(root: Path, mode: str, fix: bool) -> dict:
    findings = []
    removed = []

    for name in ("build", "dist"):
        p = root / name
        if p.exists():
            if fix:
                shutil.rmtree(p)
                removed.append(name + "/")
            else:
                findings.append({"severity":"warning","code":"HY100","message":"Generated directory exists in source tree","path":name + "/"})

    for p in sorted(root.rglob("*"), key=lambda x: len(x.parts), reverse=True):
        if not p.exists():
            continue
        rel = p.relative_to(root).as_posix()
        if p.is_dir() and p.name in CACHE_DIRS:
            if fix:
                shutil.rmtree(p); removed.append(rel + "/")
            else:
                findings.append({"severity":"warning","code":"HY110","message":"Cache directory found","path":rel})
        elif p.is_file() and (p.name in TEMP_FILES or p.suffix.lower() in TEMP_SUFFIXES):
            if fix:
                p.unlink(); removed.append(rel)
            else:
                findings.append({"severity":"warning","code":"HY111","message":"Temporary file found","path":rel})

    for p in root.rglob("*"):
        if p.is_file():
            rel = p.relative_to(root).as_posix()
            if HISTORICAL_RE.search(p.stem):
                findings.append({"severity":"warning","code":"HY200","message":"Filename suggests historical/superseded copy; manual review required","path":rel})

    if mode == "final":
        for rel in (
            "gpt-project.yaml",
            "project-status.yaml",
            "docs/development-plan.md",
            "runtime-parity.yaml",
            "canonical/instructions.md",
        ):
            if not (root / rel).exists():
                findings.append({"severity":"blocked","code":"HY300","message":"Required canonical project file missing","path":rel})

    result = "blocked" if any(x["severity"]=="blocked" for x in findings) else ("warning" if findings else "pass")
    return {"result":result,"mode":mode,"removed":sorted(set(removed)),"findings":findings}


def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--project-root",default=".")
    ap.add_argument("--mode",choices=["checkpoint","final"],default="checkpoint")
    ap.add_argument("--fix",action="store_true")
    ap.add_argument("--json",action="store_true")
    ns=ap.parse_args()
    report=run(Path(ns.project_root).resolve(),ns.mode,ns.fix)
    if ns.json:
        print(json.dumps(report,ensure_ascii=False,indent=2))
    else:
        for item in report["removed"]: print("REMOVED",item)
        for item in report["findings"]: print(item["severity"].upper(),item["code"],item["message"],f"[{item.get('path','')}]")
        print("Hygiene result:",report["result"].upper())
    return 1 if report["result"]=="blocked" else 0


if __name__=="__main__":
    raise SystemExit(main())
