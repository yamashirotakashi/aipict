#!/usr/bin/env bash
set -euo pipefail

# Phase 1: WSL + AMD ROCm 構築手順スクリプト
# 仕様書駆動・TDD観点から、必須コマンドとログファイル配置を定義する。

if [[ "${EUID}" -eq 0 ]]; then
  echo "このスクリプトは通常ユーザで実行し、sudoが必要な部分のみ権限昇格します" >&2
fi

LOG_DIR="${AI_HOME:-/opt/ai}/logs/phase1"
mkdir -p "$LOG_DIR"
CHECKLIST_LOG="$LOG_DIR/wsl_rocm_setup_$(date +%Y%m%d_%H%M%S).log"

{
  echo "[Phase1] WSL + ROCm setup started: $(date --iso-8601=seconds)"

  echo "[Windows] 開発者モード/WSL有効化 (手動確認)"
  echo "PowerShell(管理者)で以下を実行:" 
  echo "  wsl --install -d Ubuntu-24.04"

  echo "[Windows] 最新WSLへ更新"
  echo "  wsl --update"

  echo "[WSL] 主要パッケージの導入"
  echo "  sudo mkdir -p /opt/ai && sudo chown -R $USER:$USER /opt/ai"
  echo "  sudo apt update"
  echo "  sudo apt install -y git wget curl build-essential python3-venv python3-pip python3-dev"

  echo "[WSL] Python仮想環境(ROCm)の構築"
  echo "  python3 -m venv /opt/ai/venvs/rocm"
  echo "  source /opt/ai/venvs/rocm/bin/activate"
  echo "  python -m pip install --upgrade pip wheel setuptools"
  echo "  pip install --index-url https://download.pytorch.org/whl/rocm6.0 torch torchvision torchaudio --extra-index-url https://pypi.org/simple"

  echo "[Verification] torch + ROCm デバイス検証"
} | tee "$CHECKLIST_LOG"

python - <<'PY' | tee "$LOG_DIR/torch_device_check.log"
import torch
print("torch:", torch.__version__)
print("is_hip_available:", torch.version.hip is not None)
print("cuda.is_available:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("device_name:", torch.cuda.get_device_name(0))
else:
    print("device_name:", "N/A")
PY

{
  echo "[Memo] 落とし穴をdocs/xml/stage1-report.xmlに追記する"
  echo "[Phase1] setup completed"
} | tee -a "$CHECKLIST_LOG"
