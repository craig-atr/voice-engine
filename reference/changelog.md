# Voice Changelog

Track how the voice profile sharpens over time. Bump the version in `rules.md` to match. This versioned history is the proof that the system *learns* — not just a static prompt.

## v0.1 — 2026-06-26 — Seed
- Initialized from template.

## v0.2 — 2026-06-26 — First audit
- Audited ~18 of Craig's real sent emails across customer-care/clinical and B2B/peer threads (Atomic Tattoo Removal).
- Filled `rules.md`: tone (warm but efficient), diction, short rhythm, `Hi [Name],` openers, "Let me know" closers, two-spaces-after-period fingerprint, banned corporate list.
- Added 7 gold examples (pricing, clinical options, scheduling, follow-up, B2B decline, sponsorship, one-word approval) and 3 contrast pairs to `examples.md`.
- Key tells captured: plain-language parentheticals, numbered options with a marked recommendation, soft declines, one-line replies.

## v0.4 — 2026-07-16 — Enforcement, evidence, and dials (post-comp feedback)
- Acted on the Comp #8 feedback file. Three changes, mapped to the three field lessons.
- **Enforcement:** added `check.py` — a dependency-free linter that compiles the voice rules into a deterministic gate (banned phrases, two-spaces fingerprint, invented-link guard, left-in placeholders) with a `--selftest` corpus that proves it clears real me-drafts and flags generic ones. A "must" in code, not just markdown.
- **Evidence:** added `reference/runs-log.md` — a per-draft ledger with an edit-distance column, so "drafts need less editing over time" becomes measurable. Seeded with the three real v0.3 runs.
- **Dials:** added a tunable Voice-dials table (`rules.md §0`) as a single edit surface for length/formality/warmth, and a Canonical-source rule so the voice can't fork across files.
- Swept the last shipped placeholder ("how [Your name] writes" → "how Craig writes" in `identity.md`).
- Borrowed ideas credited in-file: Nicolás Patrón (canonical source), Sunny Singh (preferences table), Charlie Weeks / Roc Lee (runs ledger).

## v0.3 — 2026-06-26 — First retrain (from real use)
- Used the folder on 3 real asks (pricing, healing check-in, re-booking) and logged 2 corrections.
- Distilled into `rules.md`: added §6 "Standing facts" (booking link, text line, payment plans); pricing replies now give the real removal timeline (a year or more) and the cover-up note.
- Promoted a low-edit healing check-in to a gold example (`examples.md` now 8 gold + 3 contrast pairs).
- Added a "Before & After" section to the README — same asks through a blank Claude vs. Voice Engine, with the prompts so anyone can reproduce it.
