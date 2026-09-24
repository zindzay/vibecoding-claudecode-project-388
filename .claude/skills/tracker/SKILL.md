---
name: "tracker"
description: "Проходит по списку URL и собирает таблицу цен"
---

# Tracker

## Quick start

Входные данные URL

- https://www.ozon.ru/product/karta-pamyati-512gb-microsd-sandisk-nintendo-switch-sdsqxao-512g-gnczn-820770107/?at=1pql1TmcJ_vrGhtMnSs6Pb-FtmUuTTAZ&sh=xJSuSCfhKw
- https://www.ozon.ru/product/karta-pamyati-128gb-microsd-sandisk-nintendo-switch-sdsqxao-128g-gnczn-272323160/?at=1pql1RsZJgJMU_BqdyPMMMQ6mLWxjgq2
- https://www.ozon.ru/product/lexar-microsd-express-card-dlya-nintendo-switch-2-1tb-2916614830/?at=1pul1OskPrQ0YzhGnWOLqBHnqfqMjmP5
- https://www.ozon.ru/product/karta-pamyati-sandisk-microsdxc-512-gb-dlya-nintendo-switch-100-90-mb-s-2583756233/?at=1pul1P0gLjKlR3WlJE2UYknXb7sw2q4b
- https://www.ozon.ru/product/microsd-express-card-dlya-nintendo-switch-2-1tb-5442521333/?at=1pul1ZRAaRxgadufKctX3usf4vKl6B6p
- https://www.ozon.ru/product/lexar-microsd-express-card-dlya-nintendo-switch-2-1tb-3415256585/?at=1pul1XTgPWZFL9ldfin5I6XQI03OJCTK
- https://www.ozon.ru/product/microsd-express-card-dlya-nintendo-switch-2-1tb-5684497053/?at=1pul1XDCz8Y0s_QXIbmrfRVz1z9bt8Pq
- https://www.ozon.ru/product/lexar-microsd-express-card-dlya-nintendo-switch-2-1tb-3289746466/?at=1pul1Y7aRaZVzIBNbJP6hX494d37YToD
- https://www.ozon.ru/product/l-exar-microsd-express-card-dlya-nintendo-switch-2-1tb-4785717093/?at=1pul1SUu4d8Tw7SxFQDMotK4sFiKaSBV

## Секреты
Перед запуском найди .env в подключённых папках пользователя,
только по имени файла, НЕ открывая и НЕ выводя его содержимое:
`find / -name ".env" -path "*mnt*" 2>/dev/null | head`
Затем запусти скрипт с найденным путём:
`SKILL_ENV_FILE=<путь> python3 send.py ...`

Никогда не делай cat/head/Read на .env и не цитируй ключи.
Если .env не найден, попроси пользователя положить его
в подключённую папку, а не вставлять ключ в чат.

Алгоритм

1. Не используй данные из контекста от прошлых запусков скила, выполняй все шаги с 0, по новой
2. Для каждого URL из списка ассистент вызывает уже готовый скилл extract-price, трекер переиспользует extract-price, а не дублирует его логику
3. Между запросами к разным URL делай паузу (несколько секунд), чтобы не словить антибот-блокировку Ozon при обходе списка
4. Получает объекты с ценами
5. Результат записывается в таблицу, одна строка на товар, в строке — URL и поля regular_price, sale_price, has_credit, таблица json
6. Получи список файлов из репозитория zindzay/tracker-data через GitHub MCP (mcp__github__* / mcp__claude_ai_GitHub__*), а не через прямой git clone
7. Прочитай последний по дате файл (YYYY-MM-DD.json), если файлов нет, то переходи к пункту 9
8. Сопоставь товары из новой таблицы с товарами из таблицы пункта 6, сопоставление делай по URL (а не по полям цены — они как раз то, что сравнивается)
9. Значимость изменения цены описана в файле KNOWLEDGE.md рядом с этим скиллом
10. Напиши в чат значимые изменения
11. После анализа полученную таблицу нужно загрузить в репозиторий zindzay/tracker-data через тот же GitHub MCP
12. Сформируй человеко-читаемый отчёт и отправь в чат используя скрипт send.py, если изменений нет — напиши в чат «Значимых изменений цен нет»

Формат файла: json
Название файла: YYYY-MM-DD.json
Пример записи в файле:
```json
[
  {
    "url": "https://www.ozon.ru/product/...",
    "regular_price": "17131₽",
    "sale_price": "15417₽",
    "has_credit": true
  },
  {
    "url": "https://www.ozon.ru/product/...",
    "regular_price": "27131₽",
    "sale_price": "18417₽",
    "has_credit": false
  }
]
```
