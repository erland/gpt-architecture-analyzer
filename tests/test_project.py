from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_canonical_matches_legacy_instruction():
    assert (ROOT / "canonical/instructions.md").read_bytes() == (ROOT / "gpt-instructions.txt").read_bytes()


def test_guided_model_robustness_is_declared():
    cfg = yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))
    robust = cfg["model_robustness"]
    assert robust["level"] == "guided"
    assert robust["operational_core"] is True
    assert robust["explicit_workflow"] is True
    assert robust["deterministic_gates"] is True
    assert robust["instruction_adherence_evals"] is True


def test_core_analysis_contract_is_explicit():
    text = (ROOT / "canonical/instructions.md").read_text(encoding="utf-8")
    for marker in [
        "Inventory the repositories",
        "Infer architecture model",
        "Group aggressively before diagramming",
        "Include evidence and confidence",
        "Highlight risks, hotspots",
        "Never claim exact behavior unless supported by source evidence",
    ]:
        assert marker in text


def test_evidence_and_uncertainty_rules_exist():
    text = (ROOT / "knowledge/evidence-and-confidence-rules.md").read_text(encoding="utf-8")
    for marker in [
        "High confidence:",
        "Medium confidence:",
        "Low confidence:",
        "I infer",
        "This appears to",
        "I did not find",
        "pretending to have run the system",
    ]:
        assert marker in text


def test_clutter_control_rules_are_explicit():
    text = (ROOT / "knowledge/clutter-control-and-grouping-rules.md").read_text(encoding="utf-8")
    for marker in [
        "Target: 5-9 primary nodes",
        "Soft maximum: 12 primary nodes",
        "Hard maximum: 15 nodes",
        "Always group before drawing",
    ]:
        # "Always group..." lives in the analysis method rather than this file.
        if marker == "Always group before drawing":
            assert marker in (ROOT / "knowledge/architecture-analysis-method.md").read_text(encoding="utf-8")
        else:
            assert marker in text


def test_large_repository_strategy_is_compact_and_progressive():
    text = (ROOT / "knowledge/output-templates.md").read_text(encoding="utf-8")
    for marker in [
        "Compact response for large repositories",
        "inventory",
        "top-level grouped view",
        "analysis plan for deeper slices",
        "first-pass hotspots",
    ]:
        assert marker in text


def test_all_ten_knowledge_files_are_present():
    files = sorted(p.name for p in (ROOT / "knowledge").glob("*") if p.is_file())
    assert len(files) == 10


def test_instruction_adherence_suite_is_registered():
    manifest = yaml.safe_load((ROOT / "tests/test-manifest.yaml").read_text(encoding="utf-8"))
    suite = manifest["suites"]["instruction_adherence"]
    assert suite["type"] == "behavioral"
    assert suite["blocking"] is True
    cases = sorted((ROOT / suite["path"]).glob("*.yaml"))
    assert len(cases) >= 5
    for path in cases:
        case = yaml.safe_load(path.read_text(encoding="utf-8"))
        assert case["criticality"] in {"critical", "important", "optional"}
        assert case["input"]
        assert case["expected"]["required"]


def test_runtime_assessment_keeps_opencode_ready():
    cfg = yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))
    candidates = {x["runtime_id"]: x for x in cfg["analysis"]["runtime"]["candidates"]}
    assert candidates["opencode"]["suitability"] == "ready"
    assert candidates["opencode"]["activate_by_default"] is True
    assert candidates["openai_plugin"]["suitability"] == "reduced"
    assert candidates["openai_plugin"]["activate_by_default"] is False


def test_claude_and_opencode_are_active_peer_runtimes():
    cfg = yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))
    assert cfg["runtime"]["claude"]["enabled"] is True
    assert cfg["runtime"]["claude"]["mode"] == "claude_project"
    assert cfg["runtime"]["opencode"]["enabled"] is True
    assert cfg["runtime"]["opencode"]["mode"] == "opencode_workspace"
    assert cfg["runtime"]["opencode"]["runtime_root"] == ".opencode/architecture-analyzer"


def test_build_and_validation_cover_new_peer_distributions():
    build = (ROOT / "scripts/build_distributions.py").read_text(encoding="utf-8")
    validate = (ROOT / "scripts/validate_distributions.py").read_text(encoding="utf-8")
    for marker in [
        "def build_claude(",
        "def build_opencode(",
        '("claude", build_claude',
        '("opencode", build_opencode',
        'f"architecture-analyzer-{name}-v{version}.zip"',
        ".opencode/architecture-analyzer",
    ]:
        assert marker in build
    for marker in ["claude_project", "opencode", "projektpaket och fyra runtime-distributioner"]:
        assert marker in validate


def test_runtime_parity_model_covers_all_registered_peers():
    cfg = yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))
    parity = yaml.safe_load((ROOT / "runtime-parity.yaml").read_text(encoding="utf-8"))
    expected = {
        "chatgpt_chat", "chatgpt_custom", "claude_project", "opencode", "openai_plugin"
    }
    assert set(cfg["runtime_parity"]["registered_runtimes"]) == expected
    assert set(parity["registered_runtimes"]) == expected
    assert set(parity["compared_categories"]) == {
        "behavior", "capability", "artifact", "workspace_state", "tool"
    }
    for runtime_id in {"chatgpt_chat", "chatgpt_custom", "claude_project", "opencode"}:
        assert parity["runtimes"][runtime_id]["active"] is True
        assert parity["runtimes"][runtime_id]["suitability"] == "ready"
    assert parity["runtimes"]["openai_plugin"]["active"] is False
    assert parity["runtimes"]["openai_plugin"]["suitability"] == "reduced"


def test_release_pipeline_publishes_complete_distribution_set():
    workflow = (ROOT / ".github/workflows/build-distributions.yml").read_text(encoding="utf-8")
    for marker in [
        "scripts/validate_runtime_parity.py",
        "scripts/validate_release_readiness.py",
        "architecture-analyzer-project-v${VERSION}.zip",
        "architecture-analyzer-chat-v${VERSION}.zip",
        "architecture-analyzer-custom-gpt-v${VERSION}.zip",
        "architecture-analyzer-claude-v${VERSION}.zip",
        "architecture-analyzer-opencode-v${VERSION}.zip",
        "dist/SHA256SUMS.txt",
        "dist/DELIVERY-MANIFEST.json",
    ]:
        assert marker in workflow


def test_runtime_and_release_validators_exist():
    assert (ROOT / "scripts/validate_runtime_parity.py").is_file()
    assert (ROOT / "scripts/validate_release_readiness.py").is_file()


def test_final_quality_gates_are_wired_into_ci():
    workflow = (ROOT / ".github/workflows/build-distributions.yml").read_text(encoding="utf-8")
    for marker in [
        "scripts/project_hygiene.py --project-root . --mode final",
        "scripts/validate_workflow_parity.py",
        "scripts/verify_reproducible_build.py",
    ]:
        assert marker in workflow


def test_final_documentation_matches_runtime_state():
    project = (ROOT / "PROJECT.md").read_text(encoding="utf-8")
    plan = (ROOT / "docs/development-plan.md").read_text(encoding="utf-8")
    for marker in [
        "Claude Projects – ready, active",
        "OpenCode – ready, active",
        "Runtime parity: `runtime-parity.yaml`",
    ]:
        assert marker in project
    assert "**Step 5 – Final regression, hygiene and release readiness.**" in plan
    assert "**Step 1 – GPT Builder 1.5 project contracts" not in plan.split("## Current next step")[-1]


def test_final_quality_gate_scripts_exist():
    for rel in [
        "scripts/project_hygiene.py",
        "scripts/validate_workflow_parity.py",
        "scripts/verify_reproducible_build.py",
    ]:
        assert (ROOT / rel).is_file()
