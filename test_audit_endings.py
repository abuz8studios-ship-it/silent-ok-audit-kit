from audit_endings import classify

DAILY_CLOSE = """new reply. Mentions: thanks only, already answered.

**Desk I NEED YOU** — none (Chrome / 2FA). Profile 2 Abu live.

**Tomorrow top 3**
1. Profile pull
2. One ship-log
3. Inbound only

Logged to `ops_daily.md`."""

HF_HANDOFF = """Done — GitHub org profile is live and API-verified.

Still yours: run `hf auth login` in your terminal for Hugging Face, and send X bio wording whenever — both ship same turn."""

RECOVERED_429 = """## Bottom line
Use standard business products until donation requirements are checked.

**Issues:** search backend returned HTTP 429 (fell back to keyless tier, still returned results)."""

PRICING_BUDGET = """## Bottom line
- BMC: viable tip jar + memberships for the LLC; budget ~6–8% all-in per transaction.
- Files created/modified: none."""

TRANSPARENT_BUDGET = """## Bottom line for a 1-person US LLC
Open Collective adds transparent-budget tooling but layers fees.
- No files created or modified; web-only research task."""


def test_negated_2fa_is_done():
    assert classify(DAILY_CLOSE) == "done"


def test_explicit_terminal_login_is_user_todo_not_stuck():
    assert classify(HF_HANDOFF) == "user_todo"


def test_recovered_429_in_completed_report_is_done():
    assert classify(RECOVERED_429) == "done"


def test_pricing_budget_is_not_limit():
    assert classify(PRICING_BUDGET) == "done"
    assert classify(TRANSPARENT_BUDGET) == "done"


def test_real_exhausted_budget_is_limit():
    assert classify("I could not finish because the budget was exhausted.") == "hit_limit"


def test_real_sign_in_request_is_stuck():
    assert classify("Please sign in to the dashboard so I can continue.") == "needs_sign_in"
