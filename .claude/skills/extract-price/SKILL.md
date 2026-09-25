---
name: "extract-price"
description: "Извлекает цену товара Ozon по ссылке на карточку: обычную цену, цену со скидкой по карте банка и наличие рассрочки. Используй, когда нужно узнать текущую цену одного товара Ozon по URL (в том числе из скилла tracker)."
---

# Extract price

## Вход и выход

Вход: URL карточки товара Ozon, например
`https://www.ozon.ru/product/karta-pamyati-512gb-microsd-sandisk-nintendo-switch-sdsqxao-512g-gnczn-820770107/`

Выход: JSON

```json
{
  "url": "https://www.ozon.ru/product/...-820770107/",
  "regular_price": "17131₽",
  "sale_price": "15417₽",
  "has_credit": true,
  "status": "ok"
}
```

- `regular_price` — обычная цена (подпись «С другими банками»), `null` если не найдена
- `sale_price` — цена со скидкой (подпись «С банками»), `null` если скидки нет
- `has_credit` — `true`, если есть «Оплатить позже», иначе `false`
- `status` — `"ok"` или `"out_of_stock"`

Формат цены: пробелы убраны, символ ₽ оставлен («17 131 ₽» → «17131₽»).

## Алгоритм

1. Открой URL в браузере (Claude in Chrome). Обычный WebFetch не используй: Ozon блокирует его антиботом и robots.txt
2. Выполни на странице скрипт `scripts/extract.js` (рядом с этим файлом) через `javascript_tool`, передав содержимое файла целиком. Скрипт сам ждёт догрузки страницы и возвращает JSON в формате выше
3. Если скрипт вернул ошибку или странный результат — открой страницу через `get_page_text` и проверь вручную по правилам ниже

## Правила разбора (их реализует скрипт)

- Цены берутся только из виджета `webPrice`
  - крупная цена с подписью «С банками» — `sale_price`
  - цена с подписью «С другими банками» — `regular_price`
- Если разделения на банки нет и в `webPrice` одна цена — это `regular_price`, а `sale_price` = `null`
- Зачёркнутую старую цену (она идёт в `webPrice` после актуальных, например «114 407 ₽») игнорировать
- Цену из виджета `webBestSeller` («Есть дешевле» — цена другого продавца) игнорировать
- `has_credit` ищется только внутри виджета `webInstallmentPurchase` по тексту «Оплатить позже»
- Товар закончился: Ozon показывает «Товар закончился» или перекидывает на страницу поиска (виджета `webPrice` нет). Тогда вернуть `regular_price: null`, `sale_price: null`, `has_credit: false`, `status: "out_of_stock"`
- CSS-классы Ozon — сгенерированные хэши, которые часто меняются. Ориентируйся на `data-widget` и тексты подписей, а не на имена классов

## Пример разметки webPrice (сокращённо)

```html
<div data-widget="webPrice">
  <button>
    <span class="tsHeadline600Large">15 417 ₽</span>
    <span>С банками</span>
  </button>
  <div>
    <span class="tsHeadline500Medium">17 131 ₽</span>
    <span>С другими банками</span>
  </div>
</div>
<div data-widget="webInstallmentPurchase">
  <span>Оплатить позже</span>
</div>
```
