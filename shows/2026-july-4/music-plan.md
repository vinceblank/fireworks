# 2026 Show — Music Plan (FINAL — MIX v29 LOCKED 2026-07-03)

**The soundtrack is LOCKED.** `shows/2026-july-4/audio/2026-show-mix.wav`
(+ `.mp3` for phone playback), **10:53.0**. Built by
`tools/audio/build_mix.py` from `mix-recipe.json` (committed — the mix is
always rebuildable). Any change reopens the lock and requires a full pyro
re-cascade. Analysis JSON (beat grid ~136 bpm, 532 hits) is committed.

> ✅ **Pyro re-lay COMPLETE (2026-07-03):** overview FINAL + cobra.csv FINAL
> are laid against this locked clock using the 27 confirmed highlights and
> the as-wired mortar model. See `fireworks-show-overview.md`.

## Locked running order (mix timecodes — the show clock)

| # | Piece | Mix | Source cut | Exit |
|---|-------|-----|-----------|------|
| 1 | **American Kids — Kenny Chesney** | 0:00–2:20 | 0:00→2:15.4 | 5 s fade-out (2:15.4→2:20.4) |
| 2 | **Only in America — Brooks & Dunn** | 2:20.6–4:51 | verse 2 (1:37.8)→final-chorus resolution (4:08.5) | 2 s fade-in entry; 1.2 s chorus ring-down exit |
| 3 | **Crazy Train — Ozzy Osbourne** | 4:51.8–7:18 | 0:00 ("ALL ABOARD!" rides song 2's ring)→2:26.2 (chorus 2 complete) | hard cut |
| — | *3 s dead air (staging beat)* | 7:18–7:21 | | |
| 4 | **Thunderstruck — AC/DC** (false finale) | 7:21–9:16 | 0:00 (chants fade in from dark)→1:55 | 4 s fade-out (9:12→9:16) — "the show is ending" |
| — | *3 s silence* | 9:16–9:19 | | applause bait |
| — | **Air-raid siren** | 9:19–9:47 | full natural arc: spin-up→wail; fades on a ramp-down | low rumble underneath |
| — | *1.8 s dark* | 9:47–9:48.8 | | |
| 5 | **1812 Overture — U.S. Marine Band** (real finale) | 9:48.8–10:53 | 11:08.8→12:12 of the recording (+1 dB) | natural final chord, 4 s tail |

**No internal splices anywhere** — every song is one continuous passage
(beginning and/or ending cuts only). EAS tones were CUT from the bridge
(clip retained in `music/sfx/` for future shows).

Loudest mix instants: 8:05, 8:19, 8:32, 8:47, 9:03, 9:13 (Thunderstruck
build/chorus) and **10:03, 10:19** (1812 frenzy) — prime mortar targets for
the re-lay. Designed silences: 7:18–7:21, 9:16–9:20, 9:46–9:49.

## Show start & manual sync (unchanged)

Strobe (Ch 1 Cue 16, MANUAL) → start mix on phone/BT speaker → **press the
script trigger at mix 0:06** (user-called press point — 2 s before the
first lyric; hearing the lyric right after the press confirms timing) →
script runs the show. Cobra time = mix − 6.0 s. 18R2 +/− nudges drift.
Practice disarmed.

## Next steps (in order)

1. ✅ Cue re-lay done (overview FINAL, cobra FINAL, rehearsal validated).
2. User reviews the full show in the rehearsal player.
3. Re-push the rack plan to Google Drive with final fire times.
4. Optional: re-encode the phone MP3 with a proper seek header.
5. `/field-setup` when wiring day approaches; USB load + 18R2 dry run.

## Sourcing (all acquired — `music/library.md`)

Songs ~$5.16 in `music/tracks/`; 1812 public domain; siren/rumble CC in
`music/sfx/`; EAS clip unused this year.
