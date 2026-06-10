# VoicePrint — Real-Human Dogfood Runbook

The in-session dogfood (`dogfood-2026-06-08.md`) used a simulated persona to prove
zero-leakage and distinct-voice. Before opening VoicePrint publicly, run it on **2–3
real people who are not you.** This runbook makes that cheap. ~45 min per person.

## Who to recruit

Pick people with *different* voices from each other and from you — e.g. a blunt
engineer, a warm teacher, a terse founder. The more different they are, the better the
test: if all three bundles come out sounding distinct and like them, the tool works.

## What they do (one sitting, ~45 min)

Have them run, in their own Claude (with VoicePrint installed) and a folder open:

1. `/voiceprint-start` — sets the workspace + expectations.
2. `/voiceprint-gauntlet` — react fast to the 10 bad lines (the fun part; start here).
3. `/voiceprint-interview` — answer one-at-a-time, push them for specifics.
4. `/voiceprint-mine` — paste a real chunk of their pre-AI writing.
5. `/voiceprint-synthesize` — generate their `my-voice/` bundle.
6. `/voiceprint-refine` (×1–2) — let it draft, they edit, watch the diff.
7. `/voiceprint-proof` — see the "more you, less generic-AI" read.

## What you check afterward (the two gates)

From the person's `voiceprint/` folder:

**Gate 1 — does it sound like THEM, not a template?** Read their generated
`my-voice/SKILL.md`. Ask them: "does this read like you?" The bar from the in-session
audit: every signature-move row should quote a real line of theirs, and a stranger
should be able to tell two people's bundles apart. If it reads generic, the interview
didn't push hard enough — that's the thing to tune.

**Gate 2 — proof holds.** Their `/voiceprint-proof` should land `closer_to: reader`.
You can re-run it yourself:

```bash
python3 <plugin>/scripts/fingerprint.py \
  --samples <their voiceprint>/my-voice/references/voice-samples.md \
  --draft   <a fresh draft in their voice>
```

**Cross-person leakage check** (the one that matters most): make sure no one's bundle
contains anyone else's content — references, stories, or moves that belong to a
different person. Grep each bundle for the others' signature names/places:

```bash
grep -riE "<person-B's named places/people>" <person-A's my-voice>/   # expect: nothing
```

## What "passing" looks like

- Each person says "yeah, that's me" to their SKILL.md (not "that's generic").
- Each `/voiceprint-proof` lands `closer_to: reader`.
- No bundle leaks another person's content.
- The honest expectation landed: nobody expected one-shot magic; they saw it sharpen.

## If it fails

- **Generic bundle** → the interview craft (`voiceprint-interviewing`) needs to push
  harder on generic answers; or the person gave thin evidence (cold-start).
- **Proof not closer-to-reader** → usually too few/short samples; run more refine rounds.
- **Leakage** → a bug in synthesis (it should build ONLY from that person's `_work/`);
  re-run the zero-leakage check from `synthesis-method.md` and file it.
