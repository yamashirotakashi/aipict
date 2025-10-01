import json
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PRESET_DIR = PROJECT_ROOT / "presets" / "comfyui"
PHASE3_CONFIG = PROJECT_ROOT / "config" / "phase3"


@pytest.fixture(scope="module")
def lightnovel_preset() -> dict:
    path = PRESET_DIR / "lightnovel_workflow.json"
    assert path.exists(), "ラノベ立ち絵プリセットが存在しません"
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def turnaround_preset() -> dict:
    path = PRESET_DIR / "turnaround_workflow.json"
    assert path.exists(), "三面図プリセットが存在しません"
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def preset_registry() -> dict:
    path = PHASE3_CONFIG / "preset_registry.json"
    assert path.exists(), "プリセットレジストリが存在しません"
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def character_tags() -> dict:
    path = PHASE3_CONFIG / "character_tags.json"
    assert path.exists(), "キャラクタータグ辞書が存在しません"
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def stage3_report_root() -> ET.Element:
    report_path = PROJECT_ROOT / "docs" / "xml" / "stage3-report.xml"
    assert report_path.exists(), "Stage3レポートが存在しません"
    tree = ET.parse(report_path)
    root = tree.getroot()
    assert root.tag == "Stage3Report", "Stage3レポートのルートタグが不正です"
    return root


def test_lightnovel_preset_structure(lightnovel_preset: dict) -> None:
    required_keys = {"name", "prompt", "negative_prompt", "loras", "sampler", "steps", "cfg", "resolution"}
    assert required_keys.issubset(lightnovel_preset), "ラノベ立ち絵プリセットに必要キーが不足しています"
    assert isinstance(lightnovel_preset["loras"], list) and lightnovel_preset["loras"], "LoRA設定が空です"
    for entry in lightnovel_preset["loras"]:
        assert "name" in entry and "weight" in entry, "LoRA設定に name/weight が必要です"


def test_turnaround_preset_constraints(turnaround_preset: dict) -> None:
    assert turnaround_preset.get("name") == "turnaround_batch", "三面図プリセットのnameが想定と異なります"
    assert turnaround_preset.get("seed_mode") == "fixed", "三面図プリセットはシード固定が必要です"
    views = turnaround_preset.get("views", [])
    assert set(views) == {"front", "side", "back"}, "三面図プリセットに必要な視点が不足しています"


def test_preset_registry_links(preset_registry: dict) -> None:
    entries = preset_registry.get("presets", [])
    assert entries, "プリセットレジストリに項目がありません"
    names = {item["id"] for item in entries}
    assert {"lightnovel_pose", "turnaround_batch"}.issubset(names), "レジストリに必須プリセットIDがありません"
    for item in entries:
        assert item.get("file"), "レジストリ項目にfileが必要です"
        assert (PRESET_DIR / item["file"]).exists(), f"プリセットファイルが存在しません: {item['file']}"


def test_character_tags_schema(character_tags: dict) -> None:
    assert "characters" in character_tags, "charactersキーがありません"
    for char_id, payload in character_tags["characters"].items():
        assert "prompt_prefix" in payload, f"{char_id} にprompt_prefixが不足"
        required_attrs = {"hair", "eyes", "costume", "age"}
        assert required_attrs.issubset(payload["attributes"].keys()), f"{char_id} に必須属性が不足"


def test_stage3_report_structure(stage3_report_root: ET.Element) -> None:
    required_sections = {"PresetCatalog", "CharacterConsistency", "Operations", "MCPPlans"}
    actual = {child.tag for child in stage3_report_root}
    missing = required_sections - actual
    assert not missing, f"Stage3レポートに欠落セクションがあります: {missing}"


def test_stage3_report_details(stage3_report_root: ET.Element) -> None:
    catalog = stage3_report_root.find("PresetCatalog")
    assert catalog is not None and list(catalog), "PresetCatalogに項目がありません"
    for item in catalog.findall("Preset"):
        assert item.get("id") and item.get("file"), "Preset項目にid/file属性が必要です"
    consistency = stage3_report_root.find("CharacterConsistency")
    assert consistency is not None
    rules = {rule.tag for rule in consistency}
    assert "TagPrefix" in rules and "KeyValue" in rules, "キャラクター一貫性ルールが不足しています"


def test_character_prompt_validator_exists() -> None:
    validator = PROJECT_ROOT / "scripts" / "phase3" / "check_character_prompt.py"
    assert validator.exists(), "キャラクタープロンプト検証スクリプトが存在しません"
    content = validator.read_text(encoding="utf-8")
    for snippet in ["json", "prompt_prefix", "missing", "exit"]:
        assert snippet in content, f"検証スクリプトに '{snippet}' が含まれていません"


def test_preset_sync_script_exists() -> None:
    sync_script = PROJECT_ROOT / "scripts" / "phase3" / "sync_presets.sh"
    assert sync_script.exists(), "プリセット同期スクリプトが存在しません"
    body = sync_script.read_text(encoding="utf-8")
    assert "rsync" in body or "cp" in body, "同期スクリプトにコピー処理が含まれていません"
    assert "preset_registry.json" in body, "同期スクリプトがレジストリ参照をしていません"
