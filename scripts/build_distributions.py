#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, re, shutil, tempfile, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION_FILE = ROOT / "VERSION"
INSTRUCTIONS = ROOT / "gpt-instructions.txt"
CONFIG_MD = ROOT / "gpt-configuration.md"
CONFIG_JSON = ROOT / "gpt-config.json"
SETUP = ROOT / "docs" / "setup-steps.md"
START_HERE = ROOT / "portable" / "START-HERE.md"
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
FIXED_TIME=(2020,1,1,0,0,0)


def parse_args():
    p=argparse.ArgumentParser(); p.add_argument("--version"); p.add_argument("--output-dir",default=str(ROOT/"dist")); return p.parse_args()

def resolve_version(v):
    x=(v or VERSION_FILE.read_text(encoding="utf-8")).strip(); x=x[1:] if x.startswith("v") else x
    if not SEMVER.fullmatch(x): raise SystemExit(f"Ogiltig version: {x!r}")
    return x

def starters_text():
    lines=CONFIG_MD.read_text(encoding="utf-8").splitlines()
    try: i=lines.index("## Suggested conversation starters")+1
    except ValueError: raise SystemExit("Saknar Suggested conversation starters i gpt-configuration.md")
    out=[]
    for line in lines[i:]:
        if line.startswith("## "): break
        if line.startswith("- "): out.append(line[2:])
    if not out: raise SystemExit("Inga conversation starters hittades")
    return "# Suggested conversation starters\n\n" + "\n".join(f"- {x}" for x in out) + "\n"

def verify_sources():
    for p in [INSTRUCTIONS,CONFIG_MD,CONFIG_JSON,SETUP,START_HERE]:
        if not p.is_file(): raise SystemExit(f"Saknar {p.relative_to(ROOT)}")
    actual=sorted(str(p.relative_to(ROOT)).replace('\\','/') for p in (ROOT/'knowledge').glob('*') if p.is_file())
    if actual!=sorted(KNOWLEDGE):
        raise SystemExit(f"Knowledge-filuppsättningen avviker. Saknas={sorted(set(KNOWLEDGE)-set(actual))}, extra={sorted(set(actual)-set(KNOWLEDGE))}")
    cfg=json.loads(CONFIG_JSON.read_text(encoding="utf-8"))
    if sorted(cfg.get("knowledge_files",[]))!=sorted(KNOWLEDGE): raise SystemExit("gpt-config.json knowledge_files avviker från faktisk Knowledge")

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def zipdir(src,dst):
    dst.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(dst,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(x for x in src.rglob('*') if x.is_file()):
            info=zipfile.ZipInfo(p.relative_to(src).as_posix(),FIXED_TIME); info.compress_type=zipfile.ZIP_DEFLATED; info.external_attr=0o100644<<16
            z.writestr(info,p.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)

def build_custom(base,version):
    for rel in ["gpt-instructions.txt","gpt-configuration.md","gpt-config.json","docs/setup-steps.md",*KNOWLEDGE]:
        dst=base/rel; dst.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(ROOT/rel,dst)
    (base/'VERSION').write_text(version+'\n',encoding='utf-8')

def build_portable(base,version):
    shutil.copy2(START_HERE,base/'START-HERE.md')
    (base/'assistant').mkdir(parents=True,exist_ok=True)
    shutil.copy2(INSTRUCTIONS,base/'assistant'/'instructions.txt')
    (base/'assistant'/'conversation-starters.md').write_text(starters_text(),encoding='utf-8')
    for rel in KNOWLEDGE:
        dst=base/'knowledge'/Path(rel).name; dst.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(ROOT/rel,dst)
    (base/'VERSION').write_text(version+'\n',encoding='utf-8')
    files={}
    for p in sorted(x for x in base.rglob('*') if x.is_file() and x.name!='MANIFEST.json'):
        files[p.relative_to(base).as_posix()]=sha(p)
    manifest={"package":"architecture-analyzer","format":"portable-chat-assistant","version":version,"entrypoint":"START-HERE.md","instructions":"assistant/instructions.txt","files":files}
    (base/'MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
    a=parse_args(); version=resolve_version(a.version); verify_sources(); out=Path(a.output_dir).resolve(); out.mkdir(parents=True,exist_ok=True)
    for p in out.glob('architecture-analyzer-*-v*.zip'): p.unlink()
    with tempfile.TemporaryDirectory() as td:
        t=Path(td); c=t/'custom'; p=t/'portable'; c.mkdir(); p.mkdir(); build_custom(c,version); build_portable(p,version)
        cz=out/f'architecture-analyzer-custom-gpt-v{version}.zip'; pz=out/f'architecture-analyzer-chat-v{version}.zip'; zipdir(c,cz); zipdir(p,pz)
    print(cz); print(pz)
if __name__=='__main__': main()
