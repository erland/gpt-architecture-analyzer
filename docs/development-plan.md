# Development plan – Architecture Analyzer migration

**Target:** GPT Builder 1.5.0  
**Migration type:** existing-project, behavior-preserving  
**Model robustness:** `guided`

## Goal

Migrate the existing Architecture Analyzer project to the GPT Builder 1.5.0 project and runtime model without weakening its evidence-based architecture-analysis behavior.

The current `gpt-instructions.txt`, ten Knowledge files, Custom GPT distribution and portable Chat distribution are treated as working legacy sources until equivalent generated distributions are verified.

## Step 1 – GPT Builder 1.5 project contracts and guided model robustness

Introduce:

- `canonical/instructions.md` as the new behavioral source of truth,
- `gpt-project.yaml`,
- structured project status and development plan,
- capability, artifact, workspace/state and tool contracts,
- explicit assessment of all five registered peer runtimes,
- `guided` model robustness.

The canonical instruction must remain behaviorally identical to the existing instruction in this step.

**Done when:** the project contract is internally valid, canonical/legacy instructions match, the ten Knowledge files remain unchanged, existing Chat and Custom GPT builds/validation pass, and CI is green.

## Step 2 – Deterministic tests and instruction-adherence evals

Add regression tests and behavioral evals for:

- repository inventory,
- evidence and confidence,
- grouping before diagramming,
- large-repository partial analysis,
- uncertainty language,
- diagram clutter limits,
- report structure.

Add a test manifest and deterministic validation of critical behavior markers.

## Step 3 – Claude Projects and OpenCode peer distributions

Generate both new runtimes from the same canonical contracts.

Claude Projects must carry canonical instructions plus the Knowledge layer.

OpenCode must keep the analyzed repository workspace separate from assistant/runtime files and use local workspace/tool access without changing the evidence contract.

## Step 4 – Generalized runtime parity and release pipeline

Compare all five registered runtimes across:

- behavior,
- capability,
- artifact,
- workspace/state,
- tool.

Activate Chat, Custom GPT, Claude Projects and OpenCode. Keep OpenAI Plugin explicitly reduced/inactive unless later runtime capabilities justify activation.

Separate/modernize CI and release validation as needed. GitHub Release tags remain the authoritative version source.

## Step 5 – Final regression, hygiene and release readiness

Run the complete regression set, all active distribution validators, runtime parity, release readiness, workflow parity, project hygiene and reproducibility checks.

**Done when:** no blockers remain and the PR is ready to merge.

## Current next step

**Step 1 – GPT Builder 1.5 project contracts and guided model robustness.**
