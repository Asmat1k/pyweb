# Helios rollback demonstration

Branch: `codex/rollback-demo`. Do not merge this demonstration into `main`.

## Run

1. Push this branch: `git push -u origin codex/rollback-demo`.
2. Wait for **Публикация на Helios** to finish successfully. This creates the
   healthy baseline in this branch's isolated preview directory. Record its
   release ID and preview URL from the logs/summary. `HELIOS_ENABLED=true`,
   the existing SSH secrets, and permission to deploy this branch to the
   `helios` environment are required.
3. In Actions, manually run **Публикация на Helios**, selecting
   `codex/rollback-demo`, operation `deploy`, `rollback_demo=true`, and an
   empty `healthcheck_marker`. The build succeeds but its HTML release marker
   is deliberately removed before uploading the artifact.
4. Observe successful build and deploy jobs, then the failed health check
   in **Проверка публикации**. The automatic rollback step must succeed and
   report the baseline release ID. The overall run remains **failed** by design.
5. Open the preview URL and inspect the HTML release comment and
   `build-info.json`: both must identify the baseline, not the failed run.

If no successful baseline exists, run manually with `rollback_demo=false`
first. Repeat demonstrations using `deploy`, not manual `rollback`: rollback
swaps live and previous directories, so another rollback would restore the
intentionally broken release. A normal push or `deploy` with the demo disabled
publishes a healthy version again. GitHub Pages and the main Helios site are
unaffected by this branch's preview deployment.

## CI/CD review

Reviewed both workflows and all three deployment scripts at main commit
`022499569dc3b18f71766f25311e465f40ce625d`:

- Helios: strict generator build → artifact → SSH staging/activation → HTTP
  HTML, metadata and search checks → rollback on health-check failure.
  Publication runs are serialized; PRs build without deployment secrets.
- A compile/build failure skips deployment and cannot demonstrate rollback.
  A first deployment has no previous release to restore.
- GitHub Pages: strict MkDocs build → deploy from main → HTML health check.
  There is no automatic rollback step for Pages.
- Automatic rollback checks restored HTML and release identity, but does not
  request a report, so restored metadata and search are not checked.
- Failures before the health-check step (including verification setup errors)
  do not trigger automatic rollback. Directory swaps include a brief gap.
- No automated tests or lint checks are currently invoked by either workflow.
- Local `pelican`, `quarto`, and `sphinx` branch snapshots have older workflows
  and do not contain the current rollback scripts; they need separate updates
  before claiming the same rollback support.

This review describes repository configuration. Live Actions runs, repository
variables, secrets and environment protection rules require separate verification.
