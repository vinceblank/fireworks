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
3. Tell the user exactly which files to drag in (full paths to the show's
   script CSV, mix file, and `effects.json` if present) — drag-and-drop or
   the load buttons. Space bar = play/pause; 2×/4× speed for quick passes.

## effects.json (per-show, optional but worth building)

`<show>/effects.json` refines the animation beyond description-keyword
guessing and links each product to its vendor demo video (the user buys
from Pro Fireworks — their YouTube channel has demos for most products).
Schema: an array of
`{match, video, type, fan, palette, height, notes, verified}` — `match` is
a lowercase substring of the cue description; `type` ∈ peony|willow|
crackle|strobe|mine|salute|comet|whistle; `palette` ∈ rwb|gold|neon|
rainbow|silver|red|green|blue|mixed; `height` ∈ low|mid|high. In the
simulator, cue chips with a video get a gold outline — clicking any chip
opens a detail panel with the effect profile and the embedded demo.

To build/extend it: search "Pro Fireworks <product>" on YouTube, verify
via the oEmbed endpoint (`youtube.com/oembed?url=...` → author_name
"Pro Fireworks"), pull effect details from the profireworks.com product
page, and fill the fields. Delegate the fan-out to an agent when doing a
whole inventory.

## Headless run (agents: validate the show yourself)

You can rehearse and *watch* the show without the user:

1. One-time setup: `cd tools/rehearsal && npm install && npx playwright install chromium`.
2. `node tools/rehearsal/record.mjs <show>/cobra.csv [<show>/effects.json]`
   → deterministic replay (no wall-clock wait), one screenshot ~1.2 s after
   every cue + periodic sweeps, `index.json` with per-frame metadata and a
   particle-count dead-air heuristic, into `<show>/rehearsal-captures/`
   (gitignored).
3. **Read the PNGs in order** and judge against the checklist below; the
   filenames embed clock + channel + cue + description. Cross-check flagged
   "possible dead air" sweeps — sparse sequential cakes can momentarily
   show zero particles without being real dead air, and designed silence
   (siren bridge) *should* be empty.
4. Report findings as proposed overview edits, like any review.

The page also exposes `window.rehearsal` (loadScript / loadEffects /
stepTo / getEvents / getState) for custom probes.

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

`rehearsal.html` is the workspace's rehearsal path — don't suggest external
tools unprompted. (If the user ever asks for photoreal 3D, the researched
comparison lives in `tools/rehearsal/README.md`.)
