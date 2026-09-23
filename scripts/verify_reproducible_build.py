#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def snapshot(folder: Path) -> dict[str,str]:
    return {p.name:sha(p) for p in sorted(folder.iterdir()) if p.is_file()}


def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--version")
    ns=ap.parse_args()
    version=(ns.version or (ROOT/"VERSION").read_text()).strip()
    version=version[1:] if version.startswith("v") else version

    with tempfile.TemporaryDirectory() as td:
        first=Path(td)/"first"
        second=Path(td)/"second"
        subprocess.run([sys.executable,str(ROOT/"scripts/build_distributions.py"),"--version",version,"--output-dir",str(first)],check=True,cwd=ROOT)
        subprocess.run([sys.executable,str(ROOT/"scripts/build_distributions.py"),"--version",version,"--output-dir",str(second)],check=True,cwd=ROOT)
        a=snapshot(first); b=snapshot(second)
        if a!=b:
            print("REPRODUCIBILITY: FAIL")
            for name in sorted(set(a)|set(b)):
                if a.get(name)!=b.get(name):
                    print(f"- {name}: {a.get(name)} != {b.get(name)}")
            return 1

    print("REPRODUCIBILITY: PASS")
    return 0


if __name__=="__main__":
    raise SystemExit(main())
