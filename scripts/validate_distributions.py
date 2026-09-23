#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, re, zipfile
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE = ["knowledge/architecture-analysis-method.md","knowledge/architecture-model-schema.md","knowledge/clutter-control-and-grouping-rules.md","knowledge/diagram-style-guide.md","knowledge/evidence-and-confidence-rules.md","knowledge/example-prompts.md","knowledge/output-templates.md","knowledge/quadrant-scoring-rubric.md","knowledge/repository-inspection-checklist.md","knowledge/view-catalog.md"]
SEMVER = re.compile(r"^(0|[1-9]\\d*)\\.(0|[1-9]\\d*)\\.(0|[1-9]\\d*)(?:-[0-9A-Za-z.-]+)?(?:\\+[0-9A-Za-z.-]+)?$")
def digest(b): return hashlib.sha256(b).hexdigest()
def args(): p=argparse.ArgumentParser(); p.add_argument("--version"); p.add_argument("--dist",default=str(ROOT/"dist")); return p.parse_args()
def ver(v):
    x=(v or (ROOT/"VERSION").read_text()).strip(); x=x[1:] if x.startswith("v") else x
    if not SEMVER.fullmatch(x): raise SystemExit(f"Ogiltig version: {x}")
    return x
def starters_text():
    lines=(ROOT/"gpt-configuration.md").read_text(encoding="utf-8").splitlines(); i=lines.index("## Suggested conversation starters")+1; out=[]
    for line in lines[i:]:
        if line.startswith("## "): break
        if line.startswith("- "): out.append(line[2:])
    return "# Suggested conversation starters\\n\\n"+"\\n".join(f"- {x}" for x in out)+"\\n"
def verify_manifest(z,runtime_id,version):
    m=json.loads(z.read("MANIFEST.json"))
    if m.get("runtime_id")!=runtime_id: raise SystemExit(f"Fel runtime_id i manifest: {runtime_id}")
    if m.get("version")!=version: raise SystemExit(f"Fel manifestversion: {runtime_id}")
    for rel,meta in m.get("files",{}).items():
        if digest(z.read(rel))!=meta.get("sha256"): raise SystemExit(f"Fel hash i manifest {runtime_id}: {rel}")
def validate(v,dist):
    paths={"custom":dist/f"architecture-analyzer-custom-gpt-v{v}.zip","chat":dist/f"architecture-analyzer-chat-v{v}.zip","claude":dist/f"architecture-analyzer-claude-v{v}.zip","opencode":dist/f"architecture-analyzer-opencode-v{v}.zip"}
    for p in paths.values():
        if not p.is_file(): raise SystemExit(f"Saknar {p}")
        with zipfile.ZipFile(p) as z:
            if z.testzip() is not None: raise SystemExit(f"Korrupt ZIP: {p}")
    with zipfile.ZipFile(paths["custom"]) as z:
        exp={"gpt-instructions.txt","gpt-configuration.md","gpt-config.json","docs/setup-steps.md","VERSION",*KNOWLEDGE}
        if set(z.namelist())!=exp: raise SystemExit("Custom GPT-innehåll avviker")
    with zipfile.ZipFile(paths["chat"]) as z:
        k={f"knowledge/{Path(x).name}" for x in KNOWLEDGE}; exp={"START-HERE.md","VERSION","MANIFEST.json","assistant/instructions.txt","assistant/conversation-starters.md",*k}
        if set(z.namelist())!=exp: raise SystemExit("Portable-innehåll avviker")
        if z.read("assistant/instructions.txt")!=(ROOT/"canonical/instructions.md").read_bytes(): raise SystemExit("Portable instruktion avviker från canonical")
        if z.read("assistant/conversation-starters.md").decode()!=starters_text(): raise SystemExit("Portable starters avviker")
        verify_manifest(z,"chatgpt_chat",v)
    with zipfile.ZipFile(paths["claude"]) as z:
        k={f"project/knowledge/{Path(x).name}" for x in KNOWLEDGE}; req={"README.md","VERSION","MANIFEST.json","project/instructions.md","project/runtime-contract.json",*k}
        if set(z.namelist())!=req: raise SystemExit(f"Claude-innehåll avviker: {sorted(set(z.namelist())^req)}")
        if z.read("project/instructions.md")!=(ROOT/"canonical/instructions.md").read_bytes(): raise SystemExit("Claude instruktion avviker")
        c=json.loads(z.read("project/runtime-contract.json"))
        if c.get("runtime_id")!="claude_project": raise SystemExit("Claude runtime_id fel")
        if c.get("adapter",{}).get("local_shell_available") is not False: raise SystemExit("Claude shell declaration fel")
        verify_manifest(z,"claude_project",v)
    with zipfile.ZipFile(paths["opencode"]) as z:
        k={f".opencode/architecture-analyzer/knowledge/{Path(x).name}" for x in KNOWLEDGE}; req={"AGENTS.md","opencode.json","README.md","VERSION","MANIFEST.json",".opencode/architecture-analyzer/instructions.md",".opencode/architecture-analyzer/runtime-contract.json",*k}
        if set(z.namelist())!=req: raise SystemExit(f"OpenCode-innehåll avviker: {sorted(set(z.namelist())^req)}")
        if z.read(".opencode/architecture-analyzer/instructions.md")!=(ROOT/"canonical/instructions.md").read_bytes(): raise SystemExit("OpenCode instruktion avviker")
        agents=z.read("AGENTS.md").decode()
        for marker in ("Architecture Analyzer",".opencode/architecture-analyzer/","must not be treated as target source evidence"):
            if marker not in agents: raise SystemExit(f"OpenCode AGENTS saknar {marker}")
        c=json.loads(z.read(".opencode/architecture-analyzer/runtime-contract.json")); a=c.get("adapter",{})
        if c.get("runtime_id")!="opencode": raise SystemExit("OpenCode runtime_id fel")
        if a.get("native_filesystem") is not True or a.get("native_shell") is not True: raise SystemExit("OpenCode native capability declaration fel")
        if a.get("target_source_must_remain_outside_runtime_root") is not True: raise SystemExit("OpenCode workspace separation saknas")
        verify_manifest(z,"opencode",v)
    print(f"OK: fyra distributioner validerade för {v}")
def main(): a=args(); validate(ver(a.version),Path(a.dist).resolve())
if __name__=="__main__": main()
