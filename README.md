# WebTransport и WebSocket

Статический сайт исследования «Выбор технологий WebTransport и WebSocket для
двунаправленной передачи данных в веб-приложениях». Выполнен для задания 1 по
генераторам статических сайтов на Python.

Четыре критерия: время подключения и RTT, задержка сообщения, накладные расходы,
поведение при потерях пакетов. Материалы содержат теоретическое сравнение и план
измерений. Сетевого стенда и эмпирических результатов в репозитории пока нет.

## Запуск

Используется Python 3.14.8, MkDocs 1.6.1 и Material 9.7.7.

```bash
python3.14 -m pip install virtualenv==21.14.6
python3.14 -m virtualenv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
mkdocs serve
```

Открыть <http://127.0.0.1:8000/pyweb/>. После остановки предпросмотра (`Ctrl+C`):

```bash
mkdocs build --strict
```

HTML создаётся в `site/`. Предпросмотр и строгая сборка — проверки из задания;
автоматические тесты не добавлены. Все прямые и транзитивные зависимости закреплены
точными версиями в `requirements.txt`.

## Структура

```text
docs/                 Исследование, источники и отчёт
mkdocs.yml            Навигация, тема и строгая проверка ссылок
requirements.txt      Зафиксированные зависимости
.github/workflows/    Автоматическая сборка и публикация
task1.md              Исходное задание
```

## Публикация

Опубликованный сайт: <https://asmat1k.github.io/pyweb/>.
В репозитории выбрать **Settings → Pages → Source → GitHub Actions**.
Workflow `GitHub Pages` собирает сайт с `--strict`, затем публикует `site/`.
Pull request запускает только сборку. Push в `main` и ручной запуск на `main`
запускают публикацию.

Второй workflow `Helios` использует SSH/rsync и отдельный каталог
`~/public_html/pyweb/`. Для него задать в **Settings → Secrets and variables → Actions**:

| Тип | Имя | Значение |
|---|---|---|
| Secret | `HELIOS_USER` | Логин ИТМО вида `s123456` |
| Secret | `HELIOS_SSH_PRIVATE_KEY` | Отдельный приватный SSH-ключ для CI |
| Secret | `HELIOS_SSH_KNOWN_HOSTS` | Проверенная запись ключа сервера для `[helios.cs.ifmo.ru]:2222` |
| Variable | `HELIOS_ENABLED` | `true` после настройки секретов |

Публичный ключ CI предварительно добавить в `~/.ssh/authorized_keys` на Helios.
Целевой адрес: `https://se.ifmo.ru/~ЛОГИН/pyweb/`. Без настройки доступа этот
workflow пропускает публикацию; это не означает, что сайт на Helios развёрнут.

Полные инструкции — [запуск и публикация](docs/running.md), фактический статус —
[отчёт по заданию](docs/report.md).
