---
name: content-oracle
description: Moved. The content Oracle (stage 0 of the content machine) now lives in the private pencil-and-prompt repo and runs only from there. If asked to run the Oracle or "what should I write about" from code-brain, do not improvise a sweep here. Tell Sean to run /content-oracle from ~/Code-Brain/pencil-and-prompt. NOT the separate `the-oracle` capture/reminders project at ~/Code-Brain/the-oracle/.
---

# Content Oracle (moved)

The Oracle moved to the private `pencil-and-prompt` repo on 2026-09-25 ([#308](https://github.com/seanwinslow28/code-brain/issues/308), batch 3). It writes into the brain that lives there, so a run from this repo would write to the wrong place. The scripts were removed from here in batch 6.

**Run it from `~/Code-Brain/pencil-and-prompt`.** It still sweeps this repo's commits, dailies, closed issues, fleet manifests and tickets, and it borrows `agents-sdk/scripts/audit_dr_citations.py` and `doc_to_audio.py` from here through `$CODE_BRAIN_DIR`, until [#313](https://github.com/seanwinslow28/code-brain/issues/313) refocuses its supply.

The probation reminder that emails every Sunday at 08:00 stays here: `agents-sdk/scripts/oracle_reminder.py`, on launchd.

This stub keeps the path alive for the content machine's retirement registry, which scans it every Sunday. The full history of the skill is in git.
