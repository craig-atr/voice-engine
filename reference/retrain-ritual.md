# Retrain Ritual

This is the "training run" — the human-in-the-loop step that makes the system improve instead of bloat. Do it on a cadence (weekly to start, then whenever the corrections log fills up). Takes ~15 minutes.

## The ritual
1. **Read the week's corrections.** Open `corrections-log.md` and read every entry.
2. **Spot the patterns.** Is the same fix showing up more than once? That's not a one-off — it's a missing rule.
3. **Update `rules.md`.** Fold recurring lessons into the right section. Keep it tight — if a rule is already covered, sharpen the wording instead of adding a duplicate.
4. **Promote gold.** Any draft this week you barely had to edit? Sanitize it and add it to `examples.md`. Low-edit drafts are your best future examples.
5. **Add a contrast pair.** Take the single sharpest before/after from the log and add it to the contrast pairs in `examples.md`.
6. **Prune.** Remove any example or rule that's gone stale or that you keep overriding. A lean folder beats a bloated one — the model reads all of it every time.
7. **Bump the version.** Update `changelog.md` and the version line in `rules.md`.
8. **Clear the log.** Archive the distilled entries so next week starts clean.

## Why this matters
A folder can't learn on its own — the model has no memory between sessions. *You* are the training loop. This ritual is the difference between a system that gets sharper every week and a static prompt that plateaus. It's also the part judges will recognize as real methodology.
