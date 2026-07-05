---
name: field-setup
description: Generate the setup-day field document for a show — per-station wiring tables (cue → firework), ground layout with placement groups, and pre-show checklists — and optionally push it to Google Drive for phone access. Use when it's time to physically set up, wire, or lay out a show, or when the user asks for wiring/setup instructions.
---

# Field Setup Document

The choreography docs are written for designing; this deliverable is written
for **show day** — someone kneeling in the grass with a spool of wire and a
phone. Optimize for glanceability: short lines, big tables, no prose walls.

## Inputs

1. `equipment.yaml` — stations, channels, cue capacities, igniter type.
2. `<show>/fireworks-show-overview.md` — the settled choreography.
3. The exported firing script if present (`cobra.csv` etc.) — cross-check
   that wiring tables match it exactly; the script is what actually fires.
4. Device profile (e.g. `devices/cobra-18r2.md`) — continuity/arming steps.

If the overview and script disagree, stop and flag it — never write a wiring
doc from stale choreography.

## Deliverable: `<show>/field-setup.md`

Structure, in this order (setup happens in this order too):

1. **Header** — show name/date, runtime, station → channel dial settings,
   module firing mode (e.g. Talon 2 s vs e-match 0.1 s), battery checklist.
2. **Ground layout** — placement groups (see below) with a simple ASCII
   sketch: audience line, safety distance, each group's rough position.
3. **Per-station wiring tables** — one table per station, sorted by cue:
   `| Cue | Firework | Type | Placement group | Notes |`
   Notes carry what the wirer needs: fused-group size for mortar racks,
   "pair with Ch2-C1" for simultaneous walls, fan orientation.
4. **Mortar fusing table** — one row per fused group: rack, shell count,
   target pace (from the overview), and the **fuse cut length between
   tubes for each fuse type on hand** (rates in `equipment.yaml`;
   length = pace ÷ rate — 2026 example: 1.5 s/shell = 12 in yellow or
   7 in pink). Main runs (igniter → group) use the slow fuse (green),
   cut to equal lengths within a group. Include a test-burn reminder
   (visco batch rates vary). **When multiple cue-groups share one rack**,
   require labeled/color-coded runs and physical separation so a hot
   earlier group can't light a later run.
5. **Placement group details** — for each group: which items, why they're
   together, spacing/orientation warnings.
6. **Checklists** — wiring-complete walk (every cue in the tables), local
   continuity test per module, remote continuity from the controller,
   audio dry-run, arming steps. Pull specifics from the device profile.
7. **No-wires dry-run protocol** (bench test before setup day; owner-
   requested level of detail — ALWAYS give knob-level instructions:
   every keyswitch position, channel-dial position, and LED meaning):
   - Module keyswitches → **ARM** (TEST-keyed modules won't accept the
     script or execute; with bare terminals ARM is harmless — each fired
     cue is a 0.1 s pulse into an empty terminal).
   - Module channel dials per the wiring plan; remote parked on the
     script's TRIGGER CHANNEL (works on any firmware).
   - Expected continuity signature: ALL scripted cues RED (scripted, no
     continuity) — correct with nothing wired; count reds per channel as
     a cue-count cross-check.
   - Remote ARM → wait for SOLID ARM LED + device count, then run the
     real show ritual against the real mix end-to-end; after the run all
     scripted cue LEDs show fired-red.
   - Second pass: practice DISARM abort → re-ARM → restart → STEP
     catch-up, and one +/− nudge.
   - Keyswitch discipline note: modules stay keyed TEST during real
     wiring days; ARM only at dusk as the final step.
   - **HARD LIMIT of this dry-run (2026 failure lesson): empty terminals
     draw no current, so it can NEVER catch power-delivery problems.**
     The 2026 show passed every bench test and continuity check, then
     ~40% of cues failed to fire — module batteries sagged under real
     firing load (continuity tests with milliamps; firing takes amps).
8. **Show-day POWER checklist (mandatory — from the 2026 post-mortem,
   `shows/2026-july-4/post-mortem.md`):**
   - FRESH batteries (or COBRA LiPo / 12 V external) in every module ON
     show day. Never holdover batteries; never trust idle voltage.
   - Under-LOAD voltage check per battery (loaded <~7 V on a 9 V = replace).
   - Live-fire several sacrificial igniters at show pace (rapid sequence
     + a simultaneous pair on one module) on the actual show batteries
     during setup-day testing. Budget ~5 spare igniters for this.

## Placement grouping logic

Group items on the ground by these rules, in priority order:

1. **Station proximity**: everything wired to one module must be within its
   wire-run radius — station location anchors each group.
2. **Timeline adjacency**: items that fire back-to-back go near each other
   (one visual center of gravity per show moment); simultaneous pairs on
   opposite stations go **apart** (that's the wall effect).
3. **Finale cluster**: finale items grouped tight for layered sky, but with
   enough spacing that a tipped cake can't chain into its neighbors.
4. **Directional effects**: fan cakes and angled racks aimed across the
   audience line, never at it; note the aim direction per item.
5. **Slow beds** (long-running mortar racks) placed center-rear so cakes in
   front don't obstruct or endanger them mid-burn.

Never let layout convenience shorten safety distances — flag conflicts to
the user instead of resolving them silently.

## Google Drive push (optional, on request or offer it)

If Google Drive MCP tools are available (check via ToolSearch for
`google drive create_file`; they exist when the user's claude.ai Google
Drive connector is on):

1. Push with `create_file`: `title` = `"<Show> — Field Setup"`,
   `textContent` = the markdown, `contentMimeType` = `text/markdown`,
   default conversion ON → arrives as a native **Google Doc**, phone-ready.
2. Re-pushing: `search_files` for the title first; Drive `create_file`
   always creates new, so delete/rename awareness matters — tell the user a
   fresh version was created and include the link from the response.
3. No Drive tools available → say so, and offer alternatives: SendUserFile
   (if in a client that renders it) or printing `field-setup.md`.

The repo copy is the source of truth; the Drive copy is a convenience
export. Note the push date in the doc footer so a stale phone copy is
detectable.

**Media files (the show mix etc.) canNOT go through the Drive connector** —
create_file carries content inside the tool call as base64, and a >10 MB
MP3 is orders of magnitude over the payload limit. Instead: SendUserFile
the MP3 (saveable from the phone app), and tell the user the two manual
paths: drag-drop into the Drive folder on the PC, or phone share-sheet →
"Save to Drive" → pick the folder. Also remind: phone on Do Not Disturb
during the show.
