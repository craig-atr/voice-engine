# Voice Engine

A folder-based specialist that drafts **email in your own voice** — and gets more like you over time.

Built for Clief Notes Weekly Comp #8 (The Wildcard). I'm the client: **Craig Howard**, owner of **Atomic Tattoo Removal** (Wrentham, MA). The problem — the customer-care and business email I write all day comes back generic and corporate when I hand it to an AI, so I rewrite it from scratch. This folder fixes that by holding *my* voice, pulled from my own sent email. Full brief at [`brief.md`](./brief.md).

## The core idea
A model can't remember you between chats. So "it learns my voice" doesn't mean the model changes — it means **the folder gets smarter and you reload it each session.** The intelligence lives in three places working together:
- **Rules** you can articulate (`rules.md`)
- **Examples** you can't fully articulate but the model can pattern-match (`examples.md`)
- A **feedback loop** you run that feeds corrections back in (`reference/`)

## Folder map (ICM structure)
```
brief.md          ← the client brief (read this first)
identity.md       ← who the specialist is + how it operates each session
rules.md          ← how I write (tone, diction, rhythm, openers/closers)
examples.md       ← gold samples + good-vs-bad contrast pairs
reference/
  voice-audit-prompt.md  ← the engine: extracts your voice from your sent email
  corpus-guide.md        ← how to gather email + keep private content private
  corrections-log.md     ← log every fix you make
  retrain-ritual.md      ← the weekly step that turns fixes into a sharper profile
  changelog.md           ← versioned history (proof the voice improves)
  anti-patterns.md       ← the generic "AI voice" tells to avoid
  voices-i-admire.md     ← optional directional inspiration
  raw-corpus/            ← your real email (git-ignored, never published)
README.md         ← you are here
```

## Quickstart — using it to draft
1. Load `identity.md`, `rules.md`, and the 3–5 most relevant `examples.md` into your AI chat.
2. Give it the ask: type (customer reply / clinical / scheduling / B2B / follow-up), recipient, purpose, key points, length.
3. It returns a send-ready draft plus a one-line `Voice check:` naming the traits it leaned on.
4. Edit. Log anything you changed in `reference/corrections-log.md`.

**Example ask:** *"New customer reply. She asked how much to remove a small wrist tattoo and whether it scars. Small tattoo pricing, mention consult. Keep it short."* → draft comes back in Craig's voice, prices left as `[[…]]` if not provided.

## The improvement loop (why it learns)
1. **Draft** with the current folder.
2. **Fix & log** — note what you changed and why.
3. **Promote** low-edit drafts into `examples.md` as new gold.
4. **Contrast** — turn the sharpest fix into a good-vs-bad pair.
5. **Retrain** (weekly) — distill the log into `rules.md`, bump `changelog.md`, clear the log.

Over weeks the gold set grows, the rules sharpen, and drafts need less editing. That delta *is* the learning.

## Make it yours (for anyone forking this)
1. Read `reference/corpus-guide.md` and gather 15–40 of your own sent emails.
2. Run `reference/voice-audit-prompt.md` over them.
3. Paste the result into `rules.md`; add the flagged gold examples (sanitized) to `examples.md`.
4. Rewrite `brief.md` for your own problem. Start drafting and running the loop.

## Privacy
Real email never gets published. It lives in the git-ignored `reference/raw-corpus/`. Only sanitized excerpts (names → `[Name]`, no addresses/numbers/confidential details) ever enter `examples.md`. See `corpus-guide.md`.
