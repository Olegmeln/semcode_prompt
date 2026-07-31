# SemCode v0.2 — Autocoder + Codec

SemCode — экспериментальная двухконтурная система для работы с короткими пользовательскими командами и промптами.

## Два независимых контура

### 1. SemCode Autocoder

Понимает индивидуальный язык пользователя, который постепенно формируется в диалоге:

```text
ФМtask ответ Cl eexc new* in докс+ три сценария не выдумывать
```

Autocoder использует контекст и память, восстанавливает намерение и переводит его в типизированное промежуточное представление — **Semantic IR**. После этого он формирует:

- полный качественный промпт;
- JSON или API payload;
- запрос, адаптированный под указанную модель;
- при необходимости — сжатую команду для Codec.

### 2. SemCode Codec

Получает уже определённое намерение в Semantic IR или готовом промпте и преобразует его в короткую воспроизводимую запись по версионированному словарю:

```text
@D:FM-0.2 FM:new t:Cl@X src:d+ scn:3 !inv out:xlsx
```

Codec не должен творчески угадывать значение известных токенов. Его задача — компактное кодирование, безопасная передача и однозначное декодирование.

## Общая архитектура

```text
user idiolect
    ↓
SemCode Autocoder
    ↓
Semantic IR
    ├──→ Prompt / JSON / API payload → target model
    └──→ SemCode Codec → compressed prompt + dictionary → target model
```

## Базовый принцип разграничения

| Компонент | Допускает вероятностное понимание | Обязан быть воспроизводимым |
|---|---:|---:|
| Autocoder | да | на уровне итогового IR |
| Semantic IR | нет | да |
| Codec | нет для известных токенов | да |
| Target adapter | ограниченно | да по формату |

## Пример

Пользовательская команда:

```text
ФМtask ответ Cl eexc new* in докс+ три сценария не выдумывать
```

Нормализованный SemCode:

```text
FMtask→P Cl@Excel new*FM src:docs+ scn:3 !invent mem+ q:critical →prompt
```

Semantic IR:

```json
{
  "ir_version": "0.2",
  "intent": {"action": "create", "object": "financial_model"},
  "target": {"model": "Claude", "environment": "Excel"},
  "sources": [{"kind": "attached_documents", "cardinality": "multiple"}],
  "requirements": {"scenario_count": 3},
  "constraints": [{"type": "do_not_invent_data"}],
  "output": {"kind": "compiled_prompt"}
}
```

Codec:

```text
@D:FM-0.2 FM:new t:Cl@X src:d+ scn:3 !inv →P
```

## Структура репозитория

```text
core/
  semantic-ir/       общая типизированная модель намерения
  routing/           правила выбора Autocoder / Codec / Hybrid

autocoder/
  spec/              спецификация вероятностного интерпретатора
  prompts/           системный промпт
  memory/            персональный язык и правила обучения
  schemas/           JSON-схема персонального словаря
  tests/             тесты интерпретации

codec/
  spec/              спецификация кодека и протокола передачи
  prompts/           декодер для целевой модели
  dictionaries/      версионированные словари
  schemas/           схема словаря
  tests/             тесты кодирования и декодирования

adapters/             профили целевых моделей и сред
examples/             сквозные примеры
prototype/            минимальный исполняемый прототип
legacy/v0.1/          сохранённая первая версия
```

## Быстрый эксперимент

```bash
python prototype/semcode_v02.py \
  "ФМtask ответ Cl eexc new* in докс+ три сценария не выдумывать"
```

Прототип показывает:

1. нормализованный код;
2. Semantic IR;
3. сжатую Codec-команду;
4. черновой полный промпт.

## Статус

`0.2-experimental` — архитектура разделена на Autocoder и Codec. Следующий этап: накопление подтверждённых пользовательских токенов, сравнение интерпретаций и расширение адаптеров моделей.
