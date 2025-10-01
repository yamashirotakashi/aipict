import csv
import json
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = PROJECT_ROOT / "config" / "phase4"
SCRIPTS_DIR = PROJECT_ROOT / "scripts" / "phase4"
DATASET_TEMPLATE = PROJECT_ROOT / "datasets" / "lora_template"


@pytest.fixture(scope="module")
def ledger_template() -> Path:
    path = CONFIG_DIR / "dataset_ledger.csv"
    assert path.exists(), "データ台帳テンプレートがありません"
    return path


@pytest.fixture(scope="module")
def caption_config() -> dict:
    path = CONFIG_DIR / "caption_config.json"
    assert path.exists(), "キャプション設定JSONがありません"
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def dedup_config() -> dict:
    path = CONFIG_DIR / "dedup_config.json"
    assert path.exists(), "重複除去設定JSONがありません"
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def stage4_report_root() -> ET.Element:
    report_path = PROJECT_ROOT / "docs" / "xml" / "stage4-report.xml"
    assert report_path.exists(), "Stage4レポートが存在しません"
    tree = ET.parse(report_path)
    root = tree.getroot()
    assert root.tag == "Stage4Report", "Stage4レポートのルートタグが不正です"
    return root


def test_dataset_structure_exists() -> None:
    required_dirs = ["images", "captions", "splits", "reports"]
    for folder in required_dirs:
        path = DATASET_TEMPLATE / folder
        assert path.exists(), f"テンプレートフォルダが不足しています: {folder}"


def test_ledger_template_columns(ledger_template: Path) -> None:
    with ledger_template.open(newline="", encoding="utf-8") as fh:
        reader = csv.reader(fh)
        header = next(reader)
    required = {"image_id", "source", "license", "usage", "commercial_ok", "credit_required", "notes"}
    assert required.issubset(header), "データ台帳ヘッダが仕様不足"


def test_caption_config_defaults(caption_config: dict) -> None:
    assert caption_config.get("tool") in {"wd14", "deepdanbooru"}
    thresholds = caption_config.get("thresholds", {})
    assert 0 <= thresholds.get("min_score", 0) <= 1
    assert caption_config.get("output_dir") == "captions"


def test_dedup_config_schema(dedup_config: dict) -> None:
    assert dedup_config.get("method") in {"phash", "ahash", "dhash"}
    assert dedup_config.get("max_distance") >= 0
    assert dedup_config.get("output") == "reports/duplicates.json"


def test_stage4_report_sections(stage4_report_root: ET.Element) -> None:
    required = {"DatasetLayout", "Captioning", "Deduplication", "Training", "MCPPlans"}
    actual = {child.tag for child in stage4_report_root}
    missing = required - actual
    assert not missing, f"Stage4レポートに欠落セクションがあります: {missing}"


def test_stage4_report_details(stage4_report_root: ET.Element) -> None:
    layout = stage4_report_root.find("DatasetLayout")
    assert layout is not None
    folders = {node.get("name") for node in layout.findall("Folder")}
    assert {"images", "captions", "splits", "reports"}.issubset(folders)

    training = stage4_report_root.find("Training")
    assert training is not None
    sample = training.find("Local")
    assert sample is not None and sample.find("Command") is not None
    cloud = training.find("Cloud")
    assert cloud is not None and cloud.find("Strategy") is not None


def test_caption_script_exists() -> None:
    script = SCRIPTS_DIR / "generate_captions.py"
    assert script.exists(), "キャプション生成スクリプトが存在しません"
    content = script.read_text(encoding="utf-8")
    for snippet in ["onnx", "input", "output", "threshold", "write_text"]:
        assert snippet in content, f"キャプションスクリプトに '{snippet}' が含まれていません"


def test_dedup_script_exists() -> None:
    script = SCRIPTS_DIR / "dedup_images.py"
    assert script.exists(), "重複検出スクリプトが存在しません"
    body = script.read_text(encoding="utf-8")
    for snippet in ["imagededup", "method", "max_distance", "json.dumps"]:
        assert snippet in body, f"重複スクリプトに '{snippet}' が不足しています"


def test_train_script_exists() -> None:
    script = SCRIPTS_DIR / "run_lora_training.sh"
    assert script.exists(), "LoRA学習シェルスクリプトが存在しません"
    text = script.read_text(encoding="utf-8")
    required = [
        "python train_network.py",
        "--train_data_dir",
        "--caption_extension",
        "--output_dir",
        "--network_module",
        "--learning_rate",
        "--max_train_steps",
    ]
    for snippet in required:
        assert snippet in text, f"学習スクリプトに '{snippet}' が不足"


def test_quality_report_template_exists() -> None:
    template = DATASET_TEMPLATE / "reports" / "quality_report.md"
    assert template.exists(), "品質レポートテンプレートが存在しません"
    assert "## 重複" in template.read_text(encoding="utf-8")
