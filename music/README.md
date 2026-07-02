# Shared Music Library

Audio files (`.mp3`, `.wav`, …) placed here are **gitignored** — copyrighted
music never gets committed. What *is* committed:

- `library.md` — metadata for every track and SFX clip used or shortlisted
  across shows (artist, cut used, which show, where purchased).
- `sfx/` — notes on sound-effect sources (sirens, announcer drops). Royalty-
  free SFX files are still gitignored for consistency; keep source URLs in
  `library.md` so they're re-downloadable.

Per-show final mixes live in `shows/<show>/audio/` (also gitignored); their
`.analysis.json` timing files **are** committed so cue timing survives.
