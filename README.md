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

- [Область сравнения](docs/about.qmd)
- [WebSocket](docs/websocket.qmd) и [WebTransport](docs/webtransport.qmd)
- [Методика](docs/methodology.qmd) и [сценарии экспериментов](docs/scenarios.qmd)
- [Результаты и предварительные выводы](docs/results.qmd)
- [Источники](docs/references.qmd)

Материалы доступны на [сайте](https://asmat1k.github.io/pyweb/).

**Статус исследования:** опубликованы теоретическое сравнение и план экспериментов.
Измерения не проводились; прочерки в таблицах обозначают отсутствие данных.


## Сборка на Quarto

Ветка `quarto` использует [Quarto CLI](https://quarto.org/docs/get-started/).
Python и MkDocs для сборки не нужны. Конфигурация находится в
`docs/_quarto.yml`, материалы — в `docs/*.qmd`.

Предпросмотр из корня репозитория:

```sh
quarto preview docs
```

Сборка статического сайта:

```sh
quarto render docs
```

Готовые файлы появляются в `docs/_site/`; главная страница — `index.html`.
Внутренние ссылки указывают на `.qmd`, Quarto преобразует их в ссылки на HTML.
Информационные блоки используют встроенные callouts Quarto.

## CI/CD

GitHub Actions автоматически собирает сайт при push и pull request в `main`.
GitHub Pages автоматически публикуется только при push в `main`; pull request
выполняет только сборку. В остальных ветках запуск ручной: Actions →
GitHub Pages или Helios → Run workflow → выбрать ветку → Run workflow.
Ручной запуск собирает и публикует выбранную ветку. GitHub Pages получает
артефакт `docs/_site/`. В Settings → Pages выберите источник GitHub Actions
и разрешите выбранную ветку в правилах окружения `github-pages`.

Helios автоматически запускается при push в `main` или вручную из
выбранной ветки только при переменной репозитория
`HELIOS_ENABLED=true`. Задайте секреты `HELIOS_USER` (логин вида `s123456`),
`HELIOS_SSH_PRIVATE_KEY` и `HELIOS_SSH_KNOWN_HOSTS` (проверенный ключ хоста
`[helios.cs.ifmo.ru]:2222`). Workflow создаёт временный профиль Quarto
`helios` с адресом `https://se.ifmo.ru/~<HELIOS_USER>/pyweb/` и публикует
HTML в `~/public_html/pyweb/`. Профиль не хранит секреты в репозитории.

Официальная документация:

- [Сайты и внутренние ссылки](https://quarto.org/docs/websites/).
- [Навигация](https://quarto.org/docs/websites/website-navigation.html).
- [Callout-блоки](https://quarto.org/docs/authoring/callouts.html).
- [Профили проекта](https://quarto.org/docs/projects/profiles.html).
- [Публикация через CI](https://quarto.org/docs/publishing/ci.html).
