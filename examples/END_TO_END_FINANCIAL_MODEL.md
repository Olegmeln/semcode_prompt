# Сквозной пример: пользователь → Autocoder → IR → Codec → Claude в Excel

## 1. Ввод пользователя

```text
ФМtask ответ Cl eexc new* in докс+ три сценария не выдумывать
```

## 2. Нормализованный SemCode

```text
FMtask→P Cl@Excel new*FM src:docs+ scn:3 !invent mem+ q:critical →prompt
```

## 3. Semantic IR

```json
{
  "ir_version": "0.2",
  "request_id": "req-fm-example-001",
  "raw_input": "ФМtask ответ Cl eexc new* in докс+ три сценария не выдумывать",
  "normalized_code": "FMtask→P Cl@Excel new*FM src:docs+ scn:3 !invent mem+ q:critical →prompt",
  "domain": "financial_modeling",
  "intent": {
    "action": "create",
    "object": "financial_model",
    "intensity": 1
  },
  "target": {
    "model": "Claude",
    "environment": "Excel",
    "adapter": "claude-excel"
  },
  "sources": [
    {
      "kind": "attached_documents",
      "reference": null,
      "cardinality": "multiple",
      "priority": 1
    }
  ],
  "requirements": {
    "build_from_scratch": true,
    "scenario_count": 3,
    "extract_assumptions": true,
    "use_excel_formulas": true,
    "create_validation_checks": true
  },
  "constraints": [
    {"type": "do_not_invent_data"}
  ],
  "memory": {
    "read": true,
    "write": false,
    "scopes": ["profile", "project", "personal_language"]
  },
  "output": {
    "kind": "compiled_prompt",
    "format": "text",
    "language": "ru"
  },
  "interpretation": {
    "overall_confidence": 0.96,
    "level": "H",
    "field_confidence": {
      "target.model": 0.97,
      "target.environment": 0.97,
      "requirements.scenario_count": 1.0
    },
    "assumptions": [
      "Новая модель создаётся с нуля",
      "Структура листов выбирается по стандарту финансового моделирования"
    ],
    "critical_ambiguities": [],
    "question": null
  },
  "provenance": [
    {
      "path": "target.model",
      "value": "Claude",
      "origin": "personal_language_memory",
      "evidence": "Cl eexc"
    },
    {
      "path": "requirements.scenario_count",
      "value": 3,
      "origin": "explicit_user_input",
      "evidence": "три сценария"
    }
  ]
}
```

## 4. Полный промпт

```text
Ты — финансовый аналитик и архитектор финансовых моделей, работающий непосредственно в Excel.

На основании всех приложенных документов создай новую финансовую модель с нуля. Сначала изучи источники и извлеки исходные предпосылки, периоды, валюты, тарифы, объёмы, доходы, прямые и постоянные расходы, финансирование и иные параметры, влияющие на расчёты.

Построй прозрачную и изменяемую книгу Excel. Отдели исходные данные и ручные предпосылки от расчётных формул. Используй формулы Excel, а не статические расчётные значения.

Создай три сценария: консервативный, базовый и оптимистичный. Все сценарные параметры должны изменяться из единого блока предпосылок.

Не выдумывай отсутствующие данные. Если обязательное значение отсутствует, создай обозначенную ячейку для ввода и включи вопрос в отдельный список. При конфликте между документами зафиксируй оба значения, источники и влияние выбора на модель.

Минимальная структура книги:
- Readme;
- Sources;
- Assumptions;
- Revenue;
- Costs;
- P&L;
- Cash Flow;
- Scenarios;
- Checks;
- Questions.

Перед завершением проверь формулы, согласованность периодов, полноту переноса исходных значений и чувствительность результатов к изменению предпосылок.
```

## 5. Codec-представление

```text
@D:FM-0.2;ir:0.2 FM:new t:Cl@X src:d+ scn:3 !inv →P
```

Codec используется только если целевая система имеет словарь `FM-0.2`. Иначе передаётся полный промпт.
