#!/usr/bin/env python3
"""WD14/DeepDanbooruを用いたキャプション生成テンプレート。"""

import argparse
import json
import os
from pathlib import Path

import onnxruntime as ort
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "config" / "phase4" / "caption_config.json"


def load_config() -> dict:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def run_inference(image_path: Path, session: ort.InferenceSession) -> list[tuple[str, float]]:
    # 実運用ではモデルに合わせた前処理が必要。ここではテンプレとして疑似処理。
    # TODO: WD14の実装に合わせた入力/出力変換を追加する。
    return [("sample_tag", 0.9)]


def write_caption(output_dir: Path, image_path: Path, tags: list[tuple[str, float]], min_score: float) -> None:
    caption_path = output_dir / (image_path.stem + ".txt")
    selected = [tag for tag, score in tags if score >= min_score]
    caption_path.write_text(", ".join(selected), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="自動キャプション生成テンプレ")
    parser.add_argument("--config", default=str(CONFIG_PATH))
    parser.add_argument("--model", required=False, help="ONNXモデルへのパス")
    args = parser.parse_args()

    config = load_config()
    input_dir = ROOT / "datasets" / "lora_template" / config["input_dir"]
    output_dir = ROOT / "datasets" / "lora_template" / config["output_dir"]
    output_dir.mkdir(parents=True, exist_ok=True)

    session = None
    if args.model:
        session = ort.InferenceSession(args.model)

    threshold = config["thresholds"]["min_score"]

    for image_path in input_dir.glob("*.png"):
        tags = run_inference(image_path, session) if session else [("placeholder", 1.0)]
        write_caption(output_dir, image_path, tags, threshold)
        print(f"Generated caption for {image_path.name}")


if __name__ == "__main__":
    main()
