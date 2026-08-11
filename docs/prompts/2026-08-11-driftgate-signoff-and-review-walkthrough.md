# Driftgate — walk Sean through sign-off and the canon review (teaching session)

**This session is not a build session.** Nothing needs to be implemented. The job
is to walk Sean through three things he owns, in a way he can repeat alone next
time, and to leave him understanding *why* each step exists rather than just
which command to type.

Read the whole brief before your first action.

## Who you are working with, and the format that actually works

Sean is a product manager, not a developer. He has said plainly: **parsing code
inside a markdown file is hard for him to grasp, and he wants to see what he is
looking at.** Take that literally.

- **Explain every piece of jargon in plain language before he has to act on it.**
  "Append-only", "snapshot", "provenance", "enforcement-gap register", "decay",
  "supersede" — each of these has a real meaning and he should end the session
  able to define them.
- **Do not dump code, JSONL, or YAML into chat and ask him to read it.** If he
  needs to see the state of something, render it.
- **He is trying to learn the process, not just complete it.** When he asks "what
  do I do", answer with the reason first and the command second.

Consider opening with `/teach` (a user-level, multi-session skill at
`~/.claude/skills/teach/`) if he wants the learning tracked across sessions — it
treats the working directory as a teaching workspace and keeps state between
sessions. It is user-invoked only; suggest it, do not auto-invoke it.

## FIRST ACTION — build him a review console before you ask him anything

The single highest-value thing you can do at the start of this session is turn
the review queue into something he can actually read. Use the **Artifact tool**
to publish a self-contained HTML page (private by default, on claude.ai).

Load the `artifact-design` skill first, as its instructions require.

The console should contain, for each of the 17 pending items:

- The **proposed value**, large and readable — this is the fleet's guess.
- **Where it came from**: which frame, which region of that frame, the evidence
  id, and which era.
- **Side-by-side with Sean's ratified canon** wherever one exists. Read the
  ground truth from `~/Code-Brain/anima/characters/*/character.yaml`. Where a hex
  is involved, **show the actual colour swatches next to each other** — the
  extraction's guess and the canon value. This is the single change that makes
  the review possible for him rather than tedious; several proposals are hex
  values a few points off, and that is invisible in text.
- Three choices per item — **accept / correct / skip** — and, as he picks, the
  page accumulates the exact commands his choices imply, in one copy-paste block
  at the bottom.

**The page must not execute anything.** It is a decision aid. Execution happens
in the terminal, or you run the commands for him afterwards *on his explicit
instruction* — see the guardrail about that below.

If a plain HTML artifact is not the right shape for something, `mcp__visualize__show_widget`
renders inline in chat and is fine for smaller views (a single comparison, a
diagram of the proposal→canon flow).

## The mental model to teach — the six ideas underneath everything

Do not lecture all six up front. Introduce each one at the moment it becomes
relevant to what he is doing.

1. **A proposal is not canon.** The fleet writes facts in states `observed` or
   `inferred`. Those are guesses with receipts. `confirmed` and `declared` are
   the creator's, and the code refuses to let an agent write them (master
   forbidden list items 14 and 15). This is the whole architecture in one
   sentence: *the system must never become the author of its own ground truth.*
2. **Correcting is the interesting half.** Two separate spikes landed on the same
   boundary: **models own structure and judgement, stated canon owns fine
   attributes.** The extraction is usually right that there *is* a palette fact
   and right about which frame shows it — and wrong in the last few digits. When
   Sean corrects a value, the structure stands and the number becomes his.
3. **Nothing is ever edited or deleted.** A correction is a *new event* appended
   after the old one. The original proposal stays in the log forever. That is
   what makes a disagreement inspectable later instead of vanishing.
4. **Decay.** A confirmed fact goes stale after `decay_after_installments` (12,
   provisional). It then *displays* as `inferred / needs_reconfirmation` while
   still being his value underneath. His first confirmation decayed immediately —
   see G53 below; that is a known modelling error, not something he did wrong.
5. **The enforcement-gap register** (`governance/enforcement-gaps.md`) is the
   file that says which company rules are actually enforced by code and which are
   only written down. Rows are **appended and superseded, never edited** — when a
   row overclaimed, a new dated row corrects it and the old one stays visible.
   Explain why: a governance file that quietly rewrites itself is worthless.
6. **Sign-off** means Sean has read a governed change and accepts it. It is a
   checkbox in a change-proposal file, and it is the only thing that makes the
   change legitimate. He is signing the *claims*, not the code.

## Where things stand (verify before relying on any of it)

Company repo: `seanwinslow28/driftgate`, private, local clone at
`/Users/seanwinslow/Code-Brain/driftgate`. Verify with `gh` and pass
`-R seanwinslow28/driftgate` or you will read code-brain's issues by mistake.

- **Ticket #7 is CLOSED** (onboarding extraction). Three commits: `c79a7c4`
  (build), `a2463d9` (external-audit fixes), `fb44e94` (first confirmation).
  223 tests, ruff clean, validator 0 errors stateless and `--diff a632f31`.
- **The ledger exists and has real content.** Tenant `sean`, series
  `ser-pencil-test`, **29 events, 18 facts, 17 awaiting confirmation.** One
  creator-confirmed fact already landed. Snapshot at time of writing:
  `sha256:37e82a13715fc043855c50b45c8c9b37a2071aab8d0f908d764995b4e5af7335`.
- Read it with `python -m driftgate.onboarding_cli review --creator sean
  --series pencil-test --current-ordinal 69`. **Always pass `--current-ordinal 69`**
  — omit it and you silently read the series at the wrong point (register G44).
- Next build frontier is **#8** (D2 pipeline state machine). Not this session.

## THE THREE THINGS SEAN OWNS

### 1. Sign off the change proposal

`driftgate/governance/change-proposals/2026-08-10-onboarding-extraction.md`.

It landed on `main` unsigned, consistent with #5 and #6. Walk him through what he
is actually agreeing to — do not just point at the file:

- Five register rows moved to `enforced`; **three others were narrowed** because
  they claimed more than the code delivered (G29, G43, G26). Show him one
  narrowing concretely so he understands what an overclaim looks like.
- Ten new gaps, G43–G54. **Two are unfixed on purpose** — G46 and G52, meaning a
  bad extraction pass cannot be withdrawn through the API. Both happened during
  the build; the remedy both times was moving files by hand. He should sign
  knowing that, or decline until it is fixed.
- The cost datapoint was **published wrong and republished twice**. He should
  understand why (thinking tokens billed but uncounted; then the wrong unit for
  "installment") because it is the ticket's actual deliverable.

Done looks like: the sign-off checkbox filled in with his name and the date, a
commit, and a push.

### 2. Read and decide the 17 pending canon facts

This is the librarian role card's `review_sample` commitment: he reads **every**
proposed canon event on his own series during the dogfood slice. #7's acceptance
only needed one; the card asks for all of them.

Regenerate the queue rather than trusting the file on disk — event ids change
whenever the ledger is rebuilt, and a stale command will fail or, worse, target
the wrong event. The current queue file is at
`~/.driftgate/review/2026-08-10-pencil-test-queue.md`.

For each item he can **accept**, **correct**, or **leave it** (an unconfirmed
proposal simply stays a proposal and never reads as canon — leaving something is
a legitimate answer, not a deferral).

### 3. Decide where two untracked gaps live

**G45** (nothing reconciles two subject ids that mean one character — related to
G33's unbuilt rename/alias event) and **G53** (an installment is modelled as one
artifact, so a two-act short became 70 installments and his confirmation decayed
on arrival) have **no child ticket on the wayfinder map**. The register records
that honestly, but an untracked gap has no owner.

G53 is the one that matters and it is a design question, not a bug: **what is an
installment?** The extraction test and the cost ceiling both mean a *publication
unit* — an episode, a post. The plan modelled it as a file. Until that is
settled, decay fires against the wrong unit and cost projections have no stable
denominator. It plausibly belongs to #8 or #18. Help him decide; then file.

## Hard guardrails — the things that cannot be undone

- **Never run `onboarding_cli run` again on this series.** It would append a
  second copy of every fact. The ledger is append-only and there is no undo
  (G46/G52). If a re-run is genuinely needed, that is a conversation first.
- **A confirmation is irreversible.** A wrong one is fixed by appending a
  *superseding* event, not by removing anything. Make sure he understands the
  cost of a mistake before he starts, not after.
- **Do not hand-edit anything under `~/.driftgate/data/`.** That is the creator
  data root. Reading is fine; editing corrupts the hash chain and the ledger will
  refuse to load.
- **If you run a confirm command on his behalf, say so and record it.** The event
  will read `actor: creator/sean` regardless of who typed it — that is the G28
  seam, an unauthenticated creator action. The first confirmation was
  fleet-executed on his instruction and the register says so. Keep that honest.
- **Creator content never enters the repo.** No extracted fact values, no
  character names, no frame filenames in any tracked file. `~/.driftgate/` and
  `tenants/` are gitignored; keep review artifacts outside the repository.

## Conventions

Company work tracks in driftgate issues, not code-brain tickets. Research
artifacts go to `code-brain vault/20_projects/research/` (commit the vault
yourself on the MBP). Governed changes to `roles/`, permission profiles, the
register, or the schemas route through `governance/change-proposals/`; skills and
constitution rules route through `proposals/`. Validate with
`python3 /Users/seanwinslow/Code-Brain/groundwork/scripts/validate.py .` and
`--diff a632f31`. Keep CI green: `uv run ruff check .` and `uv run pytest`
(currently 223).

## How to end the session

Sean should be able to answer, in his own words: what a proposal is and why the
fleet cannot confirm one; what happens to the old value when he corrects
something; why his confirmation showed as stale; and what he was signing when he
signed. If he cannot, the session did the tasks but not the job.
