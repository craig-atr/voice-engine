# Corpus Guide — Gathering Your Writing (Safely)

Your sent email is the richest possible source of your real voice — it's you writing naturally, at volume, for years. This guide covers how to pull it and, critically, how to keep private content out of a public repo.

## Pulling your email
You have a few options, easiest first:
- **Connect your email** to your AI assistant and ask it to collect a batch of your *sent* messages (sent-only matters — you want your words, not replies you received). Ask for a spread: short replies, long emails, a few newsletters, a decline or two. Variety teaches voice better than 40 near-identical messages.
- **Export manually:** most mail clients let you select messages and forward/export. Drop them into `reference/raw-corpus/`.
- **Aim for 15–40** to start. More isn't always better — 25 varied emails beat 200 similar ones.

## The privacy rule (read this before you publish anything)
This repo is going on **public GitHub**. Your real email contains names, addresses, deals, numbers, and things other people said in confidence. None of that can be published.

So the repo keeps two layers separate:
- `reference/raw-corpus/` — your real, un-sanitized email. **This folder is git-ignored** (see `.gitignore`) and never leaves your machine. The audit reads from here.
- `examples.md` — only **sanitized** excerpts: real names → `[Name]`, companies → `[Company]`, strip addresses, phone numbers, dollar figures, and anything confidential. This is what the public sees.

### Quick sanitization checklist
- [ ] Real people's names replaced with `[Name]`
- [ ] Company/client names replaced with `[Company]`
- [ ] No email addresses, phone numbers, or physical addresses
- [ ] No dollar figures, contract terms, or confidential details
- [ ] Nothing that quotes someone else's private message
- [ ] Re-read as if a stranger will see it — because they will

When in doubt, leave it out. The voice survives sanitization; the privacy risk doesn't survive a leak.
