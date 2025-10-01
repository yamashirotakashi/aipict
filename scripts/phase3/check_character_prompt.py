#!/usr/bin/env python3
"""キャラクター用プロンプトがタグ辞書に準拠しているか検証するスクリプト。"""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TAGS_PATH = ROOT / "config" / "phase3" / "character_tags.json"


def load_tags() -> dict:
    if not TAGS_PATH.exists():
        raise FileNotFoundError(f"タグ辞書が存在しません: {TAGS_PATH}")
    return json.loads(TAGS_PATH.read_text(encoding="utf-8"))


def validate_prompt(character_id: str, prompt: str) -> int:
    tags = load_tags()["characters"]
    if character_id not in tags:
        print(f"✖ 未登録キャラクター: {character_id}", file=sys.stderr)
        return 1

    record = tags[character_id]
    prefix = record["prompt_prefix"]
    missing: list[str] = []
    if prefix not in prompt:
        missing.append(f"prompt_prefix '{prefix}'")

    attributes = record.get("attributes", {})
    for key, value in attributes.items():
        if value not in prompt:
            missing.append(f"{key}:{value}")

    if missing:
        print("✖ プロンプトに不足タグ: " + ", ".join(missing), file=sys.stderr)
        return 2

    print("✓ プロンプトはキャラクター辞書と整合しています")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description="キャラクタープロンプト検証")
    parser.add_argument("character_id", help="例: char:Shirayuki_Aoi")
    parser.add_argument("prompt", help="検証するプロンプト全文")
    args = parser.parse_args()

    exit_code = validate_prompt(args.character_id, args.prompt)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
