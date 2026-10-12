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
- [Источники](docs/references.md)

Материалы доступны на [сайте](https://asmat1k.github.io/pyweb/).

**Статус исследования:** опубликованы теоретическое сравнение и план экспериментов.
Измерения не проводились; прочерки в таблицах обозначают отсутствие данных.


## CI/CD

Автоматическая публикация на GitHub Pages и Helios выполняется только при push
в `main`. Pull request в `main` запускает сборку без публикации.
В других ветках workflows запускаются вручную: Actions → GitHub Pages или
Helios → Run workflow → выбрать ветку → Run workflow. Ручной запуск собирает
и публикует выбранную ветку. Helios требует `HELIOS_ENABLED=true` и секреты
`HELIOS_USER`, `HELIOS_SSH_PRIVATE_KEY`, `HELIOS_SSH_KNOWN_HOSTS`.
Окружение `github-pages` должно разрешать публикацию из выбранной ветки.
