# Virtual Rehearsal — `rehearsal.html`

**This is the workspace's rehearsal tool.** Zero install, zero accounts,
fully offline: open in any browser, drag in the show's firing-script CSV +
mix MP3, press play (space bar toggles).

What it renders:

- Canvas fireworks with additive glow, inferred from each event description:
  effect type (willow/brocade trails, crackle, strobe, mine, salute flash,
  comets, fan spreads), palette (R/W/B, neon, rainbow, gold, …), and shot
  count/duration parsed from text like `(100 / 0:35)` — each event fires
  that many launches spread across its duration from its station's position.
  Big mortar breaks get pistil cores and trailing stars.
- A clickable **timeline strip**: every event as a tick, one lane per
  channel, colored until fired — click anywhere to jump. Great for spotting
  gaps and clustering at a glance.
- Per-station cue panels using the 18R2's LED language (green pending →
  white flash firing → red fired), a now-playing readout, next-cues ticker,
  seek bar, and 0.5–4× speed.

Limits: it's a storyboard, not a physics render — built for reviewing
timing, pacing, structure, and channel balance. STEP scripts are
approximated (presses assumed 3 s after the prior event); fully timed
scripts replay exactly. The hardware dry-run before show night is still
mandatory.

---

## Appendix: external tools (researched July 2026, for reference)

If photoreal 3D ever becomes worth an extra tool: **Finale 3D** is the only
option with native COBRA CSV import + MP3 sync at $0 (Demo Mode, or a
14-day trial; Lite $149/yr). Rejected: FWsim (COBRA import locked behind
~$79/mo Pro), COBRA Show Creator ($78.79/yr, explicitly **no** visual
simulation), ShowSim (abandonware since ~2015), GLOW/IGNITE and current
open-source projects (no cue-sheet import).
