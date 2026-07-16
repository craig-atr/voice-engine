# ICM — Interpretable Context Methodology

**What this file is.** A portable explanation of the methodology behind this project, plus a runnable audit-and-plan procedure. It has two audiences:

1. **A human** who wants to understand how Voice Engine is built and why.
2. **An agent** pointed at *any* project and told: *"read ICM.md, audit this project against it, and produce a ranked improvement plan."*

If you are that agent, skip to **Part 5 (The Audit)** and **Part 6 (The Plan)** — Parts 1–4 are the reference you audit against. Cite `file:line` for every finding. Do not invent compliance; if you can't point at the file that satisfies a check, it fails.

> **Source.** The methodology is from *Interpretable Context Methodology* (arXiv:2603.16021v2). Sections 1–6 are cited inline. The three "field lessons" in Part 3 come from the Comp #8 judging that read 32 builds against this methodology at the code/word level — they are the practical test of whether an ICM build actually holds up, not just whether it's shaped right.

---

## Part 1 — What ICM is

**Core thesis (§1):** *replace framework-level orchestration with filesystem structure.* Instead of writing code that coordinates specialized agents passing context around, you use the **folder structure as the program** and **markdown files as the prompts.** One agent reads different context at each point instead of many agents coordinating through code. The filesystem does the work a framework would otherwise do.

Two consequences make this powerful:
- **The instruction set and the documentation are the same artifact (§3.3).** There is no hidden orchestration layer to reverse-engineer. What you read is what runs.
- **The system is observable by default.** No logging layer, no dashboard — the state is files on disk, diffable in git.

### The two shapes ICM takes

An auditing agent must first recognize *which shape* it's looking at. Both are ICM; the checks differ slightly.

| Shape | Looks like | Example |
|---|---|---|
| **A. Multi-stage pipeline** | Numbered stage folders (`01_research/`, `02_script/`, …), each with a `CONTEXT.md` contract, `references/`, and `output/`. One run flows stage → stage. | The paper's canonical form; `project-starter/workflows/*/stages/*`. |
| **B. Single-specialist folder** | One folder that *is* one specialist: `identity.md`, `rules.md`, `examples.md`, `reference/`, `README.md`. No stages — the whole folder loads to do one job. | **This project (Voice Engine).** The Clief Notes competition builds. |

Shape B is a **single stage** of Shape A, extracted and hardened. The principles below apply to both; where a check is shape-specific, it's marked **[A]** or **[B]**.

---

## Part 2 — The principles (what you audit against)

### 2.1 The five design principles (§3.1)

1. **One stage, one job.** Each unit reads a defined input, transforms it, writes a defined output (Unix philosophy). A file or stage that does two jobs is a smell.
2. **Plain text as the interface.** Everything passes through markdown/JSON. "Any tool that can read a text file can participate."
3. **Layered context loading.** Load only what the current job needs. *Less irrelevant context = better model performance.* Bloat is a defect, not a convenience.
4. **Every output is an edit surface.** Intermediate outputs are files a human can open, read, edit, and save before the next step. If a human can't intervene at a boundary, there's no gate there.
5. **Configure the factory, not the product.** Set the workspace up once (the stable rules/reference); each run produces a new deliverable from the same configuration. Don't hand-tune per run.

### 2.2 The five-layer context hierarchy (§3.2)

The single most useful lens for an audit. Every file in an ICM project should be classifiable into exactly one layer, and layers 3 and 4 must not be confused.

| Layer | Name | Role | The model should… |
|---|---|---|---|
| 0 | `CLAUDE.md` / identity | Global identity: which workspace, what structure, where things are | know who it is |
| 1 | workspace `CONTEXT.md` | Routing: given intent, which stage/mode handles it | know where to go |
| 2 | stage `CONTEXT.md` | The contract: **Inputs / Process / Outputs** | know this job's boundaries |
| 3 | **reference** ("the factory") | Stable across runs: voice rules, design system, conventions | **internalize as constraints** |
| 4 | **working artifacts** ("the product") | Unique per run: prior outputs, source material | **process as input** |

**The Layer 3 / Layer 4 split is the heart of it.** Layer 3 is configured once and is *constraint*; Layer 4 is produced each run and is *data*. Mixing them — e.g., baking a specific run's content into the reued rules — breaks reusability. (In Shape B, `identity.md` = Layer 0, `rules.md`/`examples.md`/`reference/` = Layer 3, and the user's actual email ask + draft = Layer 4.)

### 2.3 Deterministic structure vs. model prose

ICM deliberately splits what's enforced by **structure/code** from what's guided by **prose**:

- **Deterministic:** stage sequencing (folder numbering), context scoping (folder hierarchy + explicit Inputs tables), state (files on disk), coordination (one output = next input). *The filesystem enforces these; the model cannot drift past them.*
- **Prose:** the Process instructions, the reference material (voice/style/conventions). *The model interprets these.*

The audit question this raises is the hinge of Part 3: **is a given "must" enforced by structure/code, or only requested in prose?**

### 2.4 Human-in-the-loop (§3.3, §4.5)

- **Review gates** at every stage boundary; **edit surfaces** (the output is an editable file); **mixed-initiative** — the human can invoke, adjust, and terminate at natural breakpoints.
- Expect a **U-shaped editing pattern**: heavy human editing at stage 1 (creative direction), light in the middle (constrained by anchors), heavy again at the end (alignment/debugging). Stage-1 edits are judgment; final-stage edits are debugging. A build that removes the human from the *judgment* steps has misplaced the automation.

### 2.5 The edit-source principle & accretion (§6.3)

The forward-looking core: when output is wrong, **don't patch the output — trace the problem back to the source file and fix that** (the voice guide, the stage contract, the reference). Over time the workspace should **"improve its own source files, incorporating the patterns it learns from human corrections."** A build that only patches outputs never learns; a build with a correction→source loop compounds.

---

## Part 3 — The three field lessons (the "did it actually work" test)

Shape is necessary but not sufficient. Thirty-two ICM builds were read against these three lines; they are the fastest way to tell a real build from a well-organized promise. **An auditing agent should grade every project on all three.**

### 3.1 Enforcement — *"A must in markdown is a request. A must in code is a constraint."*
A rule written only in prose is something the model is *asked* to honor and can drift past. The strong builds moved their invariants into **code with a self-test**: a `check.py` (or equivalent gate) that fails a bad output out loud.
- **Look for:** a script that compiles the project's stated rules into a deterministic check; a self-test / fixture corpus proving the check catches violations and clears good cases.
- **Red flag:** critical invariants ("never invent a price," "never expose PII," "always cite a source") exist *only* as prose in a rules file.

### 3.2 Evidence — *receipts of a real run.*
The builds that shipped transcripts, dated logs, and before/after fixes read differently every time. The winner won on this: a real user ran the tool on real work and left a trail anyone could check.
- **Look for:** a real, dated run captured end-to-end; before/after comparisons; a self-test whose passing output is shown; anything a stranger can *verify* rather than take on faith.
- **Red flag:** the capability is described but never demonstrated; all examples are hypothetical.

### 3.3 Accretion — *the folder that learns, actually filled.*
"Nearly everyone designed a memory. Almost nobody shipped one with anything in it." This was the most common promise and the rarest delivery.
- **Look for:** a correction/feedback log with **real dated entries** (not just a template), a changelog showing genuine version history *across time*, a mechanism (retrain ritual, edit-source loop) that turns corrections into source changes.
- **Red flag:** a `corrections-log.md` with only a header row; a changelog where every version is dated the same day (designed for weeks, demonstrated for hours).

> These three map onto the paper: **Enforcement** = §2.3 deterministic vs. prose; **Evidence** = observability-by-default (§1); **Accretion** = the edit-source principle (§6.3). The paper says *what* the structure should be; these lessons test *whether the build cashed the check.*

---

## Part 4 — Worked example: how Voice Engine embodies ICM

Use this as the reference for what a passing Shape-B build looks like. Voice Engine is a single-specialist folder that drafts email in the owner's voice.

| ICM element | Where it lives in this project |
|---|---|
| **Layer 0 — identity** | [`identity.md`](identity.md) — who the specialist is, what it does/doesn't do, the load order and output contract |
| **Layer 3 — reference/factory** | [`rules.md`](rules.md) (the canonical voice: tone, diction, rhythm, dials), [`examples.md`](examples.md) (gold samples + contrast pairs), [`reference/anti-patterns.md`](reference/anti-patterns.md) |
| **Layer 4 — working/product** | the user's per-draft ask and the draft that comes back (not committed; ephemeral per run) |
| **Configure the factory (§3.1.5)** | [`reference/voice-audit-prompt.md`](reference/voice-audit-prompt.md) builds `rules.md` once from real sent email; every run reuses it |
| **Enforcement (3.1)** | [`check.py`](check.py) — compiles the banned-phrase / two-spaces / invented-link / placeholder rules into a self-tested gate (`python check.py --selftest`) |
| **Evidence (3.2)** | the README Before/After pairs (same ask through blank model vs. the folder) + `check.py`'s self-test |
| **Accretion (3.3)** | [`reference/corrections-log.md`](reference/corrections-log.md) (what changed), [`reference/runs-log.md`](reference/runs-log.md) (how much, per draft), [`reference/retrain-ritual.md`](reference/retrain-ritual.md) (the loop), [`reference/changelog.md`](reference/changelog.md) (versioned proof) |
| **Edit-source principle (2.5)** | the retrain ritual: corrections are distilled *into `rules.md`*, not patched per-draft |
| **Canonical source (anti-drift)** | `rules.md` is declared the single source of truth; if another file disagrees, it's the bug |

**Where this project is still weak (the honest read):** Accretion is designed but young — the logs need weeks of *real* dated entries to prove the loop compounds rather than just exists. That's the single highest-leverage improvement, and it's behavioral (use it for real), not structural.

---

## Part 5 — The Audit (agent procedure)

Run this against the target project. Produce one finding per failed check, each citing `file:line`. Grade honestly — a missing thing is a finding, not an omission to be polite about.

**Step 0 — Detect the shape.** Numbered stage folders → **Shape A**. A single specialist folder (identity/rules/examples) → **Shape B**. Note it; it selects the shape-specific checks.

**Step 0b — Template or live project?** Decide whether you're auditing a *starter/template* (meant to be copied and filled per project) or a *live project* (built from one). This changes how you grade Evidence and Accretion: in a template, **empty `output/` and `docs/` folders are correct by design** — they're slots the derived project fills, not missing work. Don't penalize a template for them. Instead, audit the *template's own* trail: does it ship at least one example run so a newcomer sees the shape, and does it have a mechanism (e.g. an improvements/upstream log) for capturing what real projects teach it? Grade a live project on filled logs; grade a template on whether the *slots and the loop* exist. (Learned by auditing `project-starter` and then confirming against a real project built from it — the template looked weak on Evidence/Accretion until the real project showed every slot filled.)

**Step 1 — Map every file to a layer (§2.2).** Build the layer table for this project. Findings:
- Any file that doesn't fit a layer (orphan / unclear purpose).
- **Layer 3/4 contamination:** run-specific content baked into reusable reference, or reusable rules living in per-run output. *This is the most common structural defect.*
- Bloat: reference the model loads every time that isn't earning its tokens (§3.1.3).

**Step 2 — Check the contracts.**
- **[A]** Does each stage `CONTEXT.md` have explicit **Inputs / Process / Outputs**? Do the Inputs actually exist? Does stage N's declared output match stage N+1's declared input? (Broken hand-offs are findings.)
- **[B]** Does `identity.md` (or equivalent) state the load order, what the specialist does/doesn't do, and the output contract?
- **One stage, one job (§3.1.1):** flag any file/stage doing two jobs.

**Step 3 — Grade the three field lessons (Part 3). This is the core of the audit.**
- **Enforcement:** Is there a code gate compiling the project's stated invariants, with a self-test? Or are critical "musts" prose-only? Name the specific invariants that should be enforced but aren't.
- **Evidence:** Is there a real, dated, verifiable run? Or only description? Can a stranger check any claim?
- **Accretion:** Is the memory/log filled with *real dated entries over time*, with a loop that feeds source? Or is it an empty template / same-day changelog?

**Step 4 — Check human-in-the-loop (§2.4).** Is there a real edit surface / review gate at each boundary? Is the human kept in the *judgment* steps and automated out of the mechanical ones (not the reverse)?

**Step 5 — Check anti-drift.** If the same fact/rule lives in multiple files, is one declared canonical? Are there stale placeholders (`[Your name]`, `TODO`, `lorem`), or claims in the README that the code contradicts?

**Output of the audit:** a short table — each check, pass/fail, the `file:line` evidence, and a one-line "what's wrong." Rank findings by leverage (see Part 6), not by discovery order.

---

## Part 6 — The Plan (agent procedure)

Turn findings into a ranked, actionable plan. The discipline is *judgment about leverage*, not a to-do dump.

1. **Rank by leverage, and name ONE primary push.** The single change that most improves the build. Resist listing ten equal items — the best feedback names the one thing. Usually it's whichever of the three field lessons is weakest, because those are load-bearing.
2. **Map each fix to its principle** (which layer / which field lesson) so the *why* travels with the *what*.
3. **Separate structural fixes from behavioral ones.** Some findings are code/file changes an agent can make now (add a `check.py`, split a contaminated reference file, sweep a placeholder, declare a canonical source). Others require *time and real use* (fill the accretion log with genuine dated entries). Say which is which — don't pretend a behavioral gap is a one-commit fix.
4. **Prefer edit-source fixes over output patches (§6.3).** If the project keeps producing a wrong output, the fix is upstream in a source file, not a patch on the artifact.
5. **Make each fix verifiable.** A fix isn't done until something can check it — a self-test, a before/after, a dated log entry. Bake the receipt into the fix.

**Plan template:**
```
## Audit summary
Shape: [A / B]. Overall: [1–2 sentences — the strongest thing, cited to a file].

## The one push
[The single highest-leverage change, and why it beats the others.]

## Findings, ranked
| # | Finding (file:line) | Principle / lesson | Fix | Structural or behavioral? |

## Suggested sequence
[What to do now (structural, agent-doable) vs. what needs real-world mileage.]
```

---

## Appendix — Red-flag cheat sheet

Fast tells that a project *looks* ICM but hasn't cashed the check:

- **Empty memory.** A log or changelog that's all template, or a changelog where every version shares one date. → Accretion failed.
- **Prose-only invariants.** The one rule that must never break ("never invent X") exists only as a sentence. → Enforcement failed.
- **No receipts.** Capabilities described, never demonstrated on a real, checkable run. → Evidence failed.
- **Layer 3/4 contamination.** A specific run's content welded into the reusable reference. → Reusability broken.
- **Forked truth.** The same fact in three files, none canonical; drift is inevitable.
- **Bloated context.** Everything loaded every time; nothing scoped. → §3.1.3 violated.
- **Stale placeholders.** `[Your name]`, `TODO`, `lorem` shipped in a file the model reads.
- **Human in the wrong seat.** Automated through the judgment step, human left doing the mechanical one.

> **On humility (from the paper's §4.6):** ICM has no controlled quantitative evaluation yet — its support is theoretical (lost-in-the-middle, chain-of-thought) plus practitioner observation. Audit for *whether the structure and the three lessons hold*, not for a benchmark score. The goal is a build a stranger could pick up, verify, and extend.
