#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)/.."
PLAYBOOK_JSON="$ROOT/config/phase5/playbook.json"

if [[ ! -f "$PLAYBOOK_JSON" ]]; then
  echo "playbook.json が見つかりません" >&2
  exit 1
fi

# MCP連携エージェントを起動してTODO化
codex run --agent Serena --task "Stage5 PlaybookをDAG化し、collect→normalize→caption→dedup→splitの成功条件を付与"
codex run --agent Cipher --task "dataset_ledger.csvのライセンス/個人情報カラムをレビューし欠落を報告"
codex run --agent Zen --task "品質ゲート失敗時の復旧フローをIf-Then形式で提示"

# 実行テンプレート
pushd "$ROOT" >/dev/null
python scripts/phase4/generate_captions.py
python scripts/phase4/dedup_images.py
python scripts/phase5/validate_ledger.py --ledger config/phase4/dataset_ledger.csv
popd >/dev/null

# TODOジェネレータで残タスクを整形
python "$ROOT/scripts/phase5/generate_todo.py" --playbook "$PLAYBOOK_JSON"
