# Spread run — session 1 record (2026-09-01)

Ticket: [#221](https://github.com/seanwinslow28/code-brain/issues/221). Map: [#158](https://github.com/seanwinslow28/code-brain/issues/158).
Predecessor: [`../rules-off-experiment/session-record.md`](../rules-off-experiment/session-record.md).

**The question.** Hold the inputs constant and vary the writer. How much of Arm B's 86%
hand-rewrite survival is the *configuration*, and how much is the *writer*? And is there a
fallback tier if the primary writer is unavailable?

## Design, as ratified in session

Every decision below was put to Sean one at a time and answered before anything ran.

| Decision | Ruling | Why |
|---|---|---|
| Transcript | **#2, `deleted-the-author-modes`** | The only transcript with two known scores on the same words (rules-on control 25%, Arm B 86%). A spread with no anchor is a spread against nothing. |
| Blinding | **No prior hand-rewrite in any arm** | Arm B's 86% was produced blinded. Hand a model the finished prose and it converges toward it, so the spread compresses and you measure who copies best. Verified before firing: no line of `arm-b-sean-final.md` appears in `voice-samples.md`, the corpus, or either bundle. |
| Noise floor | **Two identical Opus 5 arms, hidden from the reader** | Arms A and B differed in *prompt*, never in nothing. Without a within-model variance measurement, every vendor gap is uninterpretable. |
| Roster | **7 vendors** | Vendor spread beats sibling spread. Two vendors is one comparison and a possible fluke. |
| Harness axis | **GPT-5.5 in two harnesses** | The only model on this machine reachable both agentically (Codex CLI) and single-shot (API). No Anthropic API key exists, so Opus cannot be run in two harnesses. Arms 3/4 calibrate the offset that lets the single-shot arms be read against the agentic anchor. |
| Sample folding | **One stripped-samples arm on the incumbent** | Turned from an arbitrary trim into a principled one by the #224 finding. Inherits the twins as its noise floor for free. |
| Measurement | **Blind two-stage read, rewrite the winner only, flaw-count on all** | Human ranking degrades past ~7 items; triage-then-rank scales. One survival number on the 86/64/38/25 scale. |
| Closure | **Rank + survival %** | The #163 pattern: close on the machine's evidence, not on the publish. |

## Setup

Identical across all twelve arms: transcript #2, the standing shaping context, the one
claims-locked substance law, `there are no style rules to follow`, and the Substack deliverable
form. Prompt at [`PROMPT.md`](PROMPT.md) (single-shot) and `PROMPT-agentic-*.md` (file-list form).

**The prompt is a faithful reconstruction, not the original.** The Arm B prompt was never saved to
disk; the session record only paraphrased it. It was rebuilt from `content-machine/SKILL.md`'s
standing "The shaping context" spec plus the predecessor record's Arm B description. This is a real
limitation on comparing to 86% and is recorded rather than smoothed over. **Save the prompt with the
run from now on.**

Context bundle: **37,882 words / 56,487 tokens**. The stripped variant is 35,148 words.

## Privacy controls

Every OpenRouter call was pinned to `provider.data_collection: "deny"`, with `zdr: true` where a
zero-retention endpoint existed, and the three Chinese-lab open-weight arms additionally restricted
to a US-host allowlist (Fireworks / Together / BaseTen / DeepInfra / Parasail / Modal / CoreWeave).
Verified empirically before the run, not assumed: a probe call to GLM 5.3 under those flags routed
to Fireworks, not Z.AI.

**Gemini has no ZDR endpoint at all** and hard-failed the first attempt with HTTP 404. It ran on the
fallback tier — non-collecting, first-party Google — which is a real and deliberate weakening of the
control for that one arm.

## The arms

| # | Model | Harness | Samples | Result |
|---|---|---|---|---|
| 1 | Claude Opus 5 | Claude Code subagent | full | 914 w |
| 2 | Claude Opus 5 | Claude Code subagent | full | 945 w — **hidden twin** |
| 3 | GPT-5.5 | Codex CLI (agentic) | full | 872 w |
| 4 | GPT-5.5 | OpenRouter (single-shot) | full | 764 w |
| 5 | Gemini 3.1 Pro | OpenRouter | full | 775 w (ZDR fallback) |
| 6 | Grok 4.6 | OpenRouter | full | 628 w |
| 7 | Kimi K3 | OpenRouter (Fireworks, US) | full | 1,012 w — on retry |
| 8 | GLM 5.3 | OpenRouter (DeepInfra, US) | full | **FAILED — see finding 2** |
| 9 | DeepSeek v4 Pro | OpenRouter, US host | full | 928 w |
| 10 | Mistral Large 2512 | OpenRouter | full | 670 w |
| 11 | Claude Opus 5 | Claude Code subagent | **stripped** | 1,062 w |
| 12 | Qwen3.6 35B-A3B | local Ollama @ 64K | full | 720 w — **$0** |

## Findings before the read

These do not depend on Sean's ranking and are already banked.

**1. A $0 local fallback tier exists, with two conditions nobody had established.**
qwen3.6 35B-A3B held all 56,245 prompt tokens at 64K context on a 48 GB machine (24.1 GB resident)
and wrote a real 720-word essay in 182 seconds. But the stock `qwen3.6_35b-a3b-32k` Modelfile caps
context at **32K and could not have held the bundle at all** — the model's native limit is 262,144,
so the cap is ours, not the model's. And on the first attempt it burned all 4,000 output tokens
reasoning and returned an **empty string**; it needed 20,571 characters of thinking headroom before
a single word of essay appeared.

**2. Reasoning models are a live blind spot in headless drafting, and it bills for nothing.**
Four of the five thinking models returned zero words on the first pass against an 8,000-token output
budget that was generous for every non-reasoner — the essay is ~900 words. The reasoning is not
inside that budget in any useful sense: Kimi needed **63,933 characters** of thinking before its
first word of prose, and the local model needed 20,571. Raising the ceiling to 32,000 recovered
Kimi (1,012 w, $0.606, the most expensive arm) and the local arm (720 w, $0).

**GLM 5.3 is a genuine negative result, not a mis-configuration.** Two attempts:

| Attempt | Cap | Completion tokens | Reasoning chars | Finish | Words | Cost |
|---|---:|---:|---:|---|---:|---:|
| 1 | 8,000 | 8,000 | — | cap | 0 | $0.098 |
| 2 | 32,000 | **32,000** | **135,628** | `length` | 0 | $0.194 |

Quadrupling the budget quadrupled the spend and produced the same zero words. It does not terminate
on this task. **$0.291 for nothing**, and no third attempt was made unilaterally.

The generalizable defect: a drafting harness that treats `max_tokens` as an essay budget will
silently emit empty drafts and real invoices on any reasoning model, and a runaway reasoner will
consume the entire ceiling you give it. Grok 4.6 masked this only because xAI's endpoint accounts
for reasoning outside the cap. Nothing in the content machine currently guards either case.

**3. Five of the first six arms independently reached for the same beat.** Different vendors,
different harnesses, no shared context beyond the transcript, and the sisters moment landed in the
title or subtitle of nearly all of them. The transcript's strongest beat appears to dominate writer
choice — which, if it holds across the full twelve, says the interview matters more than the writer.

**4. The harness built a privacy exposure and it was caught before the first commit.**
To give the single-shot arms byte-identical input, the run assembled `context-full.md` — a verbatim
concatenation of the interview transcript, all six corpus files, `voice-samples.md` and
`reference-universe.md`, **every one of them git-ignored** — into
`vault/20_projects/substack-studio/spread-run/`, which is a **tracked public path**. 37,882 words of
private material, one `git add -A` away from a public repo. Nothing was committed; the directory was
still entirely untracked when this was found.

Fixed the way #160 and #169 fixed theirs: three targeted rules under the `.gitignore` private-layer
block, then a **canary** proving `git add` actually refuses all three, then a probe of 16 randomly
sampled private strings against `git grep` (tracked files only) — 15 clean. The 16th is pre-existing
and runs the other way: `corpus/03-prose-anchors.md` was built *from* Sean's published Start Here
page, so his own published prose appearing in a tracked page is not a leak.

The generalizable rule: **a derived file inherits the privacy class of its most private input**, and
nothing in the machine enforced that. Assembling private files into a bundle silently stripped their
ignore rules, because ignore rules attach to paths and this was a new path.

## Instruments

`analyze.py` (writing-critique dashboard, verified in-session: it reproduces the predecessor record's
Arm B row exactly), `origin_check.py` (claims tier, advisory per L8), `diff_pieces.py` for the
survival number on the winner. All $0, all local. Costs recorded from live API responses in
[`costs.json`](costs.json), never estimated. **Total spend $1.3988** against a ~$1.00 estimate; the
overrun is Kimi's $0.606 and GLM's $0.291 of nothing.

## Open

- Sean's blind two-stage read via [`console.html`](console.html) — **11 arms, letters A–K** —
  published as an artifact. Letters sealed in `SEALED-MAPPING.json` (seeded shuffle, not opened
  before the read).
- **Whether GLM 5.3 gets a third attempt** with `reasoning.effort` lowered rather than the budget
  raised. Sean's call: it would change the mechanism rather than the budget, which makes that arm
  non-comparable to the other ten, so the honest default is to keep the negative result.
- His hand-rewrite of the winner, then `diff_pieces.py` for the survival %.
- **De-blinding hazard, recorded:** word counts per arm were visible in session before the read.
  They were removed from the console's blind view and moved behind the reveal, but a determined
  reader could still match a remembered length to a draft. Next run: do not surface per-arm word
  counts until after ranking.
