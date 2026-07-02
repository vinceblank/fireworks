---
name: rehearse
description: Run a virtual rehearsal of a show — the browser-based simulator plays the mix and renders every cue firing (stations, cue panels, and canvas fireworks inferred from event descriptions). Use when the user wants to preview, review, watch, or rehearse a show before firing it for real.
---

# Virtual Rehearsal

`tools/rehearsal/rehearsal.html` is a self-contained, offline show simulator:
it plays the show soundtrack and fires the script in real time — canvas
fireworks (effect/color/shot-count inferred from each event description),
per-station cue panels (pending → firing → fired), a live "now playing"
readout, seek/speed controls.

## Running a rehearsal

1. Confirm the show has an exported firing script (`cobra.csv`); if not,
   `/export-show` first. The mix MP3 in `<show>/audio/` is optional but the
   whole point — rehearse with it if it exists.
2. Open the tool in the default browser
   (`start tools/rehearsal/rehearsal.html` on Windows).
3. Tell the user exactly which two files to drag in (full paths to the
   show's script CSV and mix file) — the tool takes drag-and-drop or the
   two load buttons. Space bar = play/pause; 2×/4× speed for quick passes.

## What to review (give the user this checklist)

- **Dead air** — any stretch with an empty "now playing" readout that isn't
  a designed silence (siren bridge). The no-gap rule is easiest to *see*.
- **Peak placement** — do the big moments land where the music peaks?
  Watch the false finale especially: does it read as an ending?
- **Texture clustering** — do near-identical effects fire back-to-back?
- **Finale density** — does the last minute visibly out-scale the rest?
- **Station balance** — is one cue panel exhausted long before the other?

Capture every observation as a proposed edit to
`fireworks-show-overview.md` (source of truth), then re-run `/export-show`
and rehearse again.

## Limits (say these up front)

- Visuals are inferred from event *descriptions* — a rough storyboard, not
  a physics render. Timing, pacing, and structure are what it's for.
- STEP scripts get approximated (STEP presses assumed 3 s after the prior
  event); fully timed scripts replay exactly.
- Mix formatting issues (drift) won't show here — the tool and the 18R2
  both trust the file's timeline. The dry run on real hardware is still
  mandatory (see the device profile).

## Higher-fidelity option

For a photorealistic 3D rehearsal, **Finale 3D** natively imports COBRA
script CSVs and syncs the MP3 — free via Demo Mode or a 14-day trial.
See `tools/rehearsal/README.md` for the full comparison of external tools
(researched 2026-07). Offer it when the user wants more than a storyboard,
e.g. for judging actual sky-fill and effect looks.
