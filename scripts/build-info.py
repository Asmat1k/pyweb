"""Добавляем в артефакт сведения о сборке для проверки опубликованной версии."""
import json
import os
from datetime import datetime, timezone
from pathlib import Path

site = Path('site')
generator = os.environ['GENERATOR']
info = {
    'repository': os.environ['GITHUB_REPOSITORY'],
    'ref': os.environ['GITHUB_REF'],
    'sha': os.environ['GITHUB_SHA'],
    'release': os.environ['RELEASE'],
    'generator': generator,
    'built_at': datetime.now(timezone.utc).isoformat(),
}
# У MkDocs с включённым поиском этот файл обязателен.
if generator == 'mkdocs' and not (site / 'search/search_index.json').is_file():
    raise SystemExit('В сборке отсутствует поисковый индекс MkDocs')
(site / 'build-info.json').write_text(
    json.dumps(info, ensure_ascii=False, indent=2) + '\n', encoding='utf-8'
)
