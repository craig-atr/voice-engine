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

## Before & After: the same ask, with and without the folder
To show what the folder actually buys me, I ran each task two ways. **Before** = a brand-new Claude session with *no* knowledge of my voice — just the task and a link to my site (the exact prompt is shown so you can reproduce it). **After** = the same task drafted with Voice Engine loaded. Same facts, same customer. The difference is the voice.

---

### Example 1 — New customer asks about pricing

<sub>**Before** generated from this prompt in a fresh session: *"I own a tattoo removal business. Write an email replying to a potential customer named Alishia. She has a small tattoo and is asking about pricing. Here's my website for the details: https://atomictattooremoval.com"*</sub>

❌ **Before — generic Claude (no voice):**
> Hi Alishia,
>
> Thanks so much for reaching out — I'd be happy to help.
>
> Great news on a small tattoo: those are usually the most affordable to remove, since pricing is based mainly on the size of the piece. A few other things factor in too, like the ink colors, how old the tattoo is, and the number of sessions it ends up needing, which is why I like to take a quick look before quoting an exact price. I want the number I give you to be honest and accurate, not a guess.
>
> The easiest way to get you a real estimate is one of two ways:
>
> 1. Text me a photo of the tattoo at (508) 203-1342 and I'll send back an honest estimate — no pressure, no obligation.
> 2. Book a free 30-minute consultation, where I'll look at it in person, walk you through the process, and give you a personalized plan and pricing. You can book here: https://atomictattooremoval.com/book-consultation
>
> Either way there's zero obligation, and you'll always be texting with me directly — I'm the owner, not a call center.
>
> Looking forward to helping you out!
>
> Best,
> Craig Howard

✅ **After — Voice Engine:**
> **SUBJECT: Tattoo Removal**
>
> Hi Alishia,
>
> Small tattoos (smaller than a palm) are $150 a session.
>
> Avg # of sessions for complete removal is 6-12, and you wait 6-8 weeks between sessions to give your skin time to heal. This means it could take a year or more to fully remove your tattoo. Cover ups take less sessions — it's dependent on your tattoo artist and the design.
>
> There are discounts up to 15% if you buy a package of 3 or 5 sessions up front. We also have payment plans through Cherry — you can check what you'd be approved for at https://atomictattooremoval.com/payment-plans
>
> You can book a consultation here: https://atomictattooremoval.com/book-consultation or text us your availability at 508.203.1342
>
> Let me know if you have any questions.

---

### Example 2 — Checking in on a client's healing

<sub>**Before** generated from this prompt in a fresh session: *"I own a tattoo removal business. Write a friendly email to a client named Sam, checking in to see how his healing is going after his last laser session."*</sub>

❌ **Before — generic Claude (no voice):**
> Hi Sam,
>
> I hope you're doing well! I wanted to check in and see how you've been healing since your last laser session. It's normal to notice some redness, swelling, or tenderness in the days afterward, and most of that should be settling down by now.
>
> A few quick reminders as the area continues to heal: keep it clean and moisturized, avoid picking at any scabs or blisters, and protect the spot from direct sun (or use a good SPF if it's going to be exposed). If you have any concerns or notice anything unusual, don't hesitate to reach out.
>
> How is everything looking and feeling on your end? I'd love to hear how it's going, and we can start thinking about scheduling your next session whenever you're ready.
>
> Take care,
> [Your Name]
> [Business Name]
> [Phone / Contact Info]

✅ **After — Voice Engine:**
> **SUBJECT: Checking in**
>
> Hi Sam,
>
> Just wanted to check in and see how the healing is going after your last session. Any blistering or anything you're not sure about?
>
> Feel free to send me a picture if you want me to take a look. Let me know.

---

### Example 3 — Re-booking a client who's gone quiet

<sub>**Before** generated from this prompt in a fresh session: *"I own a tattoo removal business. Write an email to a client named Bruna. She has 2 prepaid sessions left and I haven't seen her in about 3 months. Remind her and tell her how to book the next one. My booking page: https://atomictattooremoval.com/book-consultation"*</sub>

❌ **Before — generic Claude (no voice):**
> Hi Bruna,
>
> It's been a little while since we last saw you, and we wanted to check in! You still have 2 prepaid sessions remaining with us, and we'd love to help you keep your progress moving along.
>
> Tattoo removal works best with consistent sessions, so now is a great time to get the next one on the calendar.
>
> Whenever you're ready, you can book your next appointment here:
> https://atomictattooremoval.com/book-consultation
>
> If you have any questions or want to talk through your treatment plan, just reply to this email — we're happy to help.
>
> Looking forward to seeing you again!
>
> Warm regards,
> Atomic Tattoo Removal

✅ **After — Voice Engine:**
> **SUBJECT: Your remaining sessions**
>
> Hi Bruna,
>
> It's been about 3 months since your last session, so I wanted to check in. You've still got 2 sessions left on your package.
>
> Whenever you're ready, you can book your next one here: https://atomictattooremoval.com/book-consultation — or just text me your availability at 508.203.1342.
>
> Let me know what works for you.

---

**What to notice — these aren't cherry-picked, they're the failure modes the folder fixes:**

- **Example 1:** the generic draft *never gives the price.* It deflects — "I like to take a quick look before quoting" — and pads with "Thanks so much for reaching out" and "no pressure, no obligation" (twice). I actually quote the $150 up front. It also invented a "free 30-minute consultation" I never mentioned. The Voice Engine draft answers the question in the first line.
- **Example 2:** opens with "I hope you're doing well!", turns a 30-second check-in into an aftercare lecture, and — the tell — didn't even know who I am, signing off "[Your Name] / [Business Name]". Mine is three lines and sounds like me texting a client.
- **Example 3:** slips into corporate "we," adds filler ("Tattoo removal works best with consistent sessions"), and signs off "Warm regards, Atomic Tattoo Removal." I write as "I," skip the filler, and close with "Let me know what works for you."

Same model, same facts. The only variable is whether it read the folder. That gap — long/generic/evasive → short/specific/me — *is* the product.

## Make it yours (for anyone forking this)
1. Read `reference/corpus-guide.md` and gather 15–40 of your own sent emails.  (I use a Gmail mcp, instead of copying and pasting)
2. Run `reference/voice-audit-prompt.md` over them.
3. Paste the result into `rules.md`; add the flagged gold examples (sanitized) to `examples.md`.
4. Rewrite `brief.md` for your own problem. Start drafting and running the loop.

## Privacy
Real email never gets published. It lives in the git-ignored `reference/raw-corpus/`. Only sanitized excerpts (names → `[Name]`, no addresses/numbers/confidential details) ever enter `examples.md`. See `corpus-guide.md`.
