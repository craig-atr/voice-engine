# Voice Audit Prompt

This is the engine that "learns your voice." Run it once to build your first `rules.md` and `examples.md`, and re-run it whenever you've gathered a fresh batch of writing. It's also what makes the system reusable by anyone — a stranger points it at their own sent mail and gets their own profile.

## How to run it
1. Gather 15–40 of your own sent emails/newsletters (see `corpus-guide.md` for how to pull them, including connecting your email so they can be read in bulk).
2. Paste the batch where indicated below and send the whole thing as one prompt.
3. Review the output, correct anything that isn't right, and paste it into `rules.md`. Pick the best raw samples it flags and add them (sanitized) to `examples.md`.

---

## The prompt

```
You are a forensic writing analyst. Below are real emails and newsletters I have
written. Your job is to reverse-engineer my voice precisely enough that someone
could draft new emails indistinguishable from mine.

Do NOT compliment the writing or summarize what the emails are about. Analyze HOW
I write, not WHAT I wrote. Quote short snippets as evidence for every claim.

Produce these sections:

1. TONE & PERSONALITY — register, warmth vs. efficiency, emotional temperature,
   and one sentence describing how I come across. Evidence required.

2. DICTION — the specific words and phrases I reach for repeatedly (list 10–20 with
   counts/examples). Separately, flag any words I clearly avoid.

3. RHYTHM & STRUCTURE — typical sentence length and variation, use of fragments,
   one-line paragraphs, whether I front-load the point or build to it, paragraph
   length.

4. OPENERS & CLOSERS — every greeting and sign-off I use, with frequency. How I
   open and close longer/newsletter pieces specifically.

5. FORMATTING HABITS — em dashes, lists, emoji, emphasis, how I handle links.

6. TELLS — the 5–10 things that, if missing, would make a draft NOT sound like me.
   These are my fingerprint.

7. BANNED — phrases or moves that appear NOWHERE in my writing and would break the
   illusion (so the drafter knows to avoid them).

8. GOLD CANDIDATES — pick the 3–5 emails from the batch that are the most
   characteristically "me" and say why each one is a strong example.

Format the output as clean Markdown I can paste directly into a rules file.

Here is my writing:
[[PASTE 15–40 EMAILS HERE]]
```

## After you run it
- Edit the output — you know your voice better than the model. Trust your ear over its analysis.
- Paste sections 1–7 into `rules.md`, replacing the placeholders.
- Take the GOLD CANDIDATES, sanitize them, and add to `examples.md`.
- Log the version bump in `changelog.md` (e.g. v0.1 → v0.2).
