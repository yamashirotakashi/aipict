#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="/opt/ai"
REPO_DIR="$BASE_DIR/sdnext"
VENV="/opt/ai/venvs/base"

if [[ ! -d "$VENV" ]]; then
  echo "共有venvが存在しません。setup_shared_venv.sh を先に実行してください。" >&2
  exit 1
fi

mkdir -p "$BASE_DIR"
cd "$BASE_DIR"

if [[ ! -d "$REPO_DIR" ]]; then
  git clone https://github.com/vladmandic/automatic.git sdnext
fi

cd "$REPO_DIR"
source "$VENV/bin/activate"

python -m pip install -r requirements.txt

cat <<'LAUNCH' > "$BASE_DIR/run-sdnext.sh"
#!/usr/bin/env bash
set -euo pipefail
source /opt/ai/venvs/base/bin/activate
cd /opt/ai/sdnext
python launch.py --listen 0.0.0.0 --port 7860 --enable-insecure-extension-access --no-half "$@"
LAUNCH
chmod +x "$BASE_DIR/run-sdnext.sh"

echo "SD.Next ready. launch via $BASE_DIR/run-sdnext.sh"
