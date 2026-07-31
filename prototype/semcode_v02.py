#!/usr/bin/env python3
"""Minimal SemCode v0.2 demonstration.

This is intentionally heuristic. It demonstrates the separation:
raw user idiolect -> Autocoder-like interpretation -> Semantic IR -> Codec.
It is not a production parser.
"""

from __future__ import annotations

import json
import re
import sys
import uuid
from dataclasses import dataclass, asdict
from typing import Any


@dataclass
class Interpretation:
    normalized_code: str
    ir: dict[str, Any]
    codec: str
    prompt: str


def interpret(raw: str) -> Interpretation:
    low = raw.lower()

    is_financial = any(x in low for x in ["фм", "fm", "фин. модел", "финансовая модел"])
    wants_claude_excel = any(x in low for x in ["cl eexc", "cl@x", "claude excel", "кл в экс"])
    create_new = "new*" in low or "с нуля" in low or "созд" in low
    has_docs = "докс+" in low or "docs+" in low or "приложенн" in low
    no_invent = "не выдум" in low or "!invent" in low or "!inv" in low

    scenario_count = None
    word_nums = {"один": 1, "два": 2, "три": 3, "четыре": 4, "пять": 5}
    for word, value in word_nums.items():
        if f"{word} сценар" in low:
            scenario_count = value
            break
    if scenario_count is None:
        m = re.search(r"(?:scn|сценар(?:ия|иев)?)[\s:=]*(\d+)", low)
        if m:
            scenario_count = int(m.group(1))

    if not is_financial:
        raise ValueError("Prototype currently supports the financial-model example only")

    target_model = "Claude" if wants_claude_excel else None
    target_env = "Excel" if wants_claude_excel else None
    confidence = 0.96 if wants_claude_excel and has_docs else 0.72
    level = "H" if confidence >= 0.85 else "M"

    normalized = ["FMtask→P"]
    if wants_claude_excel:
        normalized.append("Cl@Excel")
    if create_new:
        normalized.append("new*FM")
    if has_docs:
        normalized.append("src:docs+")
    if scenario_count:
        normalized.append(f"scn:{scenario_count}")
    if no_invent:
        normalized.append("!invent")
    normalized += ["mem+", "q:critical", "→prompt"]
    normalized_code = " ".join(normalized)

    constraints = []
    if no_invent:
        constraints.append({"type": "do_not_invent_data"})

    requirements: dict[str, Any] = {
        "build_from_scratch": create_new,
        "extract_assumptions": True,
        "use_excel_formulas": True,
        "create_validation_checks": True,
    }
    if scenario_count:
        requirements["scenario_count"] = scenario_count

    ir = {
        "ir_version": "0.2",
        "request_id": f"req-{uuid.uuid4().hex[:12]}",
        "raw_input": raw,
        "normalized_code": normalized_code,
        "domain": "financial_modeling",
        "intent": {"action": "create" if create_new else "build", "object": "financial_model", "intensity": 1},
        "target": {"model": target_model, "environment": target_env, "adapter": "claude-excel" if wants_claude_excel else "generic-llm"},
        "sources": [{"kind": "attached_documents", "reference": None, "cardinality": "multiple", "priority": 1}] if has_docs else [],
        "requirements": requirements,
        "constraints": constraints,
        "memory": {"read": True, "write": False, "scopes": ["personal_language", "project"]},
        "output": {"kind": "compiled_prompt", "format": "text", "language": "ru"},
        "interpretation": {
            "overall_confidence": confidence,
            "level": level,
            "field_confidence": {"target.model": 0.97 if target_model else 0.4},
            "assumptions": [],
            "critical_ambiguities": [] if target_model else ["target model is not explicitly resolved"],
            "question": None,
        },
        "provenance": [],
    }

    codec_parts = ["@D:FM-0.2;ir:0.2", "FM:new"]
    if wants_claude_excel:
        codec_parts.append("t:Cl@X")
    if has_docs:
        codec_parts.append("src:d+")
    if scenario_count:
        codec_parts.append(f"scn:{scenario_count}")
    if no_invent:
        codec_parts.append("!inv")
    codec_parts.append("→P")
    codec = " ".join(codec_parts)

    scn_text = f" Создай {scenario_count} сценария." if scenario_count else ""
    prompt = (
        "Ты — финансовый аналитик и архитектор финансовых моделей, работающий в Excel. "
        "На основании приложенных документов создай новую прозрачную финансовую модель с отдельными блоками "
        "исходных данных, предпосылок, выручки, расходов, P&L, Cash Flow и проверок. "
        "Используй формулы Excel и отделяй ручной ввод от расчётов."
        + scn_text
        + (" Не выдумывай отсутствующие данные; фиксируй их как вопросы или placeholders." if no_invent else "")
    )

    return Interpretation(normalized_code, ir, codec, prompt)


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python prototype/semcode_v02.py '<short command>'", file=sys.stderr)
        return 2
    raw = " ".join(sys.argv[1:])
    try:
        result = interpret(raw)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(result.normalized_code)
    print("\nSEMANTIC_IR:")
    print(json.dumps(result.ir, ensure_ascii=False, indent=2))
    print("\nCODEC:")
    print(result.codec)
    print("\nPROMPT:")
    print(result.prompt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
