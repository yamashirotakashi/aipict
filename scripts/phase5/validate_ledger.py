#!/usr/bin/env python3
"""データ台帳CSVを検証し、欠落や不正値を報告するユーティリティ。"""

import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RULES_PATH = ROOT / "config" / "phase5" / "ledger_rules.json"
LEDGER_DEFAULT = ROOT / "config" / "phase4" / "dataset_ledger.csv"


class LedgerValidationError(Exception):
    """台帳検証例外"""


def load_rules() -> dict:
    return json.loads(RULES_PATH.read_text(encoding="utf-8"))


def validate_row(row: dict, rules: dict, line_no: int) -> list[str]:
    errors: list[str] = []
    required = rules["required_columns"]
    validators = rules.get("validators", {})

    for column in required:
        value = (row.get(column) or "").strip()
        if not value:
            errors.append(f"missing required column '{column}' at line {line_no}")
            continue
        allowed = validators.get(column)
        if allowed and value.lower() not in allowed:
            errors.append(f"invalid value '{value}' for column '{column}' at line {line_no}")
    return errors


def validate_ledger(path: Path, rules: dict) -> int:
    if not path.exists():
        raise LedgerValidationError(f"ledger file not found: {path}")

    with path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        missing_columns = [col for col in rules["required_columns"] if col not in reader.fieldnames]
        if missing_columns:
            raise LedgerValidationError(f"header missing columns: {missing_columns}")

        violations: list[str] = []
        for idx, row in enumerate(reader, start=2):
            violations.extend(validate_row(row, rules, idx))

    if violations:
        for message in violations:
            print(f"ERROR: {message}", file=sys.stderr)
        return 1

    print("Ledger validation passed.")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description="データ台帳検証")
    parser.add_argument("--ledger", default=str(LEDGER_DEFAULT))
    args = parser.parse_args()

    rules = load_rules()
    exit_code = validate_ledger(Path(args.ledger), rules)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
