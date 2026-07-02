# 🎆 fireworks

A Claude Code workspace for designing **music-synchronized fireworks shows** —
from a pile of cakes and mortars to a scripted, soundtrack-locked firing plan.

Built around the COBRA 18R2 but designed to work with **any firing system**
(controller + N stations × M cues): device knowledge lives in [`devices/`](devices/),
your specific rig is described once in [`equipment.yaml`](equipment.yaml).

## Workflow

```
/setup        →  describe your firing system, racks, and site (equipment.yaml)
/design-show  →  choreograph the show from this year's inventory
/soundtrack   →  design the music mix; the audio file becomes the show clock
/export-show  →  generate + validate the firing-system script (e.g. Cobra CSV)
/field-setup  →  setup-day wiring tables + ground layout; push to Google Drive
                 so the instructions are on your phone in the field
```

Each show lives in `shows/<year>-<name>/` — inventory in, show overview +
music plan + firing script out.

## What's here

- **`.claude/skills/`** — the four skills above, usable by anyone who clones this repo with Claude Code.
- **`devices/`** — researched firing-system profiles (COBRA 18R2 today; the `/setup` skill researches and adds new devices on demand).
- **`tools/audio/`** — Python beat/energy analysis of your final mix, plus a cue-snapper that nudges firing times onto musical hits.
- **`shows/`** — real shows, kept as working history and examples.

> 🎵 Music files are **never committed** (copyright) — `.gitignore` blocks all
> audio formats. Only plans, timestamps, and analysis outputs live in git.

## Safety

Consumer fireworks are dangerous. This repo helps with *planning and scripting*;
follow your firing system's manual, local laws, and safety distances. Test
continuity, keep a deadman on the button, and never let choreography pressure
you into unsafe wiring or spacing.
