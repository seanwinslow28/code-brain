# Kickoff A — Fix gemini_dr.py (google-genai >= 2.0.0 migration)

**Paste this into a fresh Claude Code session in `~/Code-Brain/code-brain`. Run BEFORE Kickoff D (the deep-research session is dead until this lands). Independent of Kickoffs B and C.**

---

Fix the broken Gemini Deep Research path so the Pencil & Prompt research round (and every other caller) can use it again. This is the open ticket "gemini_dr.py migration to google-genai >= 2.0.0" in `vault/00_inbox/tickets.md` — read that ticket first; it carries the full diagnosis.

Context you need:

- Google hard-rejects the legacy Interactions API schema (400 "no longer supported... upgrade to >= 2.0.0", enforcement live since ~May 2026). `agents-sdk/scripts/gemini_dr.py` fails on every live call regardless of credential.
- New call shape (validated by a working reference runner on 2026-07-30): `client.interactions.create(input=..., agent="deep-research-preview-04-2026", background=True)`, poll `client.interactions.get(id)`, final report at `interaction.steps[-1].content[0].text`.
- **The API key lives in `.env`** (check repo root and `agents-sdk/.env`). The script's documented credential home is the macOS Keychain slot `com.sean.agents.gemini_api_key`, and there is a separate open ticket that the Keychain slot is empty. Preferred fix: set the Keychain slot from the `.env` value via `python3 agents-sdk/lib/keychain.py` so the documented convention holds, AND add a `.env` fallback in the resolution path (reference-runner pattern) so a fresh machine without Keychain still works. Never print, echo, or commit the key value anywhere.

The job:

1. Upgrade `google-genai` to >= 2.0.0 in `agents-sdk/.venv` (respect `agents-sdk/pyproject.toml` pinning conventions).
2. Migrate the create/poll/extract block in `agents-sdk/scripts/gemini_dr.py` to the new shape above. Keep the existing tier logic, spend ledger (`vault/health/gemini-spend-{YYYY-MM}.json`), caps ($7/task, $20/day, $50/month), and vault output conventions untouched.
3. Wire the credential resolution: Keychain slot first, `.env` fallback. Set the Keychain slot from `.env` as part of this session.
4. Fix `agents-sdk/tests/test_gemini_dr.py` — the mocks pin the OLD call shape and must be migrated with the code. Keep the tests hermetic (no network; the suite previously had a live-call escape bug, do not reintroduce it — see the DONE ticket note from 2026-06-18).
5. Run `cd agents-sdk && PYTHONPATH=. pytest tests/test_gemini_dr.py -v` and then the full `pytest tests/` to prove no collateral damage.
6. Optional live smoke test: propose the cheapest possible real DR call and ASK SEAN for cost confirmation before firing it. Do not run any live call without his explicit yes.
7. Update the ticket in `vault/00_inbox/tickets.md` (mark DONE with evidence), commit code + ticket per repo conventions.

Done = tests green, credential resolution proven (Keychain populated, fallback exercised in a unit test), ticket closed, and Kickoff D unblocked.
