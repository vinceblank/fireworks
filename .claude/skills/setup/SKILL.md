---
name: setup
description: Create or update equipment.yaml — the user's firing system, mortar racks, audio gear, and site profile. Researches unknown firing systems and records them as device profiles in devices/. Use when equipment.yaml is missing, has TODOs, or the user mentions new/changed gear.
---

# Equipment Setup Wizard

Every other skill in this workspace reads `equipment.yaml` at the repo root
before doing anything. Your job: make sure that file exists, is complete, and
is backed by a device profile in `devices/`.

## Procedure

1. **Look for `equipment.yaml` at the repo root.**
   - Exists and complete (no `TODO` values) → summarize it back to the user, ask if anything changed, update as needed. Done.
   - Exists with `TODO`s → only interview for the missing pieces.
   - Missing → full interview (below).

2. **Interview** (use AskUserQuestion where options are enumerable; keep it
   conversational, not a form). Gather:
   - Firing system **make + model** (controller/remote model).
   - **Modules/stations**: how many, model, cues per module, and the channel
     each is set to.
   - **Igniter type**: e-match, Talon, or consumer clip igniters.
   - **Scripting**: does their system support scripted shows? (Look this up in
     the device profile — don't ask if the profile answers it.)
   - **Audio**: how music is played (synced audio box vs. manual playback) and
     on what device.
   - **Mortar racks**: tube counts, diameters, whether tubes are fused into
     groups (one cue per group) or fired individually.
   - **Site**: backyard/field, rough audience distance, any constraints.
   - **Show defaults**: target length, overlap style, finale reservation.

3. **Device profile check.** Slugify make+model (e.g. `cobra-18r2`) and look
   for `devices/<slug>.md`.
   - Found → link it in `equipment.yaml` under `firing_system.profile`.
   - Not found → **research it** (see below), write the profile, then link it.

4. **Write `equipment.yaml`** following the structure of the existing file (or
   the schema in `devices/firing-systems.md`). Keep comments — the file is
   read by humans wiring a show, not just by skills.

## Researching an unknown firing system

When no `devices/<slug>.md` exists, delegate to the **device-researcher**
agent (`.claude/agents/device-researcher.md`) — it keeps the verbose search
output out of the conversation and returns a summary. If agents are
unavailable, follow the same procedure inline:

1. Web-search the manufacturer's official manual/support pages. Establish:
   architecture (controller + modules), channels vs cues, cues per module,
   firing modes, **script/show file format if scripting is supported** (exact
   columns/fields — this is what `/export-show` will consume), audio sync
   mechanism, igniter compatibility, arming/continuity workflow, limits.
2. Write `devices/<slug>.md` using `devices/TEMPLATE.md` as the skeleton.
   Cite source URLs at the bottom. Mark anything unverified as such.
3. If the web is unreachable or results are thin, create the profile from the
   user's own answers and mark it `status: unverified` in the header so a
   future session knows to finish the research.

## Notes

- `devices/firing-systems.md` has the generic vocabulary (controller, module,
  channel, cue, igniter) and a survey of common systems — read it before
  interviewing so your questions use the right terms for their brand.
- Never delete a device profile; systems other users of this repo own may
  differ from the current `equipment.yaml`.
