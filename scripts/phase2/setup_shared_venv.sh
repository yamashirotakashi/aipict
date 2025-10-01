#!/usr/bin/env bash
set -euo pipefail

# Phase2 shared venv setup script
# 仕様: /opt/ai/venvs/base を作成し、共通依存 requirements_phase2_base.txt を導入する。
# 各UI固有の追加依存は install_* スクリプトで個別に処理する。

VENV_PATH="/opt/ai/venvs/base"
# 実行コマンド例: python3 -m venv /opt/ai/venvs/base
REQ_FILE="$(dirname "$0")/../../requirements_phase2_base.txt"

if [[ ! -f "$REQ_FILE" ]]; then
  echo "requirements_phase2_base.txt が見つかりません" >&2
  exit 1
fi

python3 -m venv "$VENV_PATH"
# 指示: source /opt/ai/venvs/base/bin/activate
source "$VENV_PATH/bin/activate"

pip install --upgrade pip wheel setuptools
# 指示: pip install -r requirements_phase2_base.txt
pip install -r "$REQ_FILE"

deactivate

echo "[Phase2] shared venv configured at $VENV_PATH"
