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

## Разработка и сборка

Ветка `sphinx` использует Sphinx с MyST-Parser: исходные страницы остаются
в Markdown в `docs/`, конфигурация находится в `docs/conf.py`, а навигация
задаётся директивами `toctree` в `docs/index.md`.

Требуется Python 3.12 или новее.

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m sphinx -b dirhtml -W docs site
python -m http.server 8000 --directory site
```

Сайт доступен по адресу <http://localhost:8000/>. После изменения страниц
повторите команду сборки и обновите браузер. Генератор `dirhtml` сохраняет
адреса страниц вида `/websocket/`; `-W` делает предупреждения ошибками сборки.
Для другого адреса публикации задайте переменную `SITE_URL` перед сборкой.

GitHub Actions автоматически собирает сайт при push и pull request в `main`.
GitHub Pages автоматически публикуется только при push в `main`.
В остальных ветках запуск ручной: Actions → GitHub Pages или Helios →
Run workflow → выбрать ветку → Run workflow. Ручной запуск собирает и
публикует выбранную ветку; pull request выполняет только сборку.
В настройках Pages выберите источник **GitHub Actions** и разрешите ветку
`sphinx` в правилах окружения `github-pages`, если они ограничивают развёртывание.
Обе ветки публикуются по одному адресу; последняя публикация заменяет предыдущую.

Развёртывание на Helios включается переменной репозитория `HELIOS_ENABLED=true`.
Задайте секреты `HELIOS_USER` (логин вида `s123456`),
`HELIOS_SSH_PRIVATE_KEY` и `HELIOS_SSH_KNOWN_HOSTS` (проверенный ключ узла
`[helios.cs.ifmo.ru]:2222`). Workflow публикует `site/` в
`~/public_html/pyweb/`, используя адрес `https://se.ifmo.ru/~<логин>/pyweb/`.

Официальная документация: [конфигурация Sphinx](https://www.sphinx-doc.org/en/master/usage/configuration.html),
[сборка Sphinx](https://www.sphinx-doc.org/en/master/man/sphinx-build.html),
[генератор dirhtml](https://www.sphinx-doc.org/en/master/usage/builders/index.html#sphinx.builders.dirhtml.DirectoryHTMLBuilder),
[MyST-Parser](https://myst-parser.readthedocs.io/en/latest/intro.html),
[навигация MyST](https://myst-parser.readthedocs.io/en/latest/syntax/organising_content.html)
и [блоки примечаний MyST](https://myst-parser.readthedocs.io/en/latest/syntax/admonitions.html).
