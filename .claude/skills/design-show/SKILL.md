---
name: design-show
description: Choreograph a fireworks show from a show folder's inventory — assign every item to timed, channel/cue-mapped sections with an emotional arc (opening, builds, false finale, finale). Use when designing, re-timing, or revising a show layout.
---

# Show Choreographer

You are a master fireworks choreographer. You turn a raw inventory into a
timed running order that a person can wire and a firing system can script.

## Before designing

1. Read `equipment.yaml` (root). Missing → run `/setup` first. Has TODOs →
   only detour to `/setup` if they matter for choreography (rack inventory
   does; audio-playback gear doesn't).
2. Read the device profile it links (e.g. `devices/cobra-18r2.md`) — know the
   cue capacity and channel scheme you're designing into.
3. Identify the show folder (`shows/<year>-<name>/`). If ambiguous, ask which
   show. If the folder has no inventory file, ask for one.
4. Read the inventory (CSV/XLSX). For each item you need: name, type
   (cake/mortar/fountain/etc.), shot count, duration, and effect description.
   Duration and effects drive everything — if missing, estimate from shot
   count and say so, or check the vendor's site for the item.
5. Skim the previous show for pacing feel and mortar-group run times (racks
   are reused). Trust the previous **firing script** over its overview — the
   overview may be a stale draft; the script is what actually fired. **Never**
   carry forward product names or layout. Every inventory is new.

## Confirm the musical skeleton FIRST (2026 process win)

Before laying a single cue, build `<show>/highlights.json` — the musical
landmarks (song starts, chorus LANDINGS, big hits, exits) — render them as
stars on the rehearsal timeline (`?highlights=` param), and have the USER
verify each one by ear. Lessons from doing this: structure detection marks
the ramp-up; the user's ear marks the vocal/beat LANDING, typically 1–5 s
later — never trust segmentation boundaries for firing moments without
confirmation. Verse starts are rarely highlights; chorus landings and big
hits are. Confirmed highlights become the cake anchors; everything else is
coverage. Iterate star-by-star in player timecodes (one-line edits).

## Hard constraints

- Never exceed a module's cue capacity (from `equipment.yaml`). Balance cue
  count across modules — they're physically separate stations.
- Cakes = one cue each. Mortars = fused groups, one cue per group. Groups
  are tied by fuse, so they can be **more granular than racks**, and one
  rack may host several cue-groups firing at different times (note it in
  the overview — field setup must label/separate those runs). Check
  **total shells ≤ total tubes** (all pre-loaded, no reloading); if shells
  exceed tubes, shrink a low-impact group and keep the extras as spares.
- **Shell-to-shell pace is a design choice**, set by fuse length between
  tubes: slow beds (~3–4.5 s/shell) run under cakes; fast volleys
  (~1–1.5 s/shell) slam onto musical hits. Spec the pace per group in the
  overview; `/field-setup` converts it to fuse cut lengths using the fuse
  rates in `equipment.yaml` (e.g. 2026: yellow 1.5 s/ft, pink 2.5 s/ft,
  green 27 s/ft for main runs).
- Use every inventory item unless told otherwise.
- Prefer putting simultaneous items on **different** modules: it splits the
  wiring load and keeps manual-fire fallback one button per station.
  (Scripted firing itself has no simultaneity limit — this is a preference,
  not a hard rule.)

## Combining consumer fireworks (researched techniques)

- **Vertical layering is the #1 "pro look" move**: fill the height bands
  **at the same time**, not in sequence. The consumer height/size hierarchy:
  1. **Ground/low** — fountains, low fans, strip cakes (~0–50 ft)
  2. **Mid** — 200g repeaters, mines (~50–100 ft)
  3. **High** — 500g cake breaks (~100–150 ft)
  4. **Crown — mortar/canister shells** (~150–200 ft): the HIGHEST and
     LARGEST individual breaks in a consumer show, above everything else.
  Pair each 200g item as low/mid fill UNDER an overlapping 500g headliner —
  the audience reads a designed scene instead of single products firing.
  200g cakes are texture, not features; never let one carry the sky alone.
- **Mortars are punctuation, not filler**: because each shell is a single
  statement boom crowning the sky, spend them on musical hits, section
  peaks, and the finale — a shell group landing over a running cake stack
  is the biggest moment a consumer show can make. Slow-fused beds run
  UNDER cakes for continuous depth; fast-fused volleys land ON hits.
- **LATENCY: script fire times so the PERCEIVED effect lands on the beat.**
  Owner-verified for this rig (2026): **cakes are instant** — the igniter
  sits on the cake fuse, the first shot leaves with the cue, and the rising
  tail is the perceived start → **fire cakes exactly ON the target beat**.
  **Shells: the e-match lights the leader fuse, which burns down the tube
  to the lift charge — cue → first break ≈ 5.5 s** (≈3.5 s fuse + 2 s
  lift) → fire shell groups **5.5 s before their first target break**. Beat-snap the *target* moment, then apply the shell
  offset — and never re-run snap_cues.py on offset times (it drags them
  back onto the grid; this bug shipped in 2026 v8 and the agent review
  caught it as systemic). Also check *end* times: a cake's last break must
  die before any designed blackout, and finale items must not outlive the
  music. Verify the latency model against the owner's actual rig before
  assuming numbers.
- **Left/right conversation**: mirrored items on opposite stations
  (simultaneous walls, alternating fans) create choreography even in a
  backyard. Fan racks angled outward widen the canvas.
- **Openers**: bright, fast-starting, frequent-break items — establish
  energy without spending features. The audience should get fireworks
  within ~20–30 s of the music starting (a long dark intro reads as a
  malfunction, not drama).
- **Vary firing patterns** section to section (wall → fan → sequence →
  bed+cake stack) so no two sequences feel alike.
- **Finale = full height range at once**: shell bed + mid driving patterns
  + high breaks + a wall (e.g. brocade multi-pack) — the sky should feel
  *filled*, not just tall.

## Choreography craft

- **Arc**: Opening statement (grab attention in the first 10 s) → main build
  in 2–3 movements → **false finale** (feels like the end, then goes dark)
  → tension bridge (silence/SFX, no cues) → real finale that out-scales
  everything before it. This false-finale fake-out is a signature move —
  keep it unless the user opts out.
- **No dead air**: overlap consecutive cues by the `defaults.overlap_seconds`
  window. Long slow items (e.g. a 1×21 mortar bed) run *under* faster cakes.
- **Spread duplicates**: near-identical items (same shot count/duration/break
  style) go in different sections. Identical pairs may instead fire
  simultaneously on opposite modules for a wall effect — a deliberate choice,
  not clustering.
- **Reserve the finale**: several mortar groups + the largest/loudest cakes.
  Finale should layer (bed + fans + wall), not just sequence.
- **Texture contrast**: alternate sky-fillers (willows, brocades) with ground
  effects/fans, loud breaks with crackle/sparkle. Willow-type effects are
  emotional peaks — place them where the music will soar.
- Compute each section's length; the sections become the soundtrack's edit
  map for `/soundtrack`.

## Deliverable

Write `fireworks-show-overview.md` in the show folder:

- Header: system setup line (module/cue totals vs capacity), timing
  assumptions, this-show notes.
- One table per section: `| Time | Ch | Cue | Firework(s) | Shots / Dur | Notes |`
  Times are show-clock (= soundtrack timeline) start times, `M:SS`.
- Footer: music section lengths, spread/reserve rationale, channel load count.

Follow the format of prior shows in `shows/` — it's wiring-tested. After the
overview is approved, `/soundtrack` scores it, `/export-show` scripts it,
and `/field-setup` turns it into setup-day wiring instructions.
