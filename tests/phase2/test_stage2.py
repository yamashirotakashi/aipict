import json
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_DIR = PROJECT_ROOT / "scripts" / "phase2"


@pytest.fixture(scope="module")
def comfy_installer() -> Path:
    return SCRIPTS_DIR / "install_comfyui.sh"


@pytest.fixture(scope="module")
def sdnext_installer() -> Path:
    return SCRIPTS_DIR / "install_sdnext.sh"


@pytest.fixture(scope="module")
def invoke_installer() -> Path:
    return SCRIPTS_DIR / "install_invokeai.sh"


@pytest.fixture(scope="module")
def shared_venv_script() -> Path:
    return SCRIPTS_DIR / "setup_shared_venv.sh"


@pytest.fixture(scope="module")
def ports_config() -> Path:
    return PROJECT_ROOT / "config" / "phase2" / "service_ports.json"


@pytest.fixture(scope="module")
def stage2_report() -> ET.Element:
    report_path = PROJECT_ROOT / "docs" / "xml" / "stage2-report.xml"
    assert report_path.exists(), "Stage2レポートが存在しません"
    tree = ET.parse(report_path)
    root = tree.getroot()
    assert root.tag == "Stage2Report", "Stage2レポートのルートタグが不正です"
    return root


def test_shared_venv_script(shared_venv_script: Path) -> None:
    assert shared_venv_script.exists(), "共有venvセットアップスクリプトが存在しません"
    content = shared_venv_script.read_text(encoding="utf-8")
    snippets = [
        "python3 -m venv /opt/ai/venvs/base",
        "source /opt/ai/venvs/base/bin/activate",
        "pip install --upgrade pip",
        "pip install -r requirements_phase2_base.txt",
    ]
    for snippet in snippets:
        assert snippet in content, f"共有venvスクリプトに '{snippet}' が含まれていません"


def test_comfyui_installer(comfy_installer: Path) -> None:
    assert comfy_installer.exists(), "ComfyUIインストールスクリプトがありません"
    content = comfy_installer.read_text(encoding="utf-8")
    expected = [
        "git clone https://github.com/comfyanonymous/ComfyUI.git",
        "pip install -r requirements.txt",
        "python main.py --listen 0.0.0.0 --port 8188",
    ]
    for snippet in expected:
        assert snippet in content, f"ComfyUIスクリプトに '{snippet}' が不足しています"


def test_sdnext_installer(sdnext_installer: Path) -> None:
    assert sdnext_installer.exists(), "SD.Nextインストールスクリプトがありません"
    content = sdnext_installer.read_text(encoding="utf-8")
    expected = [
        "git clone https://github.com/vladmandic/automatic.git sdnext",
        "python -m pip install -r requirements.txt",
        "python launch.py --listen 0.0.0.0 --port 7860 --enable-insecure-extension-access --no-half",
    ]
    for snippet in expected:
        assert snippet in content, f"SD.Nextスクリプトに '{snippet}' が不足しています"


def test_invokeai_installer(invoke_installer: Path) -> None:
    assert invoke_installer.exists(), "InvokeAIインストールスクリプトがありません"
    content = invoke_installer.read_text(encoding="utf-8")
    expected = [
        "pip install invokeai",
        "invokeai-configure",
        "invokeai --web --host 0.0.0.0 --port 9090",
    ]
    for snippet in expected:
        assert snippet in content, f"InvokeAIスクリプトに '{snippet}' が不足しています"


def test_ports_config(ports_config: Path) -> None:
    assert ports_config.exists(), "ポート設定ファイルが存在しません"
    data = json.loads(ports_config.read_text(encoding="utf-8"))
    assert data["ComfyUI"] == 8188
    assert data["SDNext"] == 7860
    assert data["InvokeAI"] == 9090


def test_stage2_report_structure(stage2_report: ET.Element) -> None:
    required = {"Summary", "VenvStrategy", "PortAssignments", "ModelDirectories", "MCPPlans"}
    actual = {child.tag for child in stage2_report}
    missing = required - actual
    assert not missing, f"Stage2レポートに {missing} がありません"


def test_stage2_report_details(stage2_report: ET.Element) -> None:
    venv = stage2_report.find("VenvStrategy")
    assert venv is not None
    assert venv.find("Shared") is not None
    assert venv.find("PerProject") is not None

    ports = stage2_report.find("PortAssignments")
    assert ports is not None
    expected_ports = {"ComfyUI": "8188", "SDNext": "7860", "InvokeAI": "9090"}
    for elem in ports.findall("Service"):
        name = elem.get("name")
        value = elem.get("port")
        assert expected_ports.get(name) == value, f"{name} のポートが想定と異なります"

    models = stage2_report.find("ModelDirectories")
    assert models is not None
    required_dirs = {"checkpoints", "loras", "vae"}
    for entry in models.findall("Entry"):
        required_dirs.discard(entry.get("type"))
    assert not required_dirs, f"モデルディレクトリで不足: {required_dirs}"
