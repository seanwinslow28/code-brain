# trace — Systemcraft's side of the shared trace kit

The kit itself lives in [craftwork/trace/](../../craftwork/trace/README.md): the record and labels templates, the rung-0 checker, the viewer, the registry numbers and the handoff freezer. This folder holds only what is Systemcraft's, written on 2026-10-01 when Systemcraft adopted the shared law ([craftwork build 4](https://github.com/seanwinslow28/code-brain/issues/327), per [#282](https://github.com/seanwinslow28/code-brain/issues/282) decision 4).

| File | What it holds |
|---|---|
| [studio.py](studio.py) | The profile the kit reads: the five-seat pipeline as stages 1–5, the record kinds (the handoff modifier's `intake` among them), the closed audit cycle, and rung-0 line 8, which checks that a design engagement ran its own shape and that no audit pass crossed into a lane its seat neither owns nor audits |
| [taxonomy.md](taxonomy.md) | Systemcraft's own seat failure modes. It is empty until its own labels earn one; the shared process-waste family is the kit's |

**Traced from eng-005 on.** eng-001 to eng-004 ran before the kit existed and are not retrofitted. The kit finds this profile by walking up from the engagement folder, so the Close lines need no flag:

```bash
python3 craftwork/trace/check.py systemcraft/ledger/engagements/<eng-id>
```

```bash
python3 craftwork/trace/render.py systemcraft/ledger/engagements/<eng-id>
```

**Two Systemcraft differences from Productcraft.** The brief header sits in `open-brief.md`, the file Systemcraft's Open has always written. Audits, co-signs and gate findings sit in `artifacts/` beside the work they check, not in a separate `audits/` folder. The record grammar, the hash chain, the labels file and every other rung-0 line are the kit's, unchanged.

**Labels.** Labels follow pc-eng-001's pattern ([#282](https://github.com/seanwinslow28/code-brain/issues/282) decision 4). The coordinator drafts them at Close, Sean approves them, and the labels file's provenance block says so.
