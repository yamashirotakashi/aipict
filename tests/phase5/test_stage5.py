import json
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = PROJECT_ROOT / "config" / "phase5"
SCRIPTS_DIR = PROJECT_ROOT / "scripts" / "phase5"


@pytest.fixture(scope="module")
def playbook_json() -> dict:
    path = CONFIG_DIR / "playbook.json"
    assert path.exists(), "データ整備プレイブックjsonが存在しません"
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def ledger_rules() -> dict:
    path = CONFIG_DIR / "ledger_rules.json"
    assert path.exists(), "台帳検証ルールjsonが存在しません"
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def stage5_report_root() -> ET.Element:
    report_path = PROJECT_ROOT / "docs" / "xml" / "stage5-report.xml"
    assert report_path.exists(), "Stage5レポートが存在しません"
    tree = ET.parse(report_path)
    root = tree.getroot()
    assert root.tag == "Stage5Report", "Stage5レポートのルートタグが不正です"
    return root


def test_playbook_structure(playbook_json: dict) -> None:
    steps = playbook_json.get("steps", [])
    assert len(steps) >= 5, "Playbookのステップ数が不足しています"
    required_order = [
        "collect_images",
        "normalize",
        "auto_caption",
        "deduplicate",
        "split_and_report",
    ]
    ids = [step.get("id") for step in steps]
    for req in required_order:
        assert req in ids, f"Playbookに {req} が含まれていません"


def test_ledger_rules(ledger_rules: dict) -> None:
    required_columns = ledger_rules.get("required_columns", [])
    assert set(required_columns) >= {
        "image_id",
        "source",
        "license",
        "usage",
        "commercial_ok",
        "credit_required",
    }, "必須カラム定義が不足しています"
    assert "validators" in ledger_rules, "validatorsが定義されていません"


def test_stage5_report_sections(stage5_report_root: ET.Element) -> None:
    required = {"Playbook", "Automation", "Validation", "MCPPlans"}
    actual = {child.tag for child in stage5_report_root}
    missing = required - actual
    assert not missing, f"Stage5レポートに欠落セクションがあります: {missing}"


def test_stage5_report_details(stage5_report_root: ET.Element) -> None:
    playbook = stage5_report_root.find("Playbook")
    assert playbook is not None and list(playbook), "Playbookセクションが空です"
    automation = stage5_report_root.find("Automation")
    assert automation is not None
    tools = {elem.get("name") for elem in automation.findall("Tool")}
    assert {"Serena", "Cipher", "Zen"}.issubset(tools)
    validation = stage5_report_root.find("Validation")
    assert validation is not None
    assert validation.find("LedgerCheck") is not None
    assert validation.find("CaptionQuality") is not None


def test_validate_ledger_script_exists() -> None:
    script = SCRIPTS_DIR / "validate_ledger.py"
    assert script.exists(), "台帳検証スクリプトが存在しません"
    body = script.read_text(encoding="utf-8")
    for snippet in ["csv", "required_columns", "missing", "error"]:
        assert snippet in body, f"validate_ledger.py に '{snippet}' が含まれていません"


def test_data_hygiene_playbook_script_exists() -> None:
    script = SCRIPTS_DIR / "data_hygiene_playbook.sh"
    assert script.exists(), "データ整備プレイブックスクリプトが存在しません"
    text = script.read_text(encoding="utf-8")
    for snippet in [
        "codex run --agent Serena",
        "codex run --agent Cipher",
        "codex run --agent Zen",
        "python scripts/phase4/generate_captions.py",
        "python scripts/phase4/dedup_images.py",
    ]:
        assert snippet in text, f"data_hygiene_playbook.sh に '{snippet}' が含まれていません"


def test_todo_generator_exists() -> None:
    script = SCRIPTS_DIR / "generate_todo.py"
    assert script.exists(), "TODO生成スクリプトが存在しません"
    content = script.read_text(encoding="utf-8")
    for snippet in ["json", "playbook", "Serena", "print"]:
        assert snippet in content, f"generate_todo.py に '{snippet}' が含まれていません"
