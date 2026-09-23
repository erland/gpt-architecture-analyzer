# Status – Architecture Analyzer

## Summary

Migration to **GPT Builder 1.5.0** is complete.

The existing Architecture Analyzer behavior and both current distributions are being preserved while a modern canonical/project-contract layer is introduced.

## Migration steps

- [x] Step 1 – GPT Builder 1.5 project contracts and guided model robustness
- [x] Step 2 – Deterministic tests and instruction-adherence evals
- [x] Step 3 – Claude Projects and OpenCode peer distributions
- [x] Step 4 – Generalized runtime parity and release pipeline
- [x] Step 5 – Final regression, hygiene and release readiness

## Current runtime state

- ChatGPT Chat: ready / active
- ChatGPT Custom: ready / active
- Claude Projects: ready / active
- OpenCode: ready / active
- OpenAI Plugin: reduced / inactive

## Verification of step 1

CI passed the new GPT project lint, the existing distribution build and the existing distribution validation. `canonical/instructions.md` remains byte-for-byte identical to `gpt-instructions.txt`, and all ten Knowledge files remain in place.

## Verification of step 2

CI passed deterministic regression tests and the blocking instruction-adherence suite for evidence/confidence, grouping before diagramming, large-repository handling, uncertainty language and clutter control. Existing Chat and Custom GPT distribution build/validation still pass.

## Verification of step 3

CI passed the four-runtime build and validation. Claude Projects uses the canonical instruction and all ten Knowledge files. OpenCode uses the same canonical contract, keeps Architecture Analyzer runtime/reference files under `.opencode/architecture-analyzer/`, and explicitly excludes that runtime root from target-source evidence.

## Verification of step 4

CI passed generalized runtime parity across all five registered runtimes. The active release set now contains a project ZIP plus Chat, Custom GPT, Claude Projects and OpenCode ZIPs, together with `SHA256SUMS.txt` and `DELIVERY-MANIFEST.json`. GitHub Release uploads the complete set explicitly and uses the release tag as the authoritative version source.

## Verification of step 5

The final CI run passed project lint, deterministic regression tests, instruction-adherence validation, project plus four runtime builds, distribution validation, runtime parity, release readiness, project hygiene, workflow parity, reproducible delivery and artifact upload.

Documentation drift found during the final review was corrected and regression-tested.

## Current state

The project is in **maintenance mode**. The migration is complete and the PR is ready to merge.

## Blockers

None.
