# Shared Music Library

**All reusable audio lives here** — purchased song MP3s and royalty-free SFX
are assets that outlive a single show. Only a show's *final mix* is
show-local (`shows/<show>/audio/`). Audio files (`.mp3`, `.wav`, …) are
**gitignored** everywhere — copyrighted music never gets committed. What *is*
committed:

- `library.md` — metadata for every track and SFX clip used or shortlisted
  across shows (artist, cut used, which show, where purchased/downloaded).
- `tracks/` — purchased song MP3s (local only). Buy once, reuse in any mix.
- `sfx/` — royalty-free sound effects and recorded voice drops (local only).
  Its README logs source URLs + licenses so clips are re-downloadable.

Per-show final mixes live in `shows/<show>/audio/` (also gitignored); their
`.analysis.json` timing files **are** committed so cue timing survives.
