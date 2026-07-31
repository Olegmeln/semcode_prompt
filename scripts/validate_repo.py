#!/usr/bin/env python3
from pathlib import Path
import json
import sys

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path):
    with path.open('r', encoding='utf-8') as f:
        return json.load(f)


def main() -> int:
    errors = []

    # Basic JSON parse
    for path in ROOT.rglob('*.json'):
        try:
            load_json(path)
        except Exception as exc:
            errors.append(f'{path.relative_to(ROOT)}: {exc}')

    # Basic YAML parse
    for path in list(ROOT.rglob('*.yaml')) + list(ROOT.rglob('*.yml')):
        try:
            with path.open('r', encoding='utf-8') as f:
                yaml.safe_load(f)
        except Exception as exc:
            errors.append(f'{path.relative_to(ROOT)}: {exc}')

    # Validate example personal language
    try:
        schema = load_json(ROOT / 'autocoder/schemas/personal-language.schema.json')
        instance = load_json(ROOT / 'autocoder/memory/personal-language.example.json')
        for err in Draft202012Validator(schema).iter_errors(instance):
            errors.append(f'personal-language.example.json: {err.message}')
    except Exception as exc:
        errors.append(f'personal language validation: {exc}')

    if errors:
        print('VALIDATION FAILED')
        for err in errors:
            print('-', err)
        return 1

    print('VALIDATION OK')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
