# Semantic IR Specification v0.2

## 1. Назначение

Semantic IR — каноническое промежуточное представление намерения пользователя. Оно разделяет вероятностное понимание пользовательского языка и последующее формирование промпта или сжатого кода.

```text
raw user input → Autocoder → Semantic IR → Compiler / Codec / Adapter
```

После создания IR последующие компоненты не должны повторно угадывать исходное намерение без явного указания.

## 2. Основные свойства

Semantic IR должен быть:

- типизированным;
- валидируемым JSON Schema;
- переносимым между моделями;
- независимым от пользовательских опечаток;
- независимым от конкретного синтаксиса промпта;
- версионируемым;
- пригодным для аудита и semantic diff.

## 3. Минимальная структура

```json
{
  "ir_version": "0.2",
  "request_id": "req-...",
  "raw_input": "...",
  "normalized_code": "...",
  "intent": {
    "action": "create",
    "object": "financial_model"
  },
  "target": {
    "model": "Claude",
    "environment": "Excel"
  },
  "sources": [],
  "requirements": {},
  "constraints": [],
  "memory": {},
  "output": {},
  "interpretation": {},
  "provenance": []
}
```

## 4. Интерпретация и уверенность

Уверенность хранится не только глобально, но и по отдельным полям:

```json
{
  "interpretation": {
    "overall_confidence": 0.91,
    "level": "H",
    "field_confidence": {
      "intent.action": 0.99,
      "target.model": 0.97,
      "requirements.period_months": 0.42
    },
    "assumptions": [],
    "critical_ambiguities": []
  }
}
```

Правила:

- `H`: итоговое намерение можно выполнить без уточнения;
- `M`: допустимы прозрачные допущения;
- `L`: требуется один вопрос по критической развилке.

## 5. Источники и происхождение

Каждое существенное значение может иметь происхождение:

```json
{
  "path": "requirements.scenario_count",
  "value": 3,
  "origin": "explicit_user_input",
  "evidence": "три сценария"
}
```

Допустимые источники:

- `explicit_user_input`;
- `personal_language_memory`;
- `project_memory`;
- `current_document`;
- `reasonable_default`;
- `target_adapter`.

Приоритет:

```text
explicit current input > current source materials > task memory > project memory > profile memory > default
```

## 6. Изменение IR

Любое исправление пользователя должно применяться как patch к IR, а не как полная повторная интерпретация, если пользователь не просит пересобрать смысл.

Пример:

```text
ERR: target не Claude, а GPT
```

Patch:

```json
{
  "op": "replace",
  "path": "/target/model",
  "value": "GPT"
}
```

После подтверждённого исправления Autocoder может обновить персональный словарь.
