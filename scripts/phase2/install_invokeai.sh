#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="/opt/ai"
CONFIG_DIR="$HOME/.invokeai"
VENV="/opt/ai/venvs/base"

if [[ ! -d "$VENV" ]]; then
  echo "共有venvが存在しません。setup_shared_venv.sh を先に実行してください。" >&2
  exit 1
fi

mkdir -p "$BASE_DIR"
source "$VENV/bin/activate"

pip install invokeai

cat <<'LAUNCH' > "$BASE_DIR/run-invokeai.sh"
#!/usr/bin/env bash
set -euo pipefail
source /opt/ai/venvs/base/bin/activate
invokeai --web --host 0.0.0.0 --port 9090 "$@"
LAUNCH
chmod +x "$BASE_DIR/run-invokeai.sh"

echo "InvokeAI configure step"
invokeai-configure --yes --root $CONFIG_DIR

echo "InvokeAI ready. launch via $BASE_DIR/run-invokeai.sh"
