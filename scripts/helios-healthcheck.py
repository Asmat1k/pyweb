"""Проверяем HTTP 200, контрольную строку и ожидаемый релиз в HTML."""
import sys
import time
from urllib.parse import urlencode
from urllib.request import Request, urlopen


def check(url, marker, release, attempts=5, delay=3):
    # Legacy HTML не содержит идентификатора релиза.
    expected = f"<!-- helios-pyweb release:{release} -->"
    separator = "&" if "?" in url else "?"
    for attempt in range(1, attempts + 1):
        # Новый query для каждой попытки уменьшает риск ответа из кеша.
        query = urlencode({"helios_release": release, "attempt": attempt})
        request = Request(
            f"{url}{separator}{query}",
            headers={"Cache-Control": "no-cache", "User-Agent": "pyweb-helios-healthcheck"},
        )
        try:
            with urlopen(request, timeout=20) as response:
                html = response.read().decode("utf-8", errors="replace")
                if response.status == 200 and marker in html and (release == "legacy" or expected in html):
                    print(f"Healthcheck passed: HTTP 200, marker and release {release}: {url}")
                    return
                error = f"HTTP {response.status}; control string or expected release missing"
        except OSError as exc:
            error = str(exc)
        print(f"Attempt {attempt}/{attempts}: {error}", file=sys.stderr)
        if attempt < attempts:
            time.sleep(delay)
    raise SystemExit(f"Healthcheck failed: {url}")


if __name__ == "__main__":
    check(*sys.argv[1:])
