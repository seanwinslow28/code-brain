# Canon-extraction test — protocol (pre-registered)

Written 2026-08-08 BEFORE any extraction run. The post-ratification standing
condition on D2/D4/D5: can series canon be EXTRACTED into the two-tier bible
(structured facts + reference exemplars) from real creators' material, at
bounded cost? The council's shared dangerous assumption ("canon is a vibe
with load-bearing exceptions") is the thing under test.

## Corpora (3 creators, per the council's prescription)

- **A — Pepper&Carrot** (external, CC-BY David Revoy): 34 pages across
  episodes 1/2/3 (early era), 11/16 (middle), 34 (late) — spanning ~a decade
  of real published evolution. Sequential product-shaped extraction:
  A1 builds bible v1 from E01-03 blind; A2 receives bible v1 + E11/E16;
  A3 receives bible v2 + E34. Ground truth: official P&C wiki/character
  pages + orchestrator page-level verification.
- **B — Pencil Test** (Sean's shipped Act 1): 14 sequential approved
  keyframes/inbetweens, blind-renamed PT-*. Ground truth: ratified
  character.yaml + turnaround sheets for sean-anchor and claude-mascot.
- **C — Grandmaster** (Sean's in-production short): 12 design stills,
  blind-renamed GM-* and shuffled (filenames leaked states like "wimpy"),
  containing a canonical character transformation and deliberate register
  experiments. Ground truth: character_seeds.yaml + kid/grandma refs.

## Extraction output contract (same for every agent)

Per character: identity block (species/build/silhouette, face/hair,
palette with approximate colors, costume, distinctive features, limb/anatomy
notes) + series-level art-register block (line, color treatment, shading,
lettering) — every fact carrying an evidence pointer (image id). Characters
the extractor believes are the SAME character in different states must be
declared as one character with state/evolution events, with evidence.
Uncertainty must be marked (fact vs guess). Strict structured output.

## Pre-registered bars

1. **Fact precision ≥ 0.80** — sampled proposed facts verified true against
   ground truth/pages. (Hallucinated canon is the product-killing failure:
   the bible IS the gate's ground truth.)
2. **Identity coverage ≥ 0.70** — of the load-bearing identity facts a drift
   check needs (the ground-truth bible's core fields), the proposed bible
   contains them.
3. **Evolution handling** — the known canonical changes (P&C art-register
   evolution across eras + character costume changes; Grandmaster kid
   transformation two-states-one-character; register experiment variants)
   are surfaced as evolution/state events, not silently merged and not
   split into phantom separate characters: ≥2 of 3 corpora handle theirs
   correctly.
4. **Cost ceiling** — measured tokens per corpus, projected to a 50-
   installment catalog at production-flash prices, ≤ ~$20/series (≈ one
   month's subscription; the services-business tripwire from second-opinion
   addition #2).

Verdict shape: all four bars → D2/D4/D5 stand as ratified. Precision < 0.6
or evolution handling 0/3 → D4's agent-proposes layer needs redesign and
D2/D4/D5 reopen per the ratification condition. Middle → targeted amendment,
not reopening.

## Method notes

Extraction agents are blind to ground truth (never shown character.yaml,
wiki pages, or unblinded filenames). Chained P&C stages see only the prior
stage's proposed bible, mirroring production (installment N vs bible from
1..N-1). Scoring is done by the orchestrator against ground truth documents
+ direct page reads, with the blind maps opened only at scoring time.
