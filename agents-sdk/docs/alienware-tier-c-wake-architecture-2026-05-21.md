---
type: decision-record
created: 2026-05-21
resolved: 2026-05-25
status: accepted
supersedes:
  - "(initial Pattern A draft in Topic 20 plan)"
---

# Alienware Tier C — Wake Architecture Decision Record

## Decision

**Pattern E — manual-wake interactive Tier C.** Sean physically wakes the Alienware via mouse jiggle / keyboard / power button at the start of each day (~7am) and lets it idle-sleep at night (~5pm). The agent fleet does **not** autonomously route to Tier C. Agents that want to use Tier C must run during Sean's awake-Alienware window or fall back to Mac Mini / MBP if the machine is unreachable.

This decision was reached on 2026-05-25 after empirical refutation of three other patterns. The plan as originally drafted (Pattern A — on-demand WoL from S3) was based on hardware assumptions that did not hold.

## Context

The Topic 20 plan was drafted 2026-05-21 with these implicit assumptions:

- **Assumed hardware:** Alienware desktop with RTX 4090 24 GB VRAM, traditional S3 sleep state available
- **Assumed wake path:** WoL magic packet → NIC asserts PME → CPU wakes from S3 → Ollama serves → idle-sleeps back to S3 after 30 min
- **Assumed power profile:** ~5W S3 idle, ~150W during workload, ~$1.50/month at 22h sleep/2h workload daily

**Actual hardware** (per Dell order screenshots + `Get-NetAdapter` / `system_profiler` audit):

| Spec | Reality |
|---|---|
| Model | Alienware Aurora ACT1250 (2025 generation) |
| GPU | NVIDIA RTX 5080 — **16 GB GDDR7** (Blackwell), not 24 GB |
| CPU | Intel Core Ultra 9 285 (24-core) |
| RAM | 64 GB DDR5-5200 |
| Storage | Single 1 TB NVMe M.2 PCIe SSD |
| NIC (wired) | Killer E3100G 2.5 Gigabit Ethernet, MAC `B4-E9-B8-F7-71-47` |
| NIC (wireless) | Intel Wi-Fi 7 BE200 |
| BIOS | Alienware 1.14.0 |
| OS | Windows 11 Home Build 26200 |
| Sleep states | **Modern Standby (S0ix) ONLY** — firmware does not support S3/S1/S2 |
| Power scheme | Balanced; `standby-timeout-ac = 1800` (30 min idle) |

## What was tried and why each pattern failed

### Pattern A — on-demand WoL from S3 (original plan)

**Failed because S3 doesn't exist on this firmware.** `powercfg /a` shows S3, S1, S2, and Hibernate all as "The system firmware does not support this standby state." Only `Standby (S0 Low Power Idle) Network Connected` is supported. This is consistent with most 2024+ Intel/Dell consumer hardware — Modern Standby is the only sleep path.

### Pattern A-prime — WoL from S0ix Modern Standby

**Failed because Modern Standby firmware blocks NIC-asserted wake events at the hardware level.** Test 2026-05-25 12:24:

- Magic packet sent from Mac Mini to `192.168.71.255:9` (correct /22 broadcast for the Deco mesh — discovered 2026-05-24)
- Killer driver had `WakeOnMagicPacket=Enabled`, `WakeOnPattern=Enabled`, `Shutdown Wake-On-Lan=Enabled`
- `powercfg -devicequery wake_armed` confirmed the Killer is wake-armed
- 6 minutes passed with no wake — no fan spin-up, no screen, no RGB, no HTTP response from Ollama
- `powercfg -lastwake` afterward: `Wake History Count - 0`

The prior session's "2-second wake from S0ix verified" measurement (2026-05-24, captured in `project_topic20_phase2_findings.md`) was a **false positive**. The Killer NIC keeps an opportunistic TCP listener alive in S0ix — `socket.create_connection((host, 11434))` succeeds at the NIC level without the OS actually being awake. Real HTTP requests time out from the same state, proving the OS is genuinely in deep sleep. The `probe_until_ready` measurement protocol in `agents-sdk/scripts/wake_alienware.py` is **not a valid wake-success signal** on this hardware.

### Path 1 — disable Modern Standby via `PlatformAoAcOverride=0`

**Failed because the BIOS does not expose S3 even with Modern Standby disabled.** Test 2026-05-25 11:50–12:05:

- Set registry: `HKLM\SYSTEM\CurrentControlSet\Control\Power\PlatformAoAcOverride = 0` (DWORD)
- Restarted Alienware
- `powercfg /a` post-restart: **ALL sleep states** showed "The system firmware does not support this standby state." Machine literally could not sleep.
- Reverted: `reg delete ... /v PlatformAoAcOverride /f` + restart → Modern Standby returned

The firmware genuinely does not implement the S3 path. The `PlatformAoAcOverride` Windows-level override only works on hardware where firmware exposes both S3 and S0ix; on hardware that only exposes S0ix, disabling Modern Standby leaves nothing.

### Pattern B — Windows Task Scheduler with `WakeToRun=True`

**Failed because Modern Standby firmware also suppresses RTC wake events.** Test 2026-05-25 12:13–12:21:

- Created three tasks via PowerShell (running as `NT AUTHORITY\SYSTEM` at `RunLevel Highest`):
  - `AlienwareWakeOvernight` — daily 02:00
  - `AlienwareWakeWorkday` — daily 09:00
  - `AlienwareWakeSmokeTest` — once at 12:16:20 (T+3 min)
- All three confirmed: `WakeToRun=True`, `Allow wake timers = Enable` (index 1, not "Important Wake Timers Only" as initially misread)
- Sean clicked Start → Sleep at ~12:14
- 12:16:20 came and went — no wake event, no fan, no screen, no RGB
- Sean manually woke the machine via mouse jiggle at ~12:21
- Smoke task fired at 12:21:36 — but this was the `-StartWhenAvailable` flag running the missed task after the manual wake, **not** the scheduled wake itself firing

The same firmware mechanism that suppresses WoL also suppresses RTC wake. No Windows-side policy override exists — `Allow wake timers = Enable` is already the most permissive setting, and it has no effect on Modern Standby suppression.

### Pattern Z — S0ix-transparent serving (hypothesized, refuted)

**Failed because HTTP requests time out from S0ix even though the TCP listener is alive.** Tested as a fallback after Pattern A failed. The Killer NIC accepts TCP SYN at hardware level, but the OS networking stack is suspended — `curl --max-time 15` against `/api/tags` returned silence. The machine has to actually wake to serve real requests.

## What this firmware DOES respect

The only working wake paths on this hardware:

- Physical input (mouse, keyboard) — instant wake
- Power button press — instant wake
- Microsoft-signed system tasks (Windows Update etc.) — cannot be user-controlled

## Decision rationale — why Pattern E

| Pattern | Net effect | Verdict |
|---|---|---|
| **A** (WoL from any sleep) | Firmware blocks wake events. Not viable. | ❌ |
| **B** (Task Scheduler wake) | Firmware blocks RTC wake events. Not viable. | ❌ |
| **C** (always-on, never sleep) | ~$5–10/month extra power. Tier C fully autonomous. | Viable fallback |
| **D** (shelve Tier C) | Lose Tier C from fleet refresh. | Defeats Topic 20's purpose |
| **E** (manual physical wake) | $0 extra. Tier C available during Sean's waking hours (~7am–5pm). Overnight batch stays on Mac Mini + MBP fleet, which is already proven. | ✅ Chosen |

Pattern E was chosen because:

1. **Matches Sean's actual daily reality.** Sean is at his desk most days. Physical wake costs ~1 second of attention each morning.
2. **Zero infrastructure to maintain.** No scheduled tasks, no wake scripts in production, no fleet routing logic to handle "is Alienware reachable" — agents simply check and fall back if Tier C is unavailable.
3. **Power-efficient.** Modern Standby idle (~3–10W) when not in use; full power only when Sean actively uses it.
4. **Reversible.** If hardware ever supports remote wake (firmware update, different chassis), the fleet can adopt Pattern A or B trivially — Tier C model files and routing config stay the same.

## Implementation summary

What lives on the Alienware:

- **Modern Standby + `standby-timeout-ac = 1800`** (30 min idle-sleep) — kept as-is
- **`WOL & Shutdown Link Speed = Not Speed Down`** (Killer driver) — kept. Harmless and prepares the NIC for any future wake path that does work.
- **OpenSSH Server (Automatic startup)** — kept. SSH key auth at `C:\ProgramData\ssh\administrators_authorized_keys` works while machine is awake.
- **Ollama 0.21.0** — kept. Auto-starts and binds to LAN on `192.168.68.201:11434`. Serves while machine is awake.
- **PlatformAoAcOverride registry key** — DELETED. Modern Standby is the only viable sleep state.
- **AlienwareWake* scheduled tasks** — DELETED. Pattern B is non-functional.

What lives in `agents-sdk/` (retained as historical / portable artifacts):

- **`agents-sdk/scripts/wake_alienware.py`** — non-functional on this hardware. Retained because it works on standard Linux/desktop hardware that supports S3 + traditional WoL. If a future Tier C host is added (e.g., a Linux box), this script needs no changes.
- **`agents-sdk/scripts/sleep_alienware.py`** — non-functional on this hardware (no scriptable sleep API works on Modern Standby per Phase 2 findings). Retained for the same reason.
- **`agents-sdk/lib/wol.py`** — tested, working library code for magic-packet construction. Hardware-agnostic. Retained.
- **`agents-sdk/config.toml [routing.machines.alienware]`** — `wol_mac` and `wol_broadcast` retained. Harmless and accurate if hardware changes. `always_on = false` reflects Pattern E (not actually always-on; just "unavailable when asleep").

## Operating contract for the agent fleet

Agents that want to route to Tier C MUST treat it as a best-effort host:

1. **Check before use:** `curl -s --max-time 3 http://192.168.68.201:11434/api/tags` — if it succeeds, Tier C is awake and ready; if it times out, fall back.
2. **Do not call `wake_alienware.py` in production paths** — it is a no-op on the current Tier C host. Either call it advisorially (and ignore the failure) or skip it.
3. **If routing critical work to Tier C, schedule the agent to run during Sean's waking-Alienware window** (default: 7am–5pm). Cron / launchd schedules must respect this.

## Power math (Pattern E)

Conservative estimate:
- 10h × 100W (waking-Alienware window, mostly idle with intermittent inference) = 1.0 kWh/day
- 14h × 5W (Modern Standby overnight + during the day when not used) = 0.07 kWh/day
- Total: ~1.07 kWh/day = ~32 kWh/month
- At $0.13/kWh: **~$4.20/month**

Compared to plan-original Pattern A (assumed): ~$1.50/month. **+$2.70/month** for the simpler architecture is acceptable.

Compared to Pattern C (always-on): ~$9.36/month. **Saves $5.16/month** vs the always-on alternative.

## Rollback

To remove all Tier C provisioning entirely:
1. `ollama rm` each pulled Tier C model variant (per Task 3.4 inventory)
2. Set `[routing.machines.alienware].always_on = false` (already the value)
3. Remove any `routing.task_map` entries pointing at `alienware`
4. Optionally power the Alienware off — but it stays useful as a daily-driver / gaming machine independent of the fleet

To revert to Pattern A or B in the future:
- Pattern A: requires either (a) firmware update that exposes S3, or (b) replacement chassis with traditional sleep states. Re-test `WakeOnMagicPacket` from S3 — should work out of the box on hardware that supports it.
- Pattern B: requires firmware behavior change that allows non-Microsoft-signed RTC wake events. Unlikely on this hardware family; more likely on enterprise / workstation lines.

## Investigation log — for future reference

This decision required ~2.5 hours of empirical investigation across multiple wake patterns. Future sessions: **do not retry these on the same hardware.** The auto-memory entry `project_alienware_wake_impossible.md` summarizes the findings in 1 minute of read time.

Timeline:
- 2026-05-21 — Plan drafted with Pattern A assumption
- 2026-05-24 — Phase 2 discovered /22 broadcast + Modern Standby; logged "2-second wake from S0ix verified" (later proven a false positive)
- 2026-05-25 11:24 — First WoL attempt under proper measurement protocol failed
- 2026-05-25 11:30 — HTTP-vs-TCP gap discovery (TCP listener stays alive in S0ix, HTTP times out)
- 2026-05-25 11:34 — `powercfg -lastwake` shows zero wake events; root cause hypothesized
- 2026-05-25 11:50 — Path 1 (PlatformAoAcOverride=0) attempted, broke all sleep states, reverted
- 2026-05-25 12:13 — Pattern B (Task Scheduler) attempted with full diagnostic logging
- 2026-05-25 12:21 — Pattern B wake event also failed; scheduled task fired only after manual wake via `-StartWhenAvailable`
- 2026-05-25 12:25 — Pattern E adopted; investigation closed

## References

- Plan: [`agents-sdk/docs/plans/2026-05-21-topic-20-fleet-model-refresh-benchmarks-plan.md`](plans/2026-05-21-topic-20-fleet-model-refresh-benchmarks-plan.md)
- Synthesis context: [`vault/20_projects/research/2026-05-21-topic-19-synthesis-optimal-ollama-models-pi.md`](../../vault/20_projects/research/2026-05-21-topic-19-synthesis-optimal-ollama-models-pi.md)
- Auto-memory: `project_alienware_wake_impossible.md`, `project_alienware_hardware_specs.md`, `project_topic20_phase2_findings.md`
- Microsoft Modern Standby reference: <https://learn.microsoft.com/en-us/windows-hardware/design/device-experiences/modern-standby> (background on why firmware suppresses wake events under Modern Standby)
