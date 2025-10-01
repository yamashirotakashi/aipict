#!/usr/bin/env bash
set -euo pipefail

# LoRA学習テンプレートスクリプト
ROOT="$(cd "$(dirname "$0")/.." && pwd)/.."
DATASET_ROOT="$ROOT/datasets/lora_template"
OUTPUT_DIR="$ROOT/outputs/lora"
MODEL_PATH="/opt/ai/models/checkpoints/sdxl_base.safetensors"
VENV="/opt/ai/venvs/base"

function usage() {
  cat <<USAGE
Usage: $0 [--dataset PATH] [--remote]
  --dataset PATH    学習データセットのルート (default: $DATASET_ROOT)
  --remote          リモート実行用設定を有効化 (rsync前提)
USAGE
}

DATASET="$DATASET_ROOT"
REMOTE=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dataset)
      shift
      DATASET="$1"
      ;;
    --remote)
      REMOTE=true
      ;;
    --help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage
      exit 1
      ;;
  esac
  shift
done

if [[ ! -d "$VENV" ]]; then
  echo "venvが存在しません: $VENV" >&2
  exit 1
fi

source "$VENV/bin/activate"
mkdir -p "$OUTPUT_DIR"

python train_network.py \
  --pretrained_model_name_or_path "$MODEL_PATH" \
  --train_data_dir "$DATASET/images" \
  --caption_extension ".txt" \
  --resolution "1024,1024" \
  --output_dir "$OUTPUT_DIR" \
  --network_module "networks.lora" \
  --network_dim 16 --network_alpha 16 \
  --learning_rate 1e-4 --optimizer_type "adamw8bit" \
  --max_train_steps 2000 --lr_scheduler "cosine" \
  --mixed_precision "fp16" --save_every_n_steps 500 --save_model_as "safetensors"

deactivate

echo "LoRA training completed (dataset: $DATASET, remote=$REMOTE)"
