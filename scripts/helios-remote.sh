#!/usr/bin/env bash
set -euo pipefail
umask 022
operation=${1:?operation required}
target=${2:?target required}
release=${3:-}
[[ "$target" =~ ^[a-z0-9][a-z0-9-]{0,63}$ ]] || { echo 'Invalid target' >&2; exit 1; }
[[ "$operation" == prepare || "$operation" == activate || "$operation" == rollback || "$operation" == prune ]] || exit 1
if [[ "$operation" == prepare || "$operation" == activate ]]; then
    [[ "$release" =~ ^[a-f0-9]{40}-[0-9]+-[0-9]+$ ]] || { echo 'Invalid release' >&2; exit 1; }
fi

# У каждой ветки отдельные публикация и резервные копии.
state="$HOME/.helios-pyweb/$target"
previous="$state/previous"
swap="$state/swap"
live="$HOME/public_html/pyweb"
if [[ "$target" != main ]]; then live="$HOME/public_html/pyweb-previews/$target"; fi
# Не допускаем запись через ссылки за пределы каталогов публикации.
for path in "$HOME/public_html" "$HOME/public_html/pyweb-previews" "$HOME/.helios-pyweb" "$state" "$state/staging" "$state/history" "$previous" "$live"; do
    [[ ! -L "$path" ]] || { echo "Refusing symlink: $path" >&2; exit 1; }
done
parent=${live%/*}
mkdir -p "$state/staging" "$state/history" "$parent"
chmod 700 "$HOME/.helios-pyweb" "$state"
chmod 755 "$HOME/public_html" "$parent"
stage="$state/staging/$release"
if [[ "$operation" == prepare ]]; then
    [[ ! -e "$stage" && ! -L "$stage" ]] || { echo 'Release already exists' >&2; exit 1; }
    mkdir "$stage"
    exit 0
fi

# Блокировка защищает также от ручного переключения через SSH.
mkdir "$state/lock" || { echo 'Another switch is running (or a stale lock exists)' >&2; exit 1; }
trap 'rmdir "$state/lock"' EXIT
if [[ "$operation" == prune ]]; then
    # Keep live + previous + the three newest managed history directories.
    # Never follow links or remove directories without our release marker.
    count=0
    while IFS= read -r name; do
        archived="$state/history/$name"
        [[ "$name" =~ ^[0-9]{8}T[0-9]{6}-[0-9]+$ ]] || continue
        [[ -d "$archived" && ! -L "$archived" && -f "$archived/.helios-release" ]] || continue
        count=$((count + 1))
        if (( count > 3 )); then rm -rf -- "$archived"; fi
    done < <(LC_ALL=C ls -1 "$state/history" | LC_ALL=C sort -r)
    exit 0
fi
if [[ "$operation" == activate ]]; then
    [[ ! -L "$stage" && -s "$stage/index.html" && -f "$stage/.helios-release" ]]
    [[ "$(cat "$stage/.helios-release")" == "$release" ]]
    if [[ -e "$previous" ]]; then
        mv "$previous" "$state/history/$(date -u +%Y%m%dT%H%M%S)-$$"
    fi
    if [[ -e "$live" ]]; then
        # Сохраняем возможность отката на сайт из старого workflow.
        if [[ ! -f "$live/.helios-release" ]]; then printf 'legacy\n' > "$live/.helios-release"; fi
        mv "$live" "$previous"
    fi
    # Между переименованиями возможен короткий простой; при ошибке восстанавливаем сайт.
    if ! mv "$stage" "$live"; then
        if [[ -d "$previous" ]]; then mv "$previous" "$live"; fi
        echo 'Activation failed; restored the previous directory' >&2
        exit 1
    fi
else
    # Меняем версии местами: повторный rollback возвращает исходную публикацию.
    [[ -s "$previous/index.html" && -f "$previous/.helios-release" ]] || { echo 'No previous version to restore' >&2; exit 1; }
    restored=$(cat "$previous/.helios-release")
    [[ "$restored" =~ ^[a-f0-9]{40}-[0-9]+-[0-9]+$ || "$restored" == legacy ]]
    [[ -d "$live" && ! -e "$swap" && ! -L "$swap" ]]
    mv "$live" "$swap"
    if ! mv "$previous" "$live"; then
        mv "$swap" "$live"
        exit 1
    fi
    mv "$swap" "$previous"
    printf '%s\n' "$restored"
fi
