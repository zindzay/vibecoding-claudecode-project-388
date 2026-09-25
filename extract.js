// Извлекает цену товара со страницы Ozon.
// Запуск: javascript_tool на открытой странице товара, содержимое файла целиком.
// Возвращает JSON-строку { regular_price, sale_price, has_credit, status }.
await new Promise(r => setTimeout(r, 4000)); // дать странице догрузиться (заодно пауза между товарами)

const norm = s => (s ? s.replace(/\s+/g, '').replace(/[^\d₽]/g, '') : null);
const isPrice = el => el.children.length === 0 && /₽/.test(el.textContent);
const result = { regular_price: null, sale_price: null, has_credit: false, status: 'ok' };

const widget = document.querySelector('[data-widget="webPrice"]');
const outOfStock = !widget || /Товар закончился/.test(document.body.innerText.slice(0, 2000));

if (outOfStock) {
  result.status = 'out_of_stock';
} else {
  // Цена, ближайшая к подписи: поднимаемся от подписи вверх, пока рядом не найдётся span с ₽
  const priceByLabel = label => {
    const labelEl = [...widget.querySelectorAll('span')].find(s => s.textContent.trim() === label);
    for (let n = labelEl; n && n !== widget; n = n.parentElement) {
      const price = [...n.parentElement.querySelectorAll('span')].find(isPrice);
      if (price) return price.textContent;
    }
    return null;
  };

  const sale = priceByLabel('С банками');
  const regular = priceByLabel('С другими банками');

  if (regular) {
    result.regular_price = norm(regular);
    result.sale_price = norm(sale);
  } else {
    // Нет разделения на банки: первая цена в webPrice — обычная, скидки нет.
    // Зачёркнутые старые цены идут после неё и игнорируются.
    const first = [...widget.querySelectorAll('span')].find(isPrice);
    result.regular_price = norm(first && first.textContent);
  }

  const installment = document.querySelector('[data-widget="webInstallmentPurchase"]');
  result.has_credit = !!installment && installment.innerText.includes('Оплатить позже');
}

JSON.stringify(result);
