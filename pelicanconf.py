import os

AUTHOR = "Asmat1k"
SITENAME = "WebTransport и WebSocket"
SITEDESCRIPTION = "Выбор технологий WebTransport и WebSocket для двунаправленной передачи данных в веб-приложениях."
SITEURL = os.environ.get("SITE_URL", "https://asmat1k.github.io/pyweb/").rstrip("/")
RELATIVE_URLS = not SITEURL
PATH = "docs"
OUTPUT_PATH = "output"
TIMEZONE = "Europe/Moscow"
DEFAULT_LANG = "ru"

# This is a documentation site: every source is a page, including the home page.
ARTICLE_PATHS = []
PAGE_PATHS = [""]
STATIC_PATHS = []
PAGE_URL = "{slug}/"
PAGE_SAVE_AS = "{slug}/index.html"
DIRECT_TEMPLATES = []
AUTHOR_SAVE_AS = CATEGORY_SAVE_AS = TAG_SAVE_AS = ""
FEED_ALL_ATOM = CATEGORY_FEED_ATOM = TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = AUTHOR_FEED_RSS = None

THEME = "theme"
THEME_STATIC_PATHS = []
NAVIGATION = (
    ("", (("Главная", "index.html"), ("Область сравнения", "about/"), ("Методика", "methodology/"))),
    ("Технологии", (("WebSocket", "websocket/"), ("WebTransport", "webtransport/"))),
    ("Эксперимент", (("Сценарии экспериментов", "scenarios/"), ("Результаты", "results/"))),
    ("", (("Источники", "references/"),)),
)
MARKDOWN = {
    "extension_configs": {
        "markdown.extensions.meta": {},
        "markdown.extensions.extra": {},
        "markdown.extensions.admonition": {},
        "markdown.extensions.toc": {"permalink": True},
    },
    "output_format": "html5",
}
