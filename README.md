# WebTransport и WebSocket

Сравнительный анализ технологий двунаправленной передачи данных в веб-приложениях:
модели доставки, время подключения, задержка сообщений, накладные расходы
и поведение при потерях пакетов.

| Режим | Транспорт | Доставка |
|---|---|---|
| WebSocket | TLS/TCP | Надёжная, упорядоченная |
| WebTransport streams | HTTP/3 поверх QUIC | Надёжная, порядок внутри потока |
| WebTransport datagrams | HTTP/3 поверх QUIC | Без гарантии доставки и порядка |

## Материалы

- [Область сравнения](docs/about.md)
- [WebSocket](docs/websocket.md) и [WebTransport](docs/webtransport.md)
- [Методика](docs/methodology.md) и [сценарии экспериментов](docs/scenarios.md)
- [Результаты и предварительные выводы](docs/results.md)
- [Ограничения](docs/limitations.md) и [источники](docs/references.md)

Материалы доступны на [сайте](https://asmat1k.github.io/pyweb/).

**Статус исследования:** опубликованы теоретическое сравнение и план экспериментов.
Реальные измерения не проводились. JavaScript-демо генерирует случайные результаты
для WebSocket, WT streams и WT datagrams и показывает их на главной странице.

## Запуск демо

Нужны Node.js 20+ и Python с зависимостями из `requirements.txt`.
JavaScript не использует внешних пакетов, `npm install` не требуется.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
npm run benchmark
npm start
```

Откройте <http://127.0.0.1:8000/pyweb/>. Таблицы загрузят результат CLI;
кнопка «Запустить демо» создаст новые случайные значения прямо в браузере.

```bash
npm test
python -m mkdocs build --strict
```

- `docs/assets/javascripts/benchmark.js` — функции-заглушки четырёх метрик.
- `scripts/benchmark.mjs` — CLI и сохранение JSON.
- `docs/assets/javascripts/demo.js` — вывод всех данных на главной и экспорт.
- `tests/benchmark.test.mjs` — проверки диапазонов, сценариев и генерации.

Подробности — [запуск и тесты](docs/running.md).
