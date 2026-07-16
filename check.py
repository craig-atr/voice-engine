#!/usr/bin/env python3
"""
Voice Engine — draft linter.

Turns the "never write like this" rules in rules.md and reference/anti-patterns.md
from a request the model is asked to honor into a constraint that fails out loud.
A must in markdown is a request; a must in code is a constraint.

What it checks, mechanically and deterministically:
  1. Banned phrases      — the corporate/AI tells listed in rules.md §2 and anti-patterns.md
  2. Invented links      — any URL that isn't on Craig's own atomictattooremoval.com domain
  3. Two-space fingerprint — sentence periods followed by a single space (Craig uses two)
  4. Left-in placeholders  — [[like this]] markers that must be filled before sending

Usage:
    python check.py draft.txt         # lint a file
    some_command | python check.py    # lint stdin
    python check.py --selftest        # run the built-in corpus test

Exit code is 0 when clean (no ERRORs), 1 when a draft has ERRORs or a self-test fails.
WARNs (the two-space fingerprint, placeholders) never fail the build on their own —
they are style nudges, not hard constraints. Pass --strict to fail on WARNs too.

Standard library only. No dependencies.
"""

import re
import sys

# --- The rules, as data -----------------------------------------------------

# Banned phrases (case-insensitive). Sourced verbatim from rules.md §2 and
# reference/anti-patterns.md. A hit here is an ERROR: it is not how Craig writes.
BANNED_PHRASES = [
    "i hope this email finds you well",
    "hope this finds you well",
    "hope this email finds you",
    "hope you're doing well",
    "hope you are doing well",
    "hope this finds you",
    "i wanted to reach out",
    "i'm reaching out",
    "reaching out to you",
    "please don't hesitate",
    "don't hesitate to reach out",
    "don't hesitate to",
    "circle back",
    "touch base",
    "synergy",
    "leverage",
    "seamless",
    "robust",
    "delve",
    "navigate the complexities",
    "a testament to",
    "in today's fast-paced world",
    "ever-evolving",
    "per my last email",
    "kindly be advised",
    "at this time",
    "warm regards",
    "best regards",
    "looking forward to",
    "so excited",
    "we're thrilled",
    "we are thrilled",
    "absolutely love",
    "love nothing more",
    "rest assured",
    "in conclusion",
    "on your tattoo removal journey",
    "tattoo removal journey",
]

# The "it's not just X, it's Y" false-profundity template (anti-patterns.md).
NOT_JUST_TEMPLATE = re.compile(r"it'?s not just\b.*?\bit'?s\b", re.IGNORECASE | re.DOTALL)

# Craig's own domain. Any link off this domain is treated as invented — the model
# must never guess a URL (identity.md: "You do not invent facts, names, numbers, links").
ALLOWED_URL_HOST = "atomictattooremoval.com"
URL_RE = re.compile(r"https?://([^/\s)]+)([^\s)]*)", re.IGNORECASE)

# Sentence period followed by exactly one space then a capital letter.
# Craig's fingerprint is TWO spaces, so a single space is a miss.
# The {2,} on the preceding word skips decimals/phone numbers (508.203.1342),
# and the abbreviation set below skips "Dr. Smith", "e.g. this", etc.
SINGLE_SPACE_RE = re.compile(r"\b([A-Za-z]{2,})\. (?=[A-Z])")
ABBREVIATIONS = {"mr", "mrs", "ms", "dr", "st", "ave", "vs", "inc", "ltd",
                 "co", "etc", "jr", "sr", "no", "eg", "ie"}

PLACEHOLDER_RE = re.compile(r"\[\[.+?\]\]")


# --- The checks -------------------------------------------------------------

def lint(text):
    """Return a list of (severity, line_no, message). severity is 'ERROR' or 'WARN'."""
    findings = []
    lines = text.splitlines()
    lower_lines = [ln.lower() for ln in lines]

    # 1. Banned phrases
    for i, low in enumerate(lower_lines, start=1):
        for phrase in BANNED_PHRASES:
            if phrase in low:
                findings.append(("ERROR", i, f'banned phrase: "{phrase}"'))

    # 1b. "it's not just X, it's Y" template (may span lines)
    for m in NOT_JUST_TEMPLATE.finditer(text):
        line_no = text.count("\n", 0, m.start()) + 1
        findings.append(("ERROR", line_no, 'banned template: "it\'s not just X, it\'s Y"'))

    # 2. Invented links (any URL off atomictattooremoval.com)
    for i, ln in enumerate(lines, start=1):
        for m in URL_RE.finditer(ln):
            host = m.group(1).lower()
            if not (host == ALLOWED_URL_HOST or host.endswith("." + ALLOWED_URL_HOST)):
                findings.append(("ERROR", i, f"unverified link (not on {ALLOWED_URL_HOST}): {m.group(0)}"))

    # 3. Two-space fingerprint
    for i, ln in enumerate(lines, start=1):
        for m in SINGLE_SPACE_RE.finditer(ln):
            if m.group(1).lower() in ABBREVIATIONS:
                continue
            findings.append(("WARN", i, f'single space after "{m.group(1)}." — Craig uses two'))

    # 4. Left-in placeholders (fine while drafting, not fine to send)
    for i, ln in enumerate(lines, start=1):
        for m in PLACEHOLDER_RE.finditer(ln):
            findings.append(("WARN", i, f"unfilled placeholder {m.group(0)} — fill before sending"))

    return findings


def report(text, strict=False):
    """Lint text, print findings, return an exit code."""
    findings = lint(text)
    errors = [f for f in findings if f[0] == "ERROR"]
    warns = [f for f in findings if f[0] == "WARN"]

    for sev, line_no, msg in findings:
        print(f"{sev}  line {line_no}: {msg}")

    if not findings:
        print("clean — reads like Craig.")

    print(f"\n{len(errors)} error(s), {len(warns)} warning(s).")
    if errors:
        return 1
    if strict and warns:
        return 1
    return 0


# --- Self-test --------------------------------------------------------------

# Real "me" drafts (from examples.md) must pass with zero ERRORs.
GOOD_SAMPLES = [
    # Pricing gold example
    "Hi Sam,\n\nSmall tattoos (smaller than a palm) are $150 a session.  "
    "You can book here: https://atomictattooremoval.com/book-consultation or "
    "text us at 508.203.1342.\n\nLet me know if you have any questions.",
    # Healing check-in (promoted gold, sent with no edits)
    "Hi Sam,\n\nJust wanted to check in and see how the healing is going after "
    "your last session.  Any blistering or anything you're not sure about?\n\n"
    "Feel free to send me a picture if you want me to take a look.  Let me know.",
    # One-word approval
    "Approved.",
]

# Generic "not me" drafts (from the contrast pairs) must each raise >=1 ERROR.
BAD_SAMPLES = [
    # Pair 1 — pricing
    "Thank you so much for reaching out to Atomic Tattoo Removal! We'd be "
    "absolutely delighted to help you on your tattoo removal journey.",
    # Throat-clearer + hesitate
    "Hi Sam,\n\nI hope this email finds you well! Please don't hesitate to reach out.",
    # Invented link on a foreign domain
    "You can book your appointment here: https://calendly.com/atomic/consult",
    # Corporate buzzwords
    "Let's circle back and leverage our synergy for a seamless, robust solution.",
]


def selftest():
    failures = 0

    for i, sample in enumerate(GOOD_SAMPLES, start=1):
        errs = [f for f in lint(sample) if f[0] == "ERROR"]
        if errs:
            failures += 1
            print(f"SELFTEST FAIL: good sample #{i} raised ERRORs it shouldn't have:")
            for sev, line_no, msg in errs:
                print(f"    {sev} line {line_no}: {msg}")
        else:
            print(f"ok: good sample #{i} passed clean")

    for i, sample in enumerate(BAD_SAMPLES, start=1):
        errs = [f for f in lint(sample) if f[0] == "ERROR"]
        if not errs:
            failures += 1
            print(f"SELFTEST FAIL: bad sample #{i} slipped through with no ERROR")
        else:
            print(f"ok: bad sample #{i} caught ({len(errs)} error(s))")

    print()
    if failures:
        print(f"SELFTEST: {failures} failure(s).")
        return 1
    print("SELFTEST: all passed. The linter catches what it should and clears what it should.")
    return 0


# --- Entry point ------------------------------------------------------------

def main(argv):
    args = [a for a in argv[1:] if a != "--strict"]
    strict = "--strict" in argv[1:]

    if "--selftest" in args:
        return selftest()

    paths = [a for a in args if not a.startswith("--")]
    if paths:
        with open(paths[0], "r", encoding="utf-8") as fh:
            text = fh.read()
    else:
        text = sys.stdin.read()

    return report(text, strict=strict)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
