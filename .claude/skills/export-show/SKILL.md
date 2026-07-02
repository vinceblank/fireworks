---
name: export-show
description: Generate and validate the firing-system-native script (e.g. COBRA CSV) from a show's overview document. Use when the choreography is settled and it's time to produce the file the firing system imports, or to re-validate after edits.
---

# Firing Script Exporter

Turn `fireworks-show-overview.md` into the exact file the user's firing
system imports — byte-format matters here; the controller's importer is
unforgiving.

## Procedure

1. Read `equipment.yaml` → find the device profile (`firing_system.profile`)
   and open it. The profile's **script/export format section** is the spec:
   exact header rows, column order, time format, field meanings. For COBRA
   see `devices/cobra-18r2.md`.
   - No profile, or profile lacks an export spec → research the format
     (manufacturer docs) and add it to the profile first, per the `/setup`
     skill's research procedure.
2. Read the show overview. Every row in its tables becomes one event line:
   time, channel, cue, and a description that a person racing between
   stations can read at a glance (name, shot count, duration, one effect cue).
   Rows with no channel/cue (designed silence, e.g. a siren bridge) produce
   **no** event line. If an approved `*.snapped.csv` proposal exists, its
   times must already be folded into the overview — flag it if not.
3. Generate the script file into the show folder (e.g. `cobra.csv`),
   matching a prior show's export byte-for-byte in structure when one exists.

## Validation (always run, report as a checklist)

- Event times strictly parseable in the device's time format and
  non-decreasing.
- No module over its cue capacity; every (channel, cue) pair unique.
- Every cue number actually exists on that module (1..capacity).
- Simultaneous events are on different modules.
- Every inventory/overview item appears exactly once; nothing invented.
- Overlaps respect the pacing defaults; flag any gap > overlap window
  (dead air) **except** designed silence (e.g. a siren bridge — confirm those
  intentionally have no cues).
- Total runtime matches the overview and (if known) the soundtrack length.

Report mismatches against the overview rather than silently "fixing" them —
the overview is the source of truth; propose corrections there first.

## Run-of-show reminders (append to your final summary, not the CSV)

Wiring happens from the `/field-setup` document; the script is loaded onto
the controller (COBRA: USB stick → 18R2). Remind the user to: verify the script
on the controller, continuity-test every cue, confirm module channel dials
match `equipment.yaml`, and do a dry-run of the audio + script timing before
show night.
