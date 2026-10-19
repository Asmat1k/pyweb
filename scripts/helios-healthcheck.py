"""Проверяем публикацию по HTTP и формируем сводку из подтверждённых данных."""
import argparse
import html
import json
import os
import sys
import time
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlencode, urljoin
from urllib.request import Request, urlopen


def fetch(url, query):
    separator = '&' if '?' in url else '?'
    request = Request(
        f'{url}{separator}{query}',
        headers={'Cache-Control': 'no-cache', 'User-Agent': 'pyweb-helios-healthcheck'},
    )
    with urlopen(request, timeout=20) as response:
        if response.status != 200:
            raise ValueError(f'{url}: HTTP {response.status}, ожидался 200')
        return response.read().decode('utf-8', errors='replace')


def details(url, release, query, allow_missing_info):
    if release == 'legacy':
        return 'не проверялся (legacy)', 'не проверялся (legacy)'
    try:
        info = json.loads(fetch(urljoin(url, 'build-info.json'), query))
    except HTTPError as exc:
        # Старые релизы созданы до добавления метаданных; откат на них разрешён.
        if allow_missing_info and exc.code == 404:
            return 'не проверялся (старый релиз без метаданных)', 'HTTP 404 (старый релиз)'
        raise
    if not isinstance(info, dict) or info.get('release') != release or info.get('sha') != release.split('-')[0]:
        raise ValueError('build-info.json: идентификатор релиза или SHA не совпадает с ожидаемым')
    generator = info.get('generator')
    # Проверяем настоящий индекс генератора, а не только наличие главной страницы.
    if generator == 'mkdocs':
        index = json.loads(fetch(urljoin(url, 'search/search_index.json'), query))
        if not isinstance(index, dict) or not isinstance(index.get('docs'), list) or not index['docs']:
            raise ValueError('Поисковый индекс MkDocs пуст или имеет неверный формат')
        search = 'HTTP 200'
    elif generator in ('pelican', 'sphinx', 'quarto'):
        search = f'не проверялся (генератор {generator})'
    else:
        raise ValueError('build-info.json: неизвестный генератор')
    return search, f'HTTP 200, отдаётся релиз `{info["sha"]}`'


def summary(url, marker, search, info):
    # Экранируем пользовательскую контрольную строку перед добавлением в Markdown.
    safe_marker = html.escape(marker).replace('`', '&#96;').replace('\n', '&#10;').replace('\r', '&#13;')
    kind = 'rollback' if os.environ.get('OPERATION') == 'rollback' else (
        'release' if os.environ.get('GITHUB_REF_NAME') == 'main' else 'preview'
    )
    return (
        '### Публикация на Helios\n\n'
        f'- Вид публикации: {kind}\n'
        f'- URL: [{url}]({url})\n'
        '- HTTP: 200\n'
        f'- Контрольная строка: <code>{safe_marker}</code>\n'
        f'- Поисковый индекс: {search}\n'
        f'- build-info.json: {info}\n'
        '- Схема раскладки: dirswap\n'
        f'- Коммит workflow: {os.environ.get("GITHUB_SHA", "не указан")}\n'
    )


def check(url, marker, release, attempts=5, delay=3, report=None, allow_missing_info=False):
    expected = f'<!-- helios-pyweb release:{release} -->'
    for attempt in range(1, attempts + 1):
        query = urlencode({'helios_release': release, 'attempt': attempt})
        try:
            body = fetch(url, query)
            if marker not in body or (release != 'legacy' and expected not in body):
                raise ValueError('В HTML отсутствует контрольная строка или ожидаемый релиз')
            if report:
                search, info = details(url, release, query, allow_missing_info)
                Path(report).write_text(summary(url, marker, search, info), encoding='utf-8')
            print(f'Проверка пройдена: HTTP 200, контрольная строка и релиз {release}: {url}')
            return
        except (OSError, ValueError) as exc:
            print(f'Попытка {attempt}/{attempts}: {exc}', file=sys.stderr)
        if attempt < attempts:
            time.sleep(delay)
    raise SystemExit(f'Проверка публикации не пройдена: {url}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('url')
    parser.add_argument('marker')
    parser.add_argument('release')
    parser.add_argument('--report', help='Файл сводки после успешной расширенной проверки')
    parser.add_argument('--allow-missing-info', action='store_true', help='Разрешить откат на старый релиз без build-info.json')
    args = parser.parse_args()
    check(args.url, args.marker, args.release, report=args.report, allow_missing_info=args.allow_missing_info)
