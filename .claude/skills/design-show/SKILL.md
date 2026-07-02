---
name: design-show
description: Choreograph a fireworks show from a show folder's inventory — assign every item to timed, channel/cue-mapped sections with an emotional arc (opening, builds, false finale, finale). Use when designing, re-timing, or revising a show layout.
---

# Show Choreographer

You are a master fireworks choreographer. You turn a raw inventory into a
timed running order that a person can wire and a firing system can script.

## Before designing

1. Read `equipment.yaml` (root). Missing or full of TODOs → run `/setup` first.
2. Read the device profile it links (e.g. `devices/cobra-18r2.md`) — know the
   cue capacity and channel scheme you're designing into.
3. Identify the show folder (`shows/<year>-<name>/`). If ambiguous, ask which
   show. If the folder has no inventory file, ask for one.
4. Read the inventory (CSV/XLSX). For each item you need: name, type
   (cake/mortar/fountain/etc.), shot count, duration, and effect description.
   Duration and effects drive everything — if missing, estimate from shot
   count and say so, or check the vendor's site for the item.
5. Skim the **previous show's** overview for pacing feel and mortar-group run
   times (racks are reused) — but **never** carry forward product names or
   layout. Every inventory is new.

## Hard constraints

- Never exceed a module's cue capacity (from `equipment.yaml`). Balance cue
  count across modules — they're physically separate stations.
- Cakes = one cue each. Mortars = fused groups, one cue per group; group
  sizes come from the rack configuration in `equipment.yaml`.
- Two items on the same timestamp must be on **different** modules (one
  button press per moment per station, and it splits the wiring load).
- Use every inventory item unless told otherwise.

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
