#!/usr/bin/env python3
"""Classify how an agent session ended.

The point is simple: never judge a session from a trigger word alone.
Negation, recovery notes, completed reports, and explicit user tasks are
checked before the stuck rules fire.

Input text should be the final assistant message (plain text or Markdown).
Output categories:
  done, user_todo, needs_sign_in, needs_approval, hit_limit,
  site_refused, missing_tool, screen_problem, asked_question
"""
import re
import sys

NEGATED = [
    r"\bnone\b[^.\n]{0,80}\b(2fa|sign[ -]?in|login|password)\b",
    r"\bno\b[^.\n]{0,40}\b(sign[ -]?in|login|2fa)\b[^.\n]{0,30}\b(needed|required)\b",
    r"\bnot\b[^.\n]{0,30}\b(logged out|blocked)\b",
]
COMPLETED = [
    r"\b(bottom line|summary|shipped|logged to|files created|no files created|web-only research task)\b",
    r"\b(done|completed|finished)\b[^.\n]{0,80}\b(summary|report|research|work)\b",
]
RECOVERED = [
    r"\bfell back\b.*\bstill returned\b",
    r"\breturned results\b",
    r"\bdisregarded for\b",
    r"\bflagged above\b",
]
USER_TODO = [
    r"\brun `[^`]+` in your terminal\b",
    r"\bstill yours\b",
    r"\bsend [^.\n]+ whenever\b",
]
STUCK = [
    ("needs_sign_in", r"\b(please|you need to|run)\b[^.\n]{0,50}\b(sign[ -]?in|log[ -]?in|auth login)\b"),
    ("needs_sign_in", r"\b(verification code|captcha)\b[^.\n]{0,50}\b(enter|complete|solve)\b"),
    ("needs_approval", r"\b(requires approval|needs? (your )?approval|awaiting (your )?approval)\b"),
    ("missing_tool", r"\b(not available in this session|tool is unavailable|unknown tool|no such tool)\b"),
    ("hit_limit", r"\b(tool-call limit|maximum turns|iteration limit|timed out before|budget (was )?(exhausted|exceeded|spent))\b"),
    ("site_refused", r"\b(connection (refused|reset)|http 403|http 429)\b[^.\n]{0,80}\b(cannot|can't|unable|failed|stopped)\b"),
    ("screen_problem", r"\b(no active window|display (is )?not reachable|capture failed)\b"),
]


def has(patterns, text):
    return any(re.search(p, text, re.I | re.S) for p in patterns)


def classify(text: str) -> str:
    tail = (text or "").strip()[-2500:]
    low = tail.lower()

    if has(NEGATED, tail):
        return "done"
    if has(RECOVERED, tail) and has(COMPLETED, tail):
        return "done"
    # A completed report whose analysis merely discusses prices or limits is done.
    if has(COMPLETED, tail) and not re.search(
        r"\b(budget (was )?(exhausted|exceeded)|timed out before|maximum turns)\b", tail, re.I
    ):
        return "user_todo" if has(USER_TODO, tail) else "done"
    if has(USER_TODO, tail):
        return "user_todo"
    for label, pattern in STUCK:
        if re.search(pattern, tail, re.I | re.S):
            return label
    if low.rstrip().endswith("?"):
        return "asked_question"
    return "done"


def main():
    data = sys.stdin.read() if len(sys.argv) < 2 else open(sys.argv[1], encoding="utf-8").read()
    print(classify(data))


if __name__ == "__main__":
    main()
