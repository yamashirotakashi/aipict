#!/usr/bin/env python3
"""PlaybookからTODOリストを生成し、Serena向けに整形する。"""

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PLAYBOOK = ROOT / "config" / "phase5" / "playbook.json"


def render_todo(playbook: dict, step_filter: str | None = None) -> str:
    steps = playbook.get("steps", [])
    lines: list[str] = []
    for step in steps:
        if step_filter and step.get("id") != step_filter:
            continue
        lines.append(f"- [{step['id']}] {step['description']} :: {step.get('command', 'N/A')}")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Playbook TODO生成")
    parser.add_argument("--playbook", default=str(DEFAULT_PLAYBOOK))
    parser.add_argument("--step", dest="step", default=None)
    args = parser.parse_args()

    playbook = json.loads(Path(args.playbook).read_text(encoding="utf-8"))
    todo_list = render_todo(playbook, args.step)
    print("Serena TODO list:\n" + todo_list)


if __name__ == "__main__":
    main()
