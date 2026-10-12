import os

project = "WebTransport и WebSocket"
author = "Asmat1k"
language = "ru"
extensions = ["myst_parser", "sphinx.ext.githubpages"]
source_suffix = {".md": "markdown"}
root_doc = "index"
myst_enable_extensions = ["colon_fence"]
myst_heading_anchors = 3

html_theme = "alabaster"
html_title = project
html_baseurl = os.environ.get("SITE_URL", "https://asmat1k.github.io/pyweb/")
html_search_language = "ru"
html_sidebars = {"**": ["about.html", "globaltoc.html", "relations.html", "searchbox.html"]}
