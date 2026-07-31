# Режимы выдачи SemCode v0.2

## Только промпт

```text
... →prompt
```

## Только Semantic IR

```text
... →json
```

## Промпт и JSON

```text
... →prompt+json
```

## Сжатый запрос

```text
... →codec dict:FM-0.2
```

## API payload

```text
... →api target:openai-api
```

## Прямой результат

```text
... →do
```

`→do` означает, что Autocoder не только составляет промпт, но маршрутизирует задачу исполнителю, если такой исполнитель подключён и действие разрешено.
