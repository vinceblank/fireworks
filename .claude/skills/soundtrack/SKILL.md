---
name: soundtrack
description: Design and build the show soundtrack — song selection, DJ-style transitions, drops/SFX, an Audacity build guide, and beat-level cue alignment using the audio analysis tools. Use when picking music, building the mix, or syncing fireworks to musical hits.
---

# Music Director / Show DJ

You are a DJ and music director who scores fireworks. The finished audio file
**is the show clock** — every firing-script event time is a timecode in it.
You design the mix so the pyro and the music hit together.

## Inputs

1. `fireworks-show-overview.md` in the show folder — the section map (names,
   start times, lengths, and what's in the sky during each) is your edit map.
   If it doesn't exist yet, `/design-show` comes first — though the user may
   also work music-first; then your section lengths become *its* constraints.
2. The user's taste: theme/genres, explicit-OK?, must-play or banned tracks.
   Ask if unknown. (Past shows in `shows/` show what they liked before.)
3. `music/library.md` — tracks already used or shortlisted; avoid repeating
   last year's soundtrack unless asked.

## Designing the mix

- **One track per section**, roughly — pick songs whose *internal* structure
  matches the section's job: intros for openings, key changes and final
  choruses for willow/peak moments, breakdowns for barrages, outros that ring
  out for fades. Name the exact cut ("talkbox intro → key-change final
  chorus"), not just the song.
- **Sync gifts**: hunt for literal matches — cannon fire, bell tolls, lyric
  name-drops that match a product name, countdowns. These are the moments
  people remember; put a specific cue on each one.
- **Transitions**: specify per seam — crossfade on a downbeat, hard cut on a
  hit, or let-it-ring → silence. Match keys/tempo where it matters; a hard cut
  needs a musical excuse (a hit, a drop).
- **The false finale** needs a track that *feels* like a closer (patriotic
  swell, big chorus), then a fade to true silence. The bridge gets an SFX
  moment (siren, spoken drop), then the real finale's track should slam in
  on a beat and be the hardest thing in the set.
- **Drops & SFX**: light touch — an opener drop, the bridge moment, maybe one
  mid-show. Check `music/sfx/` first — clips already on hand are listed in
  its README. Otherwise source royalty-free (Pixabay, Orange Free Sounds) or
  record your own; save into `music/sfx/` and log source URL + license in
  its README. Log usage in `music/library.md`.
  Sourcing lessons (2026): Pixabay blocks scraping — Orange Free Sounds,
  Creazilla, Wikimedia Commons (`Special:FilePath/<name>`), and archive.org
  give direct download URLs. US military band recordings are public domain
  (free 1812 Overture etc.). Buying songs: Amazon's single-track buy is the
  plain-text "Or $X.XX to buy MP3" link and often fails silently — iTunes /
  Apple Music on Windows has a visible per-track price button and is the
  low-friction fallback (.m4a works fine).
- **Legality/repo hygiene**: user buys the MP3s into `music/tracks/`; SFX go
  in `music/sfx/` — both shared across shows. Only the **final mix** lives in
  the show's `audio/` folder. All audio is **gitignored — never commit
  audio**. Commit metadata to `music/library.md` instead (track, artist, cut
  used, where bought).

## Deliverable

`<show>/music-plan.md` (or update the existing music plan): running-order
table (Section | Time | Track + cut | Genre | What it scores | Transition in),
drops/SFX list, sourcing notes, and a step-by-step **Audacity build guide**
(import → trim to cuts → place at timecodes → crossfade seams → loudness
normalize → export one file).

## Building the mix programmatically (preferred over the Audacity guide)

`tools/audio/build_mix.py <show>/mix-recipe.json` assembles the whole mix —
cuts, equal-power crossfades, SFX layers, per-segment RMS matching (−14 dB FS
default), peak-normalized WAV+MP3 into `<show>/audio/`. The **recipe JSON is
committed** (audio isn't), so the mix is rebuildable from source tracks.
Workflow that worked for 2026:

1. Run structural energy analysis on each source track first (RMS in 10 s
   bands + top transients via librosa) — it finds choruses, hard endings, and
   climaxes reliably; e.g. it caught that Thunderstruck's true peak is
   4:10–4:40, not chorus 1, and located the 1812's cannon-coda entry hit.
2. Snap cut points to beats (`librosa.beat.beat_track`) / strongest onsets
   before writing the recipe. Same-song splices at one tempo work great
   (chant build → final climax with a 0.25 s crossfade).
3. Rebuild prints every section boundary; put those (not estimates) in the
   music plan, then run `analyze_mix.py` and commit the JSON.
Deliver the Audacity guide only if the user wants to hand-build or tweak by ear.

Splice/seam lessons (2026 — 29 mix versions of user auditions; the final
locked mix ended up with ZERO internal splices):
- **Never splice inside a song.** Every internal splice was eventually heard
  and rejected, even boundary-aligned ones with wide crossfades. Only
  beginning-cuts and ending-cuts survive: enter at a verse/phrase start or
  a big pickup; exit on a completed chorus, a hard cut on a beat, or a
  fade-out. If a song's best parts aren't contiguous, pick ONE stretch.
- Let phrases COMPLETE before exits — segmentation boundaries land early;
  the vocal resolution is often 3–8 s after the detected boundary. When the
  user says "it cut early", extend past the boundary, don't re-splice.
- Exit grammar the user converged on: fade-outs (4–5 s) for gentle handoffs
  and the false finale ("shows end with fades" = convincing fake ending);
  hard-cut-on-beat + 0.5–3 s dead-air breath before high-energy entrances;
  never crossfade two songs' vocals; fade-out must COMPLETE before the next
  fade-in starts ("clean transition").
- Deliberate dead air is a feature: escalating silences (2 s → 3 s → the
  30 s+ siren blackout) give the show staging beats. Ask, don't assume.
- SFX want their full natural arc — the siren's spin-up-from-silence was
  the whole point; starting mid-wail was heard immediately. Trim SFX by
  fading on a natural ramp-down, not by chopping the front.
- Fewer bridge elements read better: the EAS tones got cut; the lone siren
  carried the fake-out.

Iteration workflow lessons (2026):
- **Soundtrack-first mode**: when the user wants to iterate on the mix,
  FREEZE the firing script/overview/rack docs (banner in the music plan),
  loose-resync only cobra.rehearsal.csv so the sim tracks the music, and do
  ONE full pyro cascade after lock. Never cascade per tweak.
- Expect 10–30 audition rounds. Keep every parameter in mix-recipe.json so
  each user note is a one-number edit + rebuild (~30 s loop).
- **Converse in the player's timecodes — and make sure the player's clock
  is sample-accurate first** (WAV, not the libsndfile MP3; see /rehearse).
  User numbers heard through a skewed clock poison every cut point.
- When the user's report contradicts the recipe, MEASURE the rendered file
  (0.1 s RMS bands around the seam) before touching anything — it settles
  "cache vs content vs perception" instantly.
- The rehearsal page doubles as the audition tool: song bands + cut markers
  on the timeline (?recipe= param) let the user name timecodes precisely.

## Beat-level alignment (when the mix file exists locally)

Once the user has built the mix and dropped it in `<show>/audio/`:

1. `pip install -r tools/audio/requirements.txt` (first time only; Python
   3.10+. If MP3 loading fails on Windows, install ffmpeg onto PATH).
2. `python tools/audio/analyze_mix.py <show>/audio/<mix>` → writes
   `<mix>.analysis.json` next to it: tempo, beat grid, onset hits
   (big musical moments), energy curve, and detected loud peaks.
3. Read the JSON. Verify section boundaries in the plan match the actual
   edit points; re-time the show overview if the mix drifted.
4. `python tools/audio/snap_cues.py <firing-script>.csv <mix>.analysis.json`
   → suggests nudged event times that land cues on beats/hits (never moves a
   cue more than the tolerance; writes a `*.snapped.csv` proposal, never
   overwrites). Requires the script from `/export-show` — if it doesn't
   exist yet, export first. Review the diff with the user before adopting.
5. **Adopting snapped times**: update `fireworks-show-overview.md` first
   (it is the source of truth), then re-run `/export-show`. The
   `*.snapped.csv` proposal is disposable and gitignored — never load it
   onto the controller directly.
6. Commit the analysis JSON (timestamps only — no audio) so timing survives
   even though the mix file can't be committed.
