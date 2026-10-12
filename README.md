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

## Pelican

Ветка `pelican` собирает сайт с помощью Pelican 4.12 и Python-Markdown.
Нужен Python 3.12 или 3.13. Все документы в `docs/` являются статическими
страницами, главная записывается в `output/index.html`.

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
# Разработка: http://localhost:8000/
SITE_URL= pelican docs -s pelicanconf.py --autoreload --listen
# Публикационная сборка: HTML в output/
pelican docs -s pelicanconf.py
```

Переменная `SITE_URL` задаёт адрес сайта, включая префикс пути:
по умолчанию `https://asmat1k.github.io/pyweb/`. Пустое значение включает
относительные ссылки для локальной разработки. Ссылки между документами
используют синтаксис Pelican `({filename}methodology.md)`.

GitHub Pages собирает ветки `main` и `pelican`, включая pull request,
и публикует только push или ручной запуск этих веток. Для публикации из
`pelican` окружение `github-pages` должно разрешать эту ветку в настройках
репозитория. Helios публикует эти же ветки только при `HELIOS_ENABLED=true`,
с секретами `HELIOS_USER`, `HELIOS_SSH_PRIVATE_KEY` и `HELIOS_SSH_KNOWN_HOSTS`;
адрес автоматически устанавливается в `https://se.ifmo.ru/~USER/pyweb/`.

Официальная документация:
[установка](https://docs.getpelican.com/en/stable/install.html),
[метаданные и внутренние ссылки](https://docs.getpelican.com/en/stable/content.html),
[настройки](https://docs.getpelican.com/en/stable/settings.html),
[сборка и разработка](https://docs.getpelican.com/en/stable/publish.html),
[темы](https://docs.getpelican.com/en/stable/themes.html).
