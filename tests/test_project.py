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
