"""Проверяем HTTP 200, контрольную строку и ожидаемый релиз в HTML."""
import sys
import time
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


def check(url, marker, release, attempts=5, delay=3):
    # Совпасть должен весь комментарий: страница от другого релиза не пройдёт
    # проверку, даже если в ней есть общая контрольная строка helios-pyweb.
    expected = f"<!-- helios-pyweb release:{release} -->"
    for attempt in range(1, attempts + 1):
        # Параметры релиза и попытки меняют URL, уменьшая риск ответа из кеша.
        # urlencode экранирует значения, а разделитель учитывает существующий query.
        request = Request(
            url + ("&" if "?" in url else "?") + urlencode({"helios_release": release, "attempt": attempt}),
            headers={"Cache-Control": "no-cache", "User-Agent": "pyweb-helios-healthcheck"},
        )
        try:
            with urlopen(request, timeout=20) as response:
                html = response.read().decode("utf-8", errors="replace")
                # У legacy-сайта из старого workflow нет комментария с релизом:
                # для него проверяем только HTTP 200 и заданную контрольную строку.
                if response.status == 200 and marker in html and (release == "legacy" or expected in html):
                    print(f"Healthcheck passed: HTTP 200, marker and release {release}: {url}")
                    return
                error = f"HTTP {response.status}; control string or expected release missing"
        except (URLError, TimeoutError, OSError) as exc:
            # HTTP-ошибки и сетевые сбои считаем неудачной попыткой, а не успехом.
            error = str(exc)
        print(f"Attempt {attempt}/{attempts}: {error}", file=sys.stderr)
        if attempt < attempts:
            # Пауза нужна только между попытками; после последней сразу падаем.
            time.sleep(delay)
    # SystemExit со строкой даёт ненулевой код выхода и завершает шаг CI ошибкой.
    raise SystemExit(f"Healthcheck failed: {url}")


if __name__ == "__main__":
    check(*sys.argv[1:])
