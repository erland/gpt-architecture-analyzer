#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION_FILE = ROOT / "VERSION"
LEGACY_INSTRUCTIONS = ROOT / "gpt-instructions.txt"
CANONICAL_INSTRUCTIONS = ROOT / "canonical" / "instructions.md"
CONFIG_MD = ROOT / "gpt-configuration.md"
CONFIG_JSON = ROOT / "gpt-config.json"
SETUP = ROOT / "docs" / "setup-steps.md"
START_HERE = ROOT / "portable" / "START-HERE.md"
PROJECT_CONFIG = ROOT / "gpt-project.yaml"
KNOWLEDGE = [
    "knowledge/architecture-analysis-method.md",
    "knowledge/architecture-model-schema.md",
    "knowledge/clutter-control-and-grouping-rules.md",
    "knowledge/diagram-style-guide.md",
    "knowledge/evidence-and-confidence-rules.md",
    "knowledge/example-prompts.md",
    "knowledge/output-templates.md",
    "knowledge/quadrant-scoring-rubric.md",
    "knowledge/repository-inspection-checklist.md",
    "knowledge/view-catalog.md",
]
SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")
FIXED_TIME = (2020, 1, 1, 0, 0, 0)

def parse_args():
    p = argparse.ArgumentParser(); p.add_argument("--version"); p.add_argument("--output-dir", default=str(ROOT / "dist")); return p.parse_args()

def resolve_version(v):
    x = (v or VERSION_FILE.read_text(encoding="utf-8")).strip(); x = x[1:] if x.startswith("v") else x
    if not SEMVER.fullmatch(x): raise SystemExit(f"Ogiltig version: {x!r}")
    return x

def starters_text():
    lines = CONFIG_MD.read_text(encoding="utf-8").splitlines()
    try: i = lines.index("## Suggested conversation starters") + 1
    except ValueError: raise SystemExit("Saknar Suggested conversation starters i gpt-configuration.md")
    out = []
    for line in lines[i:]:
        if line.startswith("## "): break
        if line.startswith("- "): out.append(line[2:])
    if not out: raise SystemExit("Inga conversation starters hittades")
    return "# Suggested conversation starters\n\n" + "\n".join(f"- {x}" for x in out) + "\n"

def verify_sources():
    for p in [LEGACY_INSTRUCTIONS, CANONICAL_INSTRUCTIONS, CONFIG_MD, CONFIG_JSON, SETUP, START_HERE, PROJECT_CONFIG]:
        if not p.is_file(): raise SystemExit(f"Saknar {p.relative_to(ROOT)}")
    if LEGACY_INSTRUCTIONS.read_bytes() != CANONICAL_INSTRUCTIONS.read_bytes(): raise SystemExit("Canonical instruction differs from legacy instruction during migration")
    actual = sorted(str(p.relative_to(ROOT)).replace("\\\\", "/") for p in (ROOT / "knowledge").glob("*") if p.is_file())
    if actual != sorted(KNOWLEDGE): raise SystemExit("Knowledge-filuppsättningen avviker")
    cfg = json.loads(CONFIG_JSON.read_text(encoding="utf-8"))
    if sorted(cfg.get("knowledge_files", [])) != sorted(KNOWLEDGE): raise SystemExit("gpt-config.json knowledge_files avviker från faktisk Knowledge")

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def zipdir(src, dst):
    dst.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(dst, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for p in sorted(x for x in src.rglob("*") if x.is_file()):
            info = zipfile.ZipInfo(p.relative_to(src).as_posix(), FIXED_TIME); info.compress_type = zipfile.ZIP_DEFLATED; info.external_attr = 0o100644 << 16
            z.writestr(info, p.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)

def copy_knowledge(target):
    target.mkdir(parents=True, exist_ok=True)
    for rel in KNOWLEDGE: shutil.copy2(ROOT / rel, target / Path(rel).name)

def write_manifest(base, runtime_id, version, entrypoint):
    files = {}
    for p in sorted(x for x in base.rglob("*") if x.is_file() and x.name != "MANIFEST.json"):
        files[p.relative_to(base).as_posix()] = {"sha256": sha(p), "bytes": p.stat().st_size}
    payload = {"schema_version": 1, "runtime_id": runtime_id, "version": version, "entrypoint": entrypoint, "files": files}
    (base / "MANIFEST.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def platform_contract(runtime_id, version, adapter):
    import yaml
    cfg = yaml.safe_load(PROJECT_CONFIG.read_text(encoding="utf-8"))
    return {"schema_version": 1, "runtime_id": runtime_id, "version": version, "capabilities": cfg["capabilities"], "artifacts": cfg["artifacts"], "workspace_state": cfg["workspace_state"], "tools": cfg["tools"], "adapter": adapter}

def build_custom(base, version):
    for rel in ["gpt-instructions.txt", "gpt-configuration.md", "gpt-config.json", "docs/setup-steps.md", *KNOWLEDGE]:
        dst = base / rel; dst.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(ROOT / rel, dst)
    (base / "VERSION").write_text(version + "\n", encoding="utf-8")

def build_portable(base, version):
    shutil.copy2(START_HERE, base / "START-HERE.md"); (base / "assistant").mkdir(parents=True, exist_ok=True)
    shutil.copy2(LEGACY_INSTRUCTIONS, base / "assistant" / "instructions.txt")
    (base / "assistant" / "conversation-starters.md").write_text(starters_text(), encoding="utf-8")
    copy_knowledge(base / "knowledge"); (base / "VERSION").write_text(version + "\n", encoding="utf-8")
    write_manifest(base, "chatgpt_chat", version, "START-HERE.md")

def build_claude(base, version):
    project = base / "project"; project.mkdir(parents=True, exist_ok=True)
    shutil.copy2(CANONICAL_INSTRUCTIONS, project / "instructions.md"); copy_knowledge(project / "knowledge")
    contract = platform_contract("claude_project", version, {"mode": "claude_project", "project_instructions": True, "project_knowledge": True, "local_shell_available": False, "persistent_state_required": False})
    (project / "runtime-contract.json").write_text(json.dumps(contract, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (base / "README.md").write_text("# Architecture Analyzer – Claude Projects\\n\\nUse project/instructions.md as Project Instructions and add all files under project/knowledge/ as Project Knowledge. Repository source to analyze must be supplied separately.\\n", encoding="utf-8")
    (base / "VERSION").write_text(version + "\n", encoding="utf-8"); write_manifest(base, "claude_project", version, "README.md")

def build_opencode(base, version):
    runtime_root = base / ".opencode" / "architecture-analyzer"; runtime_root.mkdir(parents=True, exist_ok=True)
    shutil.copy2(CANONICAL_INSTRUCTIONS, runtime_root / "instructions.md"); copy_knowledge(runtime_root / "knowledge")
    contract = platform_contract("opencode", version, {"mode": "opencode_workspace", "native_filesystem": True, "native_shell": True, "assistant_runtime_root": ".opencode/architecture-analyzer", "target_source_must_remain_outside_runtime_root": True, "persistent_state_required": False})
    (runtime_root / "runtime-contract.json").write_text(json.dumps(contract, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    agents = "# Architecture Analyzer – OpenCode\\n\\nAnalyze the current source-code workspace using the canonical Architecture Analyzer contract. Assistant runtime/reference files are under .opencode/architecture-analyzer/ and must not be treated as target source evidence. Use native filesystem and shell read-only by default for inventory and evidence gathering. Do not modify target source unless the user explicitly asks for a separate implementation task.\\n\\n" + CANONICAL_INSTRUCTIONS.read_text(encoding="utf-8")
    (base / "AGENTS.md").write_text(agents, encoding="utf-8")
    cfg = {"$schema": "https://opencode.ai/config.json", "instructions": ["AGENTS.md"], "permission": {"edit": "ask", "bash": "ask"}}
    (base / "opencode.json").write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (base / "README.md").write_text("# Architecture Analyzer – OpenCode\\n\\nExtract at the root of the repository/workspace to analyze. Runtime/reference files remain isolated under .opencode/architecture-analyzer/.\\n", encoding="utf-8")
    (base / "VERSION").write_text(version + "\n", encoding="utf-8"); write_manifest(base, "opencode", version, "AGENTS.md")

def main():
    a = parse_args(); version = resolve_version(a.version); verify_sources(); out = Path(a.output_dir).resolve(); out.mkdir(parents=True, exist_ok=True)
    for p in out.glob("architecture-analyzer-*-v*.zip"): p.unlink()
    with tempfile.TemporaryDirectory() as td:
        t = Path(td); outputs = []
        for name, fn in {"custom-gpt": build_custom, "chat": build_portable, "claude": build_claude, "opencode": build_opencode}.items():
            root = t / name; root.mkdir(); fn(root, version); target = out / f"architecture-analyzer-{name}-v{version}.zip"; zipdir(root, target); outputs.append(target)
    for path in outputs: print(path)

if __name__ == "__main__": main()
