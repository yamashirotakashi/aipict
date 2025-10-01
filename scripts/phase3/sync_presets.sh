#!/usr/bin/env bash
set -euo pipefail

# ComfyUIプリセットを標準ディレクトリへ同期し、レジストリ整合性を確保する。
ROOT="$(cd "$(dirname "$0")/.." && pwd)/.."
PRESET_DIR="$ROOT/presets/comfyui"
REGISTRY="$ROOT/config/phase3/preset_registry.json"
TARGET="/opt/ai/ComfyUI/presets"

if [[ ! -f "$REGISTRY" ]]; then
  echo "preset_registry.json が見つかりません" >&2
  exit 1
fi

mkdir -p "$TARGET"

# jqがあれば正規化、なければPythonで代替
if command -v jq >/dev/null 2>&1; then
  mapfile -t files < <(jq -r '.presets[].file' "$REGISTRY")
else
  mapfile -t files < <(python - <<'PY'
import json
import sys
from pathlib import Path
registry = Path(sys.argv[1])
data = json.loads(registry.read_text(encoding='utf-8'))
for item in data['presets']:
    print(item['file'])
PY "$REGISTRY")
fi

for file in "${files[@]}"; do
  if [[ ! -f "$PRESET_DIR/$file" ]]; then
    echo "プリセットファイルが存在しません: $file" >&2
    exit 2
  fi
  rsync -a "$PRESET_DIR/$file" "$TARGET/$file"
  echo "synced: $file"

done

echo "preset_registry.json に基づく同期が完了しました"
