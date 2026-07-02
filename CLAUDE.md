# Fireworks Show Workspace

Workspace for designing music-synchronized fireworks shows with Claude Code:
inventory → choreography → soundtrack → firing-system script.

## Map

| Path | What it is |
|------|------------|
| `equipment.yaml` | The user's firing system, racks, and site. **Read this first.** Run `/setup` if missing or stale. |
| `devices/` | Firing-system knowledge base — one technical profile per device (channels, cues, script export format). `devices/firing-systems.md` covers generic concepts; `devices/TEMPLATE.md` is the profile skeleton. |
| `shows/<year>-<name>/` | One folder per show (e.g. `shows/2026-july-4/`). Contains inventory, `fireworks-show-overview.md`, music plan, exported firing script, and a gitignored `audio/` folder. |
| `music/` | Shared music/SFX library notes. Audio files themselves are **gitignored** (copyright) — only metadata and build notes are committed. |
| `tools/audio/` | Python audio analysis: beat/hit detection on the final mix, cue-time snapping. |

## Skills (the workflow, in order)

1. `/setup` — create or update `equipment.yaml`; researches unknown firing systems into `devices/`.
2. `/design-show` — choreograph a show from a show folder's inventory.
3. `/soundtrack` — design and build the music mix; align show sections to musical structure.
4. `/export-show` — generate the firing-system-native script (e.g. Cobra CSV) and validate it.
5. `/field-setup` — setup-day wiring tables, ground layout groups, and checklists; optional push to Google Drive for phone access.

## Rules that persist across shows

- **Equipment is the only constant.** The product inventory is brand-new every show — never carry forward prior-year product names or layouts. Prior show folders are format/pacing reference only.
- **Cues:** cakes are one cue each; mortars fire in fused groups, one cue per group. Never exceed a module's cue capacity; balance load across modules.
- **Pacing:** no dead air — overlap consecutive cues ~10–20 s. Spread near-identical items apart. Reserve mortar groups and the biggest cakes for the finale. Use every inventory item unless told otherwise.
- **The soundtrack file is the show clock.** Every scripted event time is a timecode in that audio file.

## Conventions

- New show: copy nothing — create `shows/<year>-<name>/`, drop the inventory file in, run the skills in order.
- Never commit audio files (`.gitignore` enforces this). Local music lives in `shows/<show>/audio/` or `music/`.
- Deliverables per show: `fireworks-show-overview.md` (human/wiring-friendly, sectioned tables: Time, Ch, Cue, Firework, Shots/Duration, Notes), a music plan, and the firing script export.

## Safety

This workspace plans **consumer fireworks shows operated by the owner**. Always
include continuity-test and arming steps in run-of-show docs, never suggest
shortening safety distances, and flag any cue spacing that requires someone
downrange of live product.
