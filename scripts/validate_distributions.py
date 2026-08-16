#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, re, zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
KNOWLEDGE=[
"knowledge/architecture-analysis-method.md","knowledge/architecture-model-schema.md","knowledge/clutter-control-and-grouping-rules.md","knowledge/diagram-style-guide.md","knowledge/evidence-and-confidence-rules.md","knowledge/example-prompts.md","knowledge/output-templates.md","knowledge/quadrant-scoring-rubric.md","knowledge/repository-inspection-checklist.md","knowledge/view-catalog.md"]
SEMVER=re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")
def digest(b): return hashlib.sha256(b).hexdigest()
def args(): p=argparse.ArgumentParser(); p.add_argument('--version'); p.add_argument('--dist',default=str(ROOT/'dist')); return p.parse_args()
def ver(v):
 x=(v or (ROOT/'VERSION').read_text()).strip(); x=x[1:] if x.startswith('v') else x
 if not SEMVER.fullmatch(x): raise SystemExit(f'Ogiltig version: {x}')
 return x
def starters_text():
 lines=(ROOT/'gpt-configuration.md').read_text(encoding='utf-8').splitlines(); i=lines.index('## Suggested conversation starters')+1; out=[]
 for line in lines[i:]:
  if line.startswith('## '): break
  if line.startswith('- '): out.append(line[2:])
 return '# Suggested conversation starters\n\n'+'\n'.join(f'- {x}' for x in out)+'\n'
def validate(v,dist):
 cz=dist/f'architecture-analyzer-custom-gpt-v{v}.zip'; pz=dist/f'architecture-analyzer-chat-v{v}.zip'
 for z in (cz,pz):
  if not z.is_file(): raise SystemExit(f'Saknar {z}')
  with zipfile.ZipFile(z) as f:
   if f.testzip() is not None: raise SystemExit(f'Korrupt ZIP: {z}')
 with zipfile.ZipFile(cz) as z:
  exp={'gpt-instructions.txt','gpt-configuration.md','gpt-config.json','docs/setup-steps.md','VERSION',*KNOWLEDGE}
  if set(z.namelist())!=exp: raise SystemExit(f'Custom GPT-innehåll avviker: {sorted(set(z.namelist())^exp)}')
  for rel in ['gpt-instructions.txt','gpt-configuration.md','gpt-config.json','docs/setup-steps.md',*KNOWLEDGE]:
   if z.read(rel)!=(ROOT/rel).read_bytes(): raise SystemExit(f'Custom källa ändrad: {rel}')
  if z.read('VERSION').decode().strip()!=v: raise SystemExit('Fel VERSION i custom')
 with zipfile.ZipFile(pz) as z:
  kportable={f'knowledge/{Path(x).name}' for x in KNOWLEDGE}
  exp={'START-HERE.md','VERSION','MANIFEST.json','assistant/instructions.txt','assistant/conversation-starters.md',*kportable}
  if set(z.namelist())!=exp: raise SystemExit(f'Portable-innehåll avviker: {sorted(set(z.namelist())^exp)}')
  if z.read('assistant/instructions.txt')!=(ROOT/'gpt-instructions.txt').read_bytes(): raise SystemExit('Portable instruktion ändrad')
  if z.read('assistant/conversation-starters.md').decode()!=starters_text(): raise SystemExit('Portable starters avviker')
  for rel in KNOWLEDGE:
   if z.read(f'knowledge/{Path(rel).name}')!=(ROOT/rel).read_bytes(): raise SystemExit(f'Portable Knowledge ändrad: {rel}')
  if z.read('VERSION').decode().strip()!=v: raise SystemExit('Fel VERSION i portable')
  m=json.loads(z.read('MANIFEST.json')); 
  if m.get('version')!=v: raise SystemExit('Fel manifestversion')
  for rel,h in m.get('files',{}).items():
   if digest(z.read(rel))!=h: raise SystemExit(f'Fel hash i manifest: {rel}')
 print(f'OK: båda distributionerna validerade för {v}')
def main(): a=args(); validate(ver(a.version),Path(a.dist).resolve())
if __name__=='__main__': main()
