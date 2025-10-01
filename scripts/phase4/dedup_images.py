#!/usr/bin/env python3
"""imagededupを利用した重複画像検出テンプレート。"""

import argparse
import json
from pathlib import Path

from imagededup.methods import PHash, AHash, DHash

ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "config" / "phase4" / "dedup_config.json"


def load_config() -> dict:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def get_method(name: str):
    return {
        "phash": PHash,
        "ahash": AHash,
        "dhash": DHash,
    }[name.lower()]


def main() -> None:
    parser = argparse.ArgumentParser(description="画像重複検出")
    parser.add_argument("--config", default=str(CONFIG_PATH))
    args = parser.parse_args()

    config = load_config()
    image_dir = ROOT / "datasets" / "lora_template" / config["image_dir"]
    output_path = ROOT / "datasets" / "lora_template" / config["output"]
    output_path.parent.mkdir(parents=True, exist_ok=True)

    method_cls = get_method(config["method"])
    engine = method_cls()

    encodings = engine.encode_images(image_dir=image_dir)
    duplicates = engine.find_duplicates(
        encoding_map=encodings,
        max_distance_threshold=config["max_distance"]
    )

    output_path.write_text(
        json.dumps(duplicates, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    print(f"Duplicate report saved to {output_path}")


if __name__ == "__main__":
    main()
