#!/usr/bin/env bash
set -euo pipefail

# ComfyUI installer for Phase2
BASE_DIR="/opt/ai"
REPO_DIR="$BASE_DIR/ComfyUI"
VENV="/opt/ai/venvs/base"

if [[ ! -d "$VENV" ]]; then
  echo "共有venvが存在しません。setup_shared_venv.sh を先に実行してください。" >&2
  exit 1
fi

mkdir -p "$BASE_DIR"
cd "$BASE_DIR"

if [[ ! -d "$REPO_DIR" ]]; then
  git clone https://github.com/comfyanonymous/ComfyUI.git
fi

cd "$REPO_DIR"
source "$VENV/bin/activate"

pip install -r requirements.txt

cat <<'LAUNCH' > "$BASE_DIR/run-comfyui.sh"
#!/usr/bin/env bash
set -euo pipefail
source /opt/ai/venvs/base/bin/activate
cd /opt/ai/ComfyUI
python main.py --listen 0.0.0.0 --port 8188 "$@"
LAUNCH
chmod +x "$BASE_DIR/run-comfyui.sh"

echo "ComfyUI ready. launch via $BASE_DIR/run-comfyui.sh"
