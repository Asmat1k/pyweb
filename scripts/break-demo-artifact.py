"""Intentionally invalidate only the rollback demo's built HTML."""
import os
from pathlib import Path


def break_artifact(site, release):
    index = site / 'index.html'
    expected = f'<!-- helios-pyweb release:{release} -->'
    body = index.read_text(encoding='utf-8')
    if expected not in body:
        raise SystemExit('Expected release marker is missing; refusing an invalid demo')
    index.write_text(body.replace(expected, '<!-- intentional rollback demo failure -->'), encoding='utf-8')


if __name__ == '__main__':
    if (os.environ.get('GITHUB_REF') != 'refs/heads/codex/rollback-demo'
            or os.environ.get('GITHUB_EVENT_NAME') != 'workflow_dispatch'):
        raise SystemExit('Failure injection is restricted to manual rollback-demo runs')
    break_artifact(Path('site'), os.environ['RELEASE'])
