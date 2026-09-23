# Status – Architecture Analyzer

## Summary

Migration to **GPT Builder 1.5.0** has started.

The existing Architecture Analyzer behavior and both current distributions are being preserved while a modern canonical/project-contract layer is introduced.

## Migration steps

- [x] Step 1 – GPT Builder 1.5 project contracts and guided model robustness
- [x] Step 2 – Deterministic tests and instruction-adherence evals
- [ ] Step 3 – Claude Projects and OpenCode peer distributions
- [ ] Step 4 – Generalized runtime parity and release pipeline
- [ ] Step 5 – Final regression, hygiene and release readiness

## Current runtime state

- ChatGPT Chat: ready / active
- ChatGPT Custom: ready / active
- Claude Projects: ready / planned
- OpenCode: ready / planned
- OpenAI Plugin: reduced / inactive

## Verification of step 1

CI passed the new GPT project lint, the existing distribution build and the existing distribution validation. `canonical/instructions.md` remains byte-for-byte identical to `gpt-instructions.txt`, and all ten Knowledge files remain in place.

## Verification of step 2

CI passed deterministic regression tests and the blocking instruction-adherence suite for evidence/confidence, grouping before diagramming, large-repository handling, uncertainty language and clutter control. Existing Chat and Custom GPT distribution build/validation still pass.

## Current step

**Step 3 – Claude Projects and OpenCode peer distributions.**

## Blockers

No known blockers before CI verification.
