#!/usr/bin/env bash
set -euo pipefail

# Phase 1: WSL + DirectML 構築手順スクリプト
# 仕様書駆動・TDD観点から、DirectMLを利用したPyTorch環境構築の必須コマンドを記録する。

if [[ "${EUID}" -eq 0 ]]; then
  echo "このスクリプトは通常ユーザで実行し、必要箇所のみsudoを使用します" >&2
fi

LOG_DIR="${AI_HOME:-/opt/ai}/logs/phase1"
mkdir -p "$LOG_DIR"
CHECKLIST_LOG="$LOG_DIR/wsl_directml_setup_$(date +%Y%m%d_%H%M%S).log"

{
  echo "[Phase1] WSL + DirectML setup started: $(date --iso-8601=seconds)"

  echo "[Windows] 開発者モード/WSL有効化 (手動確認)"
  echo "PowerShell(管理者)で以下を実行:"
  echo "  wsl --install -d Ubuntu-24.04"

  echo "[Windows] 最新WSLへ更新"
  echo "  wsl --update"

  echo "[WSL] 主要パッケージの導入"
  echo "  sudo mkdir -p /opt/ai && sudo chown -R $USER:$USER /opt/ai"
  echo "  sudo apt update"
  echo "  sudo apt install -y git wget curl build-essential python3-venv python3-pip python3-dev"

  echo "[WSL] Python仮想環境(DirectML)の構築"
  echo "  python3 -m venv /opt/ai/venvs/directml"
  echo "  source /opt/ai/venvs/directml/bin/activate"
  echo "  python -m pip install --upgrade pip wheel setuptools"
  echo "  pip install torch-directml"
  echo "  pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu121"

  echo "[Verification] torch-directml デバイス検証"
} | tee "$CHECKLIST_LOG"

python - <<'PY' | tee "$LOG_DIR/torch_directml_check.log"
import torch
import torch_directml

print("torch:", torch.__version__)
device = torch_directml.device()
print("directml.device:", device)
tensor = torch.randn(1, device=device)
print("tensor_device:", tensor.device)
PY

{
  echo "[Memo] 落とし穴をdocs/xml/stage1-report.xmlに追記する"
  echo "[Phase1] setup completed"
} | tee -a "$CHECKLIST_LOG"
