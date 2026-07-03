# COBRA 18R2 Firing System — Technical Reference

<!-- status: verified (official COBRA docs, compiled 2026-07-02) -->

Technical knowledge base for choreographing shows on the COBRA wireless firing system (cobrafiringsystems.com). Compiled July 2026 from official COBRA user guides and help-center articles (help.cobrafiringsystems.com). Firmware-dependent values are noted; current stable firmware families are 6.1.x / 7.1.x, with 8.0.x in beta/hotfix rollout.

## 1. System Architecture

| Device | Role | Key numbers |
|---|---|---|
| **18R2 remote** | Handheld transmitter/controller. Fires manually, runs AUTO-FIRE sequences, and executes uploaded scripts. Stores scripts on internal 4 MB flash (script + continuity + firing history); USB port on right side for script upload. | 18 cue buttons, CH+/CH-, STEP, AUTO-FIRE, ARM, TEST/DISARM, SYNC keys; keyswitch ON; LiPo ~20 h (legacy 3×AA ~7 h); 2.43 lb |
| **18M module** | 18-cue field firing module. Keyswitch TEST/ARM. Set to one channel (hold CH+/CH- ~1 s to change). Two firing modes: e-match (0.1 s pulse) or Talon/clip-on (2 s pulse). | 18 cues; 3×9V, 14.8 V 900 mAh COBRA LiPo, or 12–24 V DC ext.; 36 h active / 108 h sleep on LiPo |
| **36M / 72M module** | Multi-bank modules = two (36M) or four (72M) internal "18Ms". Each 18-cue bank (A/B or A–D) is assigned its own channel; CHANGE BANK button toggles banks for continuity display. DMX signal output for SPFX (lights, flame, cryo). | 36M: 2 banks/36 cues; 72M: 4 banks/72 cues; same power options as 18M; 18 h active on LiPo |
| **6M module** | Compact 6-cue module; can be set to occupy cue range 1–6, 7–12, or 13–18 of a channel, so three 6Ms can tile one 18-cue channel. | 6 cues; DB9 connector to terminal-block or Quickplug adapters/slats; 14.8 V 550 mAh LiPo, 22 h active |
| **Audio Box** | Wireless audio playback device for pyromusicals. Holds the show MP3 on a USB drive; the 18R2 starts/keeps it in time with the script over the radio. Outputs: headphone, RCA, 1/4", optional single unbalanced or dual balanced XLR; independent L/R volume knobs (~80% recommended). Gen 2 has LCD status display and 2000 mAh LiPo (~10 h; legacy 3×AA ~1.5 h). | Counts as one "device" in module counts |
| **Slats (18S/36S, 6S)** | Passive cue strips (no logic/radio) cabled to a module's slat port. They *mirror* the module's cues at a remote physical position — they never add unique cues. Multiple slats can chain onto one module (series or parallel type — don't mix types in one chain). | 18- and 36-cue versions; 6S series/parallel and Quickplug variants for 6M |
| **Deadman handheld** | Fail-safe trigger accessory (18R2 needs firmware 4.0+). Script only fires while the trigger is held; releasing stops firing. Also has integrated STEP and Alternate-fire buttons. | Header value `deadman` |
| **Range accessories** | Booster (omnidirectional amplification) and DISH (directional antenna) for multi-mile links. | — |
| **Control Panel / Show Operator (PC-Mac) apps** | Optional monitoring/control software: system-wide continuity and signal view, script selection by name, disable firing/modules/groups mid-show. | Disable groups & per-module disable need fw 7.1+ and Control Panel Gen 2 |

### Wireless protocol
- 2.4 GHz (fixed "Channel 4"), FCC/CE/IC certified (ID U90-SM220), bi-directional transceivers — modules report continuity, signal strength, battery, and arm state back to the remote.
- Encryption: IEEE MAC-address pairing / encrypted data. Devices must be **synced** (paired) to a remote once; they remember sync and address through power cycles.
- Range: **500 m (1,650 ft)** line of sight base. With **MESH** (firmware 5.0.2+), every module/Audio Box is an automatic repeater: **+450 m per device, up to 10 hops** — multi-km reach with no operator configuration.
- Key reliability design: on ARM, the 18R2 **downloads the full event list into each firing module**; modules fire "on auto-pilot" on the remote's timing pings, so brief interference doesn't drop cues. (Firmware 8.0 beta adds a *Script Timeout* — see header column K — that self-disarms a module that loses pings.)
- Operating temp: −40 °F to 130 °F (−40 °C to 54 °C); cold reduces firing current (see §9).

## 2. Channels, Cues, Addresses, Banks

- A **channel** groups remote and modules: with the remote on channel 1, pressing cue 5 fires cue 5 on *every* module set to channel 1. Multiple modules may share a channel (mirrored positions).
- **Channels:** 00–99 (firmware ≤5.1) or **00–199 (firmware 6.0+)**.
- **Cues:** 1–18 per channel/bank (script accepts values 0–18; 0/blank used for DMX-only or comment-style rows).
- **Addresses:** every synced device gets a unique address at sync time. 36M reserves 2 consecutive addresses (banks A,B), 72M reserves 4 (A–D); 6M/18M use 1. Limits: fw ≤5.1 — 100 channels / 1,800 total cues; **fw 6.0+ — 400 addresses (A00–A399), 200 channels, 3,600 total cues** (= 200 channels × 18 cues). Example: 400×18M or 100×72M max by address budget; 200 independent channels is often the binding limit.
- Module count on the 18R2 counts **physical devices** (a 72M + Audio Box = 2 devices, despite 4 banks).

## 3. Firing Modes

1. **Manual fire** — select channel with CH+/CH-, press cue buttons 1–18; instant, multiple buttons simultaneously, no rate limit (overlapping "grid-fire" redundancy). Firing memory LEDs: green = live/unfired, red = fired, blinking red = last fired. Fw 6.0+: cue fires as long as button held (min 2 s in Talon mode).
2. **Basic STEP** — press STEP to fire cues 1→18 sequentially on the current channel; auto-increments to next channel after cue 18. No module-hopping.
3. **AUTO-FIRE** — on-remote sequence: set start cue (S01…), end cue (E12…), delay 0.1–99 s between cues; press AUTO-FIRE to run (can run backwards, e.g. S12→E01; hold to continue across channels; press again = stop, "Stp").
4. **Scripted shows** (uploaded CSV): three script types —
   - **Timed Event**: entire show fires automatically from one trigger button press; unlimited simultaneous channels/cues at 1/100 s resolution.
   - **STEP script**: pre-planned order, one button press per event; hops across channels/modules freely; can fire several modules per press.
   - **STEP/Timed hybrid**: STEP rows pause the script ("SP" on display) and following timed rows run relative to that STEP (the clock **resets to 0 at each STEP**).
   - **Observed (owner rig, 2026 dry-run)**: with header Trigger Button = `STEP`, the FIRST STEP press starts/queues the script (nothing fires; display shows the pending STEP row) — the SECOND press fires the first STEP row. Budget one extra "wake" press in run-of-show docs.
   - While a timed script runs you can still fire cues manually (slightly reduces redundancy of the manual commands), nudge timing with **+/−** buttons (disabled under SMPTE), or press STEP to jump immediately to the next event.

### Scripting capacity by firmware
| Firmware | Capacity / restrictions |
|---|---|
| 3.0–5.0 | 100 channels / 1,800 cues in the *first* script; secondary scripts limited to ≤2 channels per 0.4 s window; 1/10 s resolution |
| 5.0+ | 1/100 s resolution, custom audio filenames; 5.1: custom script filenames, SMPTE, script comments |
| 6.0–6.1 | 200 channels / 3,600 events in primary script; re-fire + variable pulse time (primary script only); DMX (primary only) |
| 7.1+ | All scripts downloaded to modules: up to **32 scripts per CSV, 7,600 pyro events + 10,000 DMX events**, no 2-channel/0.4 s restriction, re-fire in all scripts, disable groups |
| 8.0 beta | Script ping timeout (header col K), arming fixes |

Other hard limits: **max 3,600 events per program (Error 6)**; **<400 events per channel** stored in a 6M/36M/72M/18M-hardware-B module (excess events won't execute); 18M **hardware A** (pre-June 2015): 18 events total, no re-fire/pulse-time/multi-script/disable features. Historical (fw 2.x-era) docs cite 100 scripts per remote and 1,000 events per single script.

## 4. Script CSV Format (`cobra.csv`)

Comma-separated `.csv`. Rows beginning with `#` are comments (the familiar `#Trigger Channel,...` and `#Event Time,...` rows are just informational headers). A file contains one or more scripts, each = **one header row + event rows**; the file's **last line must be `end`** in column A (only once, at end of file — missing it gives Er4; this repo's shows used uppercase `END` and fired fine, so case appears not to matter, but lowercase matches the official docs). Events must be in ascending time order (Error 21). Multiple scripts in one file: first script triggered by its channel+button wins on conflicts.

### Header row (one per script)
| Col | Field (a.k.a.) | Values / meaning |
|---|---|---|
| A | **Trigger Channel** (optional) | Channel the 18R2 must be on for the trigger to work; 0–199 (fw 6+) / 0–99 (≤5.1). Blank = triggers on any channel. COBRA suggests channel 0. |
| B | **Trigger Button** (required) | Button that starts the script: `1`–`18`, `STEP`, or `AUTO-FIRE` (Finale default export: channel 00, button 1). |
| C | **Deadman Button** (optional; pre-4.0 "Confirmation Button") | `1`–`18` (a second button that must be held) or `deadman` for the COBRA Deadman accessory. Must differ from Trigger Button. Script fires only while held. |
| D | **Return Channel** (optional) | Channel the 18R2 jumps to when the script ends (set it to the next script's trigger channel in multi-script files). 0–199/0–99. |
| E | **AudioBox Filename** (optional) | MP3 the Audio Box plays when the script starts. fw 3.0/4.0: literally `audiobox` (file must be `audiobox.mp3`); fw 5.0: custom ≤12 chars incl. `.mp3`; fw 5.1: ≤45; **fw 6.0+: ≤31 chars incl. `.mp3`**. Allowed chars: 0-9 a-z A-Z `-` space (not leading). Must match the file on the Audio Box USB exactly ("Filename mismatch" error otherwise). |
| F | **Script Name** (optional, fw 5.0+) | Display name for choosing scripts in Control Panel; ≤35 chars (Show Creator limit). |
| G | **Disable Firing Button** (optional, fw 5.0+) | `1`–`18`. Press mid-show to stop modules firing while script+audio continue; press again to re-enable. |
| H | **Alternate Firing Button 1** (optional, fw 4.0+) | `1`–`18` (not STEP/AUTO-FIRE). Each press fires the next `ALTERNATE` event (black-sky filler). Deadman's right-hand button also fires Alternate 1 without any header entry. |
| I | **Alternate Firing Button 2** (optional, fw 5.0+) | `1`–`18`; fires the `ALTERNATE2` list. |
| J | **SMPTE Timecode** (optional, fw 5.1+) | `timecode1` (keep firing if timecode lost — untrusted audio feed) or `timecode2` (pause/resume and chase timecode — trusted feed). |
| K | **Script Timeout** (fw 8.0 beta) | Seconds a module keeps firing without hearing the remote before self-disarming: 10–300 (default 60); 0 = never (use with caution). |

Example header: `0,1,,1,mymusic.mp3,My Show,17,16,,timecode2`
Example with deadman + both alternates: `1,1,deadman,1,,,,17,18`

### Event rows
| Col | Field (a.k.a.) | Values / meaning |
|---|---|---|
| A | **Event Time** | `hh:mm:ss.ss` since trigger press (loose parsing: `1.5`, `30.00`, `1:30.00`, `05:12.20`, `01:10:01.30`; trailing `s` allowed, e.g. `00:00:01.0s`). Resolution 1/100 s (fw 5.0+; 1/10 s before, one decimal). A decimal is required (`1.0`, not `1`); negatives rejected; rows must be chronological. Special keywords: `STEP` (wait for STEP press; **subsequent timed rows are relative to the STEP, clock resets to 0**; a `00:00:00.0` row fires together with the STEP), `ALTERNATE` / `ALTERNATE2` (event fires from the alternate button queues instead of the timeline; place list anywhere before `end`). |
| B | **Channel** | 0–199 (fw 6+) / 0–99. If blank, the header Trigger Channel is used. |
| C | **Cue** | 0–18 (normally 1–18; Error 17 outside range). |
| D | **Event Description** | Free text, e.g. `Blue Mine` (keep commas out; legacy limits: ≤540 chars, ≤10 commas, ≤20 columns per row). |
| E | **Disable Groups** (fw 7.1+) | Group label, ≤64 chars a-z A-Z 0-9 (e.g. `High Wind`). Same-named events form a group that Control Panel Gen 2 can disable/enable instantly mid-show (Menu > Show Controls > Disable Firing); **max 10 groups per script**. Not on 18M hardware A. |
| F | **Fire Time / Pulse Time** ("Duration" in Finale 3D) | How long the cue is energized: 0–20.0 s, 0.01 s (help docs also say 0.1 s increments). Blank = module's default mode (e-match 0.1 s / Talon 2 s). Enables re-fire choreography for flame projectors, cryo jets, etc. Re-fire = simply another event row with the same channel+cue at a later time. Not on 18M hardware A. |
| G | **AUX Value** | Reserved / not currently supported ("future firmware"). Leave blank. |
| H | **DMX Universe** (required for DMX event) | 1–99. |
| I | **DMX Channel** | 0–200 (COBRA hardware supports first 200 of the 512 DMX channels). |
| J | **DMX Value** | 0–255. |
| K | **DMX Duration / DMX Pulse** | `MM:SS.XX`, 0 s–10 min, 1/100 s resolution (e.g. `01:10.30`). Blank = value held continuously until another event overwrites it (useful as master-on/off); when nothing is being sent, 0 is output. |

A single event row may combine a pyro fire and a DMX action at the same event time, each with independent pulse durations.

Minimal example:
```
#Trigger Channel,#Trigger Button,#Deadman Button,#Return Channel,#AudioBox Filename,#Script Name
0,1,,1,audiobox,My Script
#Event Time,#Channel,#Cue,#Event Description
00:00:01.0s,2,1,shell
00:00:02.0s,2,2,shell
00:00:03.0s,2,3,shell
end
```

### File naming, upload, and errors
- Filename: **fw ≤5.0.5 must be exactly `cobra.csv`**; fw 5.1+ any name ≤42 chars incl. `.csv`; fw 6.0+ ≤32 chars. **Only one .csv on the drive**, in the root directory (Error 1 otherwise). Small (1–16 GB) SanDisk-class or COBRA-certified drives recommended; some sticks aren't recognized (no LEDs) — try smaller/restart.
- Upload: insert USB with 18R2 **off**, power on; red LEDs circle while loading; **all-green flash = loaded OK; all-red + `Er` codes = errors**, shown as code then line number (e.g. Er 21 @ line 110). Script persists in flash after USB removal/power-down. Loading a new file replaces scripts; clear all scripts by holding **TEST+SYNC 10 s** (or load a file containing only `end`), then restart.
- After load, the 18R2 lights **red LEDs on every scripted channel/cue that lacks continuity** — your wiring checklist.
- Notable error codes: 1 file not found/name; 4 missing `end`; 5 >100 scripts; 6 max events; 7 header w/o events; 8 events w/o header; 9 >1,000 events in a script; 14/15 channel out of range; 17 cue out of range; 18/19 trigger button problems; 21 events out of order; 22 >2 channels in 0.4 s (legacy firmware/secondary scripts); 23/24 description/columns too long.

## 5. COBRA Show Creator (cobrashowcreator.com)

- Official web-based scripting app (Chrome; robust offline mode with cloud sync; production + beta branches; subscription-licensed; current release v2.2). Imports your firework inventory (Wiki Fireworks database or bulk CSV), displays the music **waveform** for placing events, validates the script against your selected firmware version, and supports DMX scripting, custom columns (Position, Angle, Rack…), cue shifting, and combined-audio building (merge multiple tracks, optionally with a SMPTE channel).
- **Show Settings** map 1:1 onto the CSV header: Show Name, Estimated Duration, Firmware Version, Trigger Channel (0–99), Trigger Button (1–18/STEP/AUTOFIRE), Return Channel, Use COBRA Audio Box (writes the AudioBox Filename argument), Deadman Button (1–18 or Deadman), Disable Firing, Alternate Firing 1/2 (≤18 events per alternate list), Script Name, Audio Box Filename, SMPTE Timecode (None/Timecode1/Timecode2).
- **Event Time vs Sub-Event Time**: adding a STEP event exposes a Sub-Event Time column — the time written to the CSV is relative to the preceding STEP (resets to 00:00.00 at each STEP); editable directly or by dragging pills on the waveform.
- **Export** (left menu): downloads the script CSV (rename to `cobra.csv` for fw ≤5.0.5) and separately the show MP3 (named from the Audio Box Filename setting) for the Audio Box USB. Show Creator cannot author multi-script files — export scripts separately and merge in Excel/Notepad; Finale 3D exports each "track" as its own script.
- Alternatives: Finale 3D and ShowSim both export COBRA CSV; plain Excel/Notepad works.

## 6. Audio Sync (Audio Box & SMPTE)

**Audio Box path (recommended, no cables):**
1. Produce the final soundtrack and format it in **Audacity** even if edited elsewhere: **MP3, 320 kbps, Constant bit rate, Stereo, 44100 Hz** — incorrect formatting is the #1 cause of audio drifting ahead/behind the pyro.
2. Name it to match header column E (fw 6.0+: ≤31 chars incl. `.mp3`) and copy to the Audio Box's USB drive (COBRA-certified/SanDisk recommended). Other files are fine, but with multiple MP3s the filename must match the script argument exactly or nothing plays.
3. Sync the Audio Box to the 18R2 once (SYNC pairing, same as modules). It participates in MESH.
4. When the operator presses the trigger button, the 18R2 starts the script and wirelessly commands the Audio Box to play the named MP3; timing stays locked to the remote. Audio continues even if Disable Firing is active. **Always dry-run the script with the Audio Box** — the TEST AUDIO button is only a volume check, not a format/argument test.

**SMPTE path (fw 5.1+, hardware upgrade available for older 18R2s):** the 18R2 chases LTC timecode carried as an audio signal from a sound source (COBRA sells a 90-min sample file; Show Creator can embed a SMPTE track on one channel of a combined file). Header col J picks sensitivity: `timecode1` = keep firing if code is lost; `timecode2` = pause/resume and follow rewinds/fast-forwards. Timecode quality displays as TC0–TC9 in TEST/ARM. The +/− script-nudge buttons are disabled under SMPTE. SMPTE is *not required* for pyromusicals — the Audio Box (or even a "3-2-1-go" simultaneous press) covers most shows.

## 7. Igniters, Continuity, Firing Capacity

- **Igniter types:** professional e-match and MJG Firewire initiators (fire in **E-Match mode, 0.1 s pulse**; series or parallel) and Talon/clip-on igniters (fire in **Talon mode, 2.0 s pulse**; **parallel only**). Toggle mode per module: hold SYNC+CH+ → `2.0` (Talon), SYNC+CH− → `0.1` (e-match); setting persists. Quickplug connector variants exist for both.
- **Max igniters per cue** (room temperature):

| Power source | Talon (parallel) | E-match/MJG series | E-match/MJG parallel |
|---|---|---|---|
| Energizer 9V | 2 | 8 | 5 |
| COBRA 14.8 V LiPo | 4 | 9 | 9 |
| External 12–24 V (24 V/10 A assumed) | 5 | 16 | 12 |

- Long shooting wire derates these (e.g. ~50 ft of 22 AWG ⇒ ~80% of table). Cold weather derates hard: 0–32 °F ⇒ max 2 parallel / 4 series per cue; below 0 °F ⇒ 1 igniter per cue; check LiPo labels for `V-C`/`V-D` cold rating.
- **Continuity** = verified circuit between cue terminal and igniter, tested with a small pulse. Check **locally** at each module (TEST button; CHANGE BANK on 36M/72M) after wiring, then **remotely** from the 18R2 across every channel. LED language on the remote: **green = good continuity; red = scripted cue with no continuity; blinking green = several modules share this channel and at least one lacks continuity**. Press TEST repeatedly to cycle per-address views on shared channels; press SYNC on the remote for signal strength (negative dBm-style value).
- Series = all-or-nothing but detects any bad igniter; parallel = tolerant but can mask a bad igniter. Don't mix series and parallel on one module.

## 8. Safety Features & Gotchas

- **Keyswitches everywhere:** modules only fire with key at ARM; remote requires ARM press. TEST mode is safe-to-handle.
- **Arming:** press ARM on the 18R2 → ARM LED blinks while each device confirms **and the script downloads into the modules** (~1–2 s per module; fw 7.0+: module ARM LED blinks during download, solid = script loaded; fw 8.0: TEST LED). **Do not fire until the ARM LED is solid** and the armed-device count matches. `A##` shown persistently = that address is off, out of range, or still keyed to TEST.
- **Disarm/abort:** TEST/DISARM instantly stops all firing (even mid-script). ARM doubles as pause/resume during scripts; after an abort you can re-arm, restart the script, and STEP forward to catch up.
- **Deadman:** release = firing stops; script/audio behavior per header config.
- **Disable options mid-show:** header Disable Firing button (all modules; script+audio continue); Control Panel Gen 2 (fw 7.1+) per-module disable and per-group disable via Disable Groups masks (survive script stop, reset on module power-cycle).
- **Weather:** −40 °F–130 °F rated electronics, but modules are not submersible — keep them elevated off wet ground, lids closed, wires out the side of armored cases; never power a wet module (dry fully, check corrosion). Shade modules in extreme heat (36M/72M can throw "Low Driver" errors when hot).
- **Gotchas:** holding buttons during 18R2 boot triggers Er3 (stuck-key check). Finale exports start time at first cue — add a dummy cue at t=0 for music alignment. Secondary scripts on fw ≤6.1 keep the 2-channels-per-0.4 s limit. 18M hardware A lacks: pulse time, re-fire, disable groups, multi-script, hold-to-fire. Modules sleep until the 18R2 wakes them, so field modules can be powered on early. Only ~400 stored events per channel will execute. Re-check continuity after any module move, channel change, or script reload.

## 9. Standard Show Workflow

1. **Design** in COBRA Show Creator (or Finale 3D/ShowSim/Excel): set Show Settings (trigger channel/button, audio filename, firmware version, deadman/disable/alternates), place events on the waveform, define disable groups and alternates.
2. **Export** script CSV → root of USB drive (one .csv only; `cobra.csv` on old firmware). Export MP3 (Audacity-formatted 320 kbps CBR 44.1 kHz stereo) → Audio Box USB.
3. **Load script:** USB into powered-off 18R2 → power on → LEDs circle → all green (success) or all red + error codes. Remove USB.
4. **Dry run** (mandatory): modules on first/last script channels, Audio Box on; arm, verify device count, press trigger on trigger channel; watch first/last cues fire and audio play cleanly end-to-end.
5. **Field setup:** wire igniters, chain slats, set channels/banks per plan; local TEST continuity at each module.
6. **Pre-show checks from the 18R2 (TEST mode):** device count; cycle all channels for continuity (fix red LEDs); SYNC for signal values; fresh batteries (new AAs in Audio Box).
7. **Arm:** module keys to ARM → press ARM on 18R2 → wait for solid ARM LED + correct count. Disarm until showtime if needed.
8. **Fire:** navigate to trigger channel, press trigger button (hold deadman if configured). Monitor countdown display; +/− to nudge timing vs audio; STEP to skip ahead; ARM to pause; TEST/DISARM to abort; alternate buttons for black-sky filler.
9. **Post-show:** disarm, keys to TEST, walk the line before touching product; clean and recharge/remove batteries for storage.

## 10. Notes / Unverified

- Firing-circuit electrical specs (output voltage/current per cue, capacitor-discharge details) are not published by COBRA; capacity is documented only as max-igniters-per-power-source (§7). For unusual igniters (>2 A) COBRA asks you to email resistance/current specs.
- "100 scripts / 1,000 events per script" limits come from the legacy (fw 2.x-era) Creating & Uploading Scripts PDF; current firmware documentation supersedes with 32 scripts (fw 7.1) and 3,600-event program limits. Both are cited in official docs; treat the newer numbers as authoritative for modern firmware.
- Audio Box drift-correction internals (whether it re-clocks continuously vs. start-trigger only) aren't documented; COBRA attributes sync problems to MP3 formatting and (Hardware A boxes) missing MESH peers.
- Show Creator pricing/tier details change frequently (subscription billing since 2023, Lite tier exists) — verify on cobrashowcreator.com.
- 18R2 4 MB flash figure is from COBRA's 18R2 product page marketing copy.

## Sources

- Script Format — https://help.cobrafiringsystems.com/hc/en-us/articles/5716119268251-Script-Format
- Scripting — https://help.cobrafiringsystems.com/hc/en-us/articles/5493854513947-Scripting
- What is Scripting? — https://help.cobrafiringsystems.com/hc/en-us/articles/5715836445211
- 18R2 Technical Specifications — https://help.cobrafiringsystems.com/hc/en-us/articles/5493033708571-18R2-Technical-Specifications
- 36M & 72M Technical Specifications — https://help.cobrafiringsystems.com/hc/en-us/articles/5538571372187
- 18M Technical Specifications — https://help.cobrafiringsystems.com/hc/en-us/articles/5511507833883
- 6M Technical Specifications — https://help.cobrafiringsystems.com/hc/en-us/articles/5628358301467
- Audio Box Technical Specifications — https://help.cobrafiringsystems.com/hc/en-us/articles/5632188057371
- Firing (manual/STEP/AUTO-FIRE) — https://help.cobrafiringsystems.com/hc/en-us/articles/5493742791451-Firing
- Re-Firing Cues and Pulse Times — https://help.cobrafiringsystems.com/hc/en-us/articles/5716435225115
- Re-fire limits per channel — https://help.cobrafiringsystems.com/hc/en-us/articles/40247695515675
- Max modules per 18R/18R2 — https://help.cobrafiringsystems.com/hc/en-us/articles/5495634921115
- Arming, Disarming and Module Count — https://help.cobrafiringsystems.com/hc/en-us/articles/5493649702427
- Checking Continuity — https://help.cobrafiringsystems.com/hc/en-us/articles/5493382603419
- Continuity Clarified — https://help.cobrafiringsystems.com/hc/en-us/articles/5734349740571
- Multiple Scripts, Clearing Scripts and Alternate Firing — https://help.cobrafiringsystems.com/hc/en-us/articles/5716431741723
- Alternate firing events — https://help.cobrafiringsystems.com/hc/en-us/articles/5718848437147
- Multiple scripts how-to — https://help.cobrafiringsystems.com/hc/en-us/articles/5717998278043
- Disable firing / groups — https://help.cobrafiringsystems.com/hc/en-us/articles/5718553965083
- Deadman Control — https://help.cobrafiringsystems.com/hc/en-us/articles/5778378563995
- What is a slat? — https://help.cobrafiringsystems.com/hc/en-us/articles/5645499780379 (also 37785652031387, 36085738567579)
- Banks on 36M/72M — https://help.cobrafiringsystems.com/hc/en-us/articles/5625402426139
- Igniter compatibility — https://help.cobrafiringsystems.com/hc/en-us/articles/36149175203227
- E-match vs Talon mode — https://help.cobrafiringsystems.com/hc/en-us/articles/5673676694171 (Talons per cue: 5673740682523)
- MESH — https://help.cobrafiringsystems.com/hc/en-us/articles/5733883457051; Range — 5733905482139
- Weather operation — https://help.cobrafiringsystems.com/hc/en-us/articles/5778279720347
- Audio Box Interface — https://help.cobrafiringsystems.com/hc/en-us/articles/5632150203675; Sync — 5632200196251; USB drives — 5644369850651; filename mismatch — 17425735767835; per-script MP3s — 5644530342683
- Creating/Formatting the MP3 — https://help.cobrafiringsystems.com/hc/en-us/articles/5643587743643; Testing MP3 — 5643665880603
- SMPTE: how it works — https://help.cobrafiringsystems.com/hc/en-us/articles/5648527836443; timecode1 vs 2 — 5649177503643; lost timecode — 5649006570651; need SMPTE? — 35606566751003
- Saving script to USB — https://help.cobrafiringsystems.com/hc/en-us/articles/5716332800539; Loading to 18R2 — 5716386341275
- What is COBRA Show Creator? — https://help.cobrafiringsystems.com/hc/en-us/articles/5669074781851; Show Settings — 8812200012059; Event/Sub-Event Time — 30640958610843; Export music — 8501140946971; Combined audio — 5672814361755
- Dry run — https://help.cobrafiringsystems.com/hc/en-us/articles/5718465263515 (checklist: 5735217557147)
- COBRA Getting Started Guide (PDF) — https://media.cobrafiringsystems.com/feedbucket/COBRA_Getting_Started.pdf
- COBRA 18R2 Creating and Uploading Automated Scripts (legacy PDF) — https://www.cobrafiringsystems.com/static/userguides/COBRA18R2CreatingandUploadingScripts.pdf
- 18R2 product page — https://www.cobrafiringsystems.com/18r2
- Finale 3D COBRA script format (third-party corroboration) — https://finale3d.com/documentation/cobra-script-file-format/
