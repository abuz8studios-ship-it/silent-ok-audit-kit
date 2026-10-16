# Silent-OK Audit Kit

Your agent says OK. Nothing shipped.

This kit finds agent work that looks finished in dashboards while the artifact,
sign-in, or verification chain is still broken. It is built from a live audit of a
Hermes desk on 2026-10-15: five inbox flags were checked against the actual final
session messages. One was a real user task. Four were vocabulary triggers.

## Run the classifier

Requirements: Python 3.11+

```powershell
python audit_endings.py last-message.txt
python -m pytest -q
```

It outputs one category: `done`, `user_todo`, `needs_sign_in`, `needs_approval`,
`hit_limit`, `site_refused`, `missing_tool`, `screen_problem`, or `asked_question`.

## The 20-minute audit

1. List every enabled **and paused** cron/automation.
2. Diff scheduled fires against dated artifacts: URLs, files, receipts, deployments.
3. Read five recent session endings in full. Classify state, not keywords.
4. Test every required sign-in with the product's own read-only command.
5. Mark each shipped ID: partial or full. Full requires a fresh target read-back,
   an independent timestamp/ID check, and a profile/history cross-check.
6. Record one owner and one next action for every open row. No owner — no closure.

## Files

- `audit_endings.py` — ending-state classifier
- `test_audit_endings.py` — regression cases from the live failure modes
- `scorecard.csv` — audit scoring sheet
- `run-ledger-template.csv` — fires versus artifacts ledger
- `full-verification-gate.md` — the publish/completion gate
- `social-pack.md` — proof-post copy for X, Instagram, and Facebook

## Truth boundary

The templates and classifier are ready to use. They do not prove another system is
healthy by themselves. A row becomes verified only when you attach fresh evidence
from that system and re-run the check in a separate view or runtime.

Built by ABUZ8 LLC. Hermes Agent Inbox case credited to @BkashJosi / BkashJEE.
