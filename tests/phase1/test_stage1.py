import xml.etree.ElementTree as ET
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="module")
def setup_script() -> Path:
    return PROJECT_ROOT / "scripts" / "phase1" / "setup_wsl_rocm.sh"


def test_setup_script_exists_and_contains_required_steps(setup_script: Path) -> None:
    assert setup_script.exists(), "Phase1 setupスクリプトが存在しません"
    content = setup_script.read_text(encoding="utf-8")
    required_snippets = [
        "wsl --install -d",
        "wsl --update",
        "sudo apt update",
        "python3 -m venv /opt/ai/venvs/rocm",
        "pip install --index-url https://download.pytorch.org/whl/rocm",
        "python - <<'PY'",
        "torch.__version__",
    ]
    for snippet in required_snippets:
        assert snippet in content, f"setupスクリプトに '{snippet}' が含まれていません"


@pytest.fixture(scope="module")
def stage1_report() -> ET.Element:
    report_path = PROJECT_ROOT / "docs" / "xml" / "stage1-report.xml"
    assert report_path.exists(), "Stage1レポートXMLが存在しません"
    tree = ET.parse(report_path)
    root = tree.getroot()
    assert root.tag == "Stage1Report", "Stage1レポートのルートタグがStage1Reportではありません"
    return root


def test_stage1_report_sections(stage1_report: ET.Element) -> None:
    required_sections = ["Checklist", "KnownPitfalls", "Logs", "MCPPlans"]
    tags = {child.tag for child in stage1_report}
    for section in required_sections:
        assert section in tags, f"Stage1レポートに{section}セクションがありません"


def test_stage1_report_checklist_items(stage1_report: ET.Element) -> None:
    checklist = stage1_report.find("Checklist")
    assert checklist is not None and list(checklist), "Checklistに項目がありません"
    for item in checklist.findall("Item"):
        assert item.find("Task") is not None, "Checklist項目にTaskがありません"
        assert item.find("SuccessCriteria") is not None, "Checklist項目にSuccessCriteriaがありません"
        assert item.find("FailureModes") is not None, "Checklist項目にFailureModesがありません"


def test_stage1_log_template_exists() -> None:
    log_path = PROJECT_ROOT / "logs" / "phase1" / "torch_device_check_example.log"
    assert log_path.exists(), "torchデバイス検証ログテンプレートがありません"
    content = log_path.read_text(encoding="utf-8").strip()
    assert "torch:" in content and "is_hip_available:" in content, "ログテンプレートに期待するキーがありません"
