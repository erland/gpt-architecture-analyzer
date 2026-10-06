# Project – Architecture Analyzer

## Purpose

Architecture Analyzer analyzes one or more source-code repositories and produces understandable, evidence-based architecture overviews without cluttering diagrams with unnecessary low-level detail.

## Canonical behavior

The behavioral source of truth is `canonical/instructions.md`. During migration it is intentionally identical to the previous `gpt-instructions.txt`; the legacy file remains in place until the distribution builders are migrated.

The ten files under `knowledge/` are the canonical method/reference layer. They contain the architecture-analysis method, evidence rules, grouping/diagram guidance, model schema, templates and examples.

## Model robustness

`guided`

The assistant follows an explicit multi-step analysis sequence, but persistent workflow state is not required.

## Runtime strategy

Registered peer candidates:

- ChatGPT Chat – ready, active
- ChatGPT Custom – ready, active
- Claude Projects – ready, active
- OpenCode – ready, active
- OpenAI Plugin – ready, active

OpenCode is considered a natural peer because direct local repository/workspace inspection is useful for the core use case. OpenAI Plugin is also active as a skills-first peer runtime, but repository/file access is a required host capability; without it the primary analysis task must block rather than simulate inspection.

## Project sources

- Canonical instruction: `canonical/instructions.md`
- Legacy instruction during migration: `gpt-instructions.txt`
- Knowledge: `knowledge/`
- Project contract: `gpt-project.yaml`
- Structured status: `project-status.yaml`
- Development plan: `docs/development-plan.md`

- Runtime parity: `runtime-parity.yaml`
- Test manifest: `tests/test-manifest.yaml`
