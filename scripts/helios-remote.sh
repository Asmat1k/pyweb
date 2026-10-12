#!/usr/bin/env bash
# Выполняется на Helios: `ssh ... 'bash -s -- OP TARGET RELEASE' < этот-файл`.
# Останавливаемся при ошибке команды, обращении к неопределённой переменной
# или ошибке внутри конвейера; новые файлы доступны владельцу на запись.
set -euo pipefail
umask 022
operation=${1:?operation required}
target=${2:?target required}
release=${3:-}
# Разрешаем только безопасные имена каталогов: ни слешей, ни переходов через ..
# Идентификатор релиза состоит из SHA коммита, номера запуска и номера попытки.
[[ "$target" =~ ^[a-z0-9][a-z0-9-]{0,63}$ ]] || { echo 'Invalid target' >&2; exit 1; }
[[ "$operation" == prepare || "$operation" == activate || "$operation" == rollback ]] || exit 1
if [[ "$operation" != rollback ]]; then
    [[ "$release" =~ ^[a-f0-9]{40}-[0-9]+-[0-9]+$ ]] || { echo 'Invalid release' >&2; exit 1; }
fi

state="$HOME/.helios-pyweb/$target"
# У каждой ветки свои опубликованный каталог, загрузки и резервные копии.
live="$HOME/public_html/pyweb"
if [[ "$target" != main ]]; then live="$HOME/public_html/pyweb-previews/$target"; fi
# Не следуем по символьным ссылкам: иначе запись может уйти за пределы
# предназначенного каталога, даже если само имя ветки прошло проверку.
for path in "$HOME/public_html" "$HOME/public_html/pyweb-previews" "$HOME/.helios-pyweb" "$state" "$state/staging" "$state/history" "$state/previous" "$live"; do
    [[ ! -L "$path" ]] || { echo "Refusing symlink: $path" >&2; exit 1; }
done
mkdir -p "$state/staging" "$state/history" "$(dirname "$live")"
# Резервные копии закрыты от других пользователей, а опубликованные страницы
# доступны веб-серверу. После mv каталог загрузки сохраняет свои права доступа.
chmod 700 "$HOME/.helios-pyweb" "$state"
chmod 755 "$HOME/public_html" "$(dirname "$live")"
stage="$state/staging/$release"
if [[ "$operation" == prepare ]]; then
    # rsync загрузит сайт в новый каталог; текущая публикация пока не меняется.
    [[ ! -e "$stage" && ! -L "$stage" ]] || { echo 'Release already exists' >&2; exit 1; }
    mkdir "$stage"
    exit 0
fi

# mkdir создаёт блокировку атомарно: только один процесс может её получить.
# Она защищает и ручные переключения вне GitHub Actions. EXIT освобождает
# блокировку при обычном завершении и ошибке; после SIGKILL она может остаться.
mkdir "$state/lock" || { echo 'Another switch is running (or a stale lock exists)' >&2; exit 1; }
trap 'rmdir "$state/lock"' EXIT
if [[ "$operation" == activate ]]; then
    # До переключения проверяем главную страницу и идентификатор загрузки.
    # Сам rsync должен успешно завершиться на runner перед вызовом activate.
    [[ ! -L "$stage" && -s "$stage/index.html" && -f "$stage/.helios-release" ]]
    [[ "$(cat "$stage/.helios-release")" == "$release" ]]
    if [[ -e "$state/previous" ]]; then
        # Более старую копию переносим в историю, освобождая previous для
        # текущего сайта. Время и PID различают имена резервных копий.
        mv "$state/previous" "$state/history/$(date -u +%Y%m%dT%H%M%S)-$$"
    fi
    if [[ -e "$live" ]]; then
        # У сайта из старого workflow нет идентификатора: помечаем его legacy,
        # чтобы сохранить возможность отката после первой новой публикации.
        if [[ ! -f "$live/.helios-release" ]]; then printf 'legacy\n' > "$live/.helios-release"; fi
        mv "$live" "$state/previous"
    fi
    # Между двумя mv возможен короткий перерыв в доступности сайта.
    # Если установка новой версии не удалась, возвращаем прежний каталог.
    if ! mv "$stage" "$live"; then
        if [[ -d "$state/previous" ]]; then mv "$state/previous" "$live"; fi
        echo 'Activation failed; restored the previous directory' >&2
        exit 1
    fi
else
    # Откат меняет местами текущую и предыдущую версии через временный swap.
    # Поэтому повторный откат возвращает версию, которая была до первого.
    [[ -s "$state/previous/index.html" && -f "$state/previous/.helios-release" ]] || { echo 'No previous version to restore' >&2; exit 1; }
    restored=$(cat "$state/previous/.helios-release")
    [[ "$restored" =~ ^[a-f0-9]{40}-[0-9]+-[0-9]+$ || "$restored" == legacy ]]
    [[ -d "$live" && ! -e "$state/swap" && ! -L "$state/swap" ]]
    mv "$live" "$state/swap"
    if ! mv "$state/previous" "$live"; then
        mv "$state/swap" "$live"
        exit 1
    fi
    mv "$state/swap" "$state/previous"
    # stdout содержит только идентификатор: workflow запишет его в RELEASE
    # и проверит, что по публичному URL действительно отдаётся эта версия.
    printf '%s\n' "$restored"
fi
