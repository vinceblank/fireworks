# Consumer & Prosumer Fireworks Firing Systems — Generic Vocabulary, Survey, and Data Model

> Reference document compiled 2026-07-02 from vendor sites, Finale 3D documentation, and hobbyist community sources. COBRA has its own dedicated profile (`cobra-18r2.md`); it is referenced here only where it defines de-facto terminology.

---

## 1. Generic Concepts & Vocabulary

Every consumer/prosumer firing system, regardless of brand, decomposes into the same handful of roles. The names vary by vendor; this table normalizes them.

| Generic term | Also called (vendor-speak) | Definition |
|---|---|---|
| **Controller** | Remote, transmitter, command module, base station, handheld, "the app" | The device (or phone/tablet app) the operator holds. Sends fire commands to modules. May be a dedicated radio remote, a PC + base radio, or a smartphone over BLE/Wi-Fi. |
| **Firing module** | Receiver, field unit, base station, slat box, firing unit | The box positioned near the fireworks. Holds the terminals that deliver firing current to igniters. Systems scale by adding modules. |
| **Cue** | Pin, output, terminal, channel (consumer systems) | One electrical output on a module. Firing a cue sends current through whatever igniter(s) are wired to it. A cue can hold multiple igniters in series/parallel (pro modules fire 15+ e-matches per cue). |
| **Channel** | Zone, group, address | Ambiguous term — on cheap consumer systems "channel" = cue (a button on the remote). On pro-oriented systems "channel" is an *addressing layer*: modules are assigned a channel/zone number so one remote can address many modules independently (e.g. "fire channel 3, cue 12"). A generic model should treat "cue address" as the tuple *(module/channel, cue number)*. |
| **Slat** | Rail, breakout, pin board | A wired breakout strip (often 4–25 cues) that plugs into a module connector (e.g. DB25), letting cue terminals sit away from the module. Some systems address cues as module + slat + pin (e.g. PyroSure `10-A`). |
| **Igniter** | — | The consumable that converts current to fire. Three broad families (below). |
| **Continuity test** | Cue test, resistance check | Module measures whether an igniter circuit is intact before the show; indicated by LEDs or reported back to the controller. Present on mid-tier and up; often absent on cheap 433 MHz systems. |
| **Arm / Safe** | Arming key, arm switch | Hardware or software state that must be enabled before any cue can fire; the core safety interlock. |
| **Scripted firing** | Automated show, sequence, choreography, timed fire | Controller (or module itself) executes a pre-programmed list of `(time, cue address)` events. Scripts are authored in vendor apps or desktop tools (Finale 3D, FWsim, Show Creator) and exported in a vendor-specific format — usually CSV/tab-separated text. |
| **Manual firing** | Free-shoot, button fire | Operator presses a button per cue in real time. All systems support this; it is the *only* mode on entry-level systems. |
| **Sequential/step fire** | Interval fire, auto-step, rapid fire | Middle ground: pressing/holding one button steps through cues at a fixed interval. Common on consumer remotes. |
| **Semi-autonomous script** | Step-through script | Script defines the order/timing but operator confirms each step or can pause — a common prosumer safety pattern. |

### Igniter types

| Type | Regulation (US) | How it lights | Typical use |
|---|---|---|---|
| **E-match** (electric match) | Regulated; ATF license required | Pyrogen-tipped bridgewire, instantaneous | Professional 1.3G shows, tight pyromusical timing |
| **MJG Firewire Initiator** | Non-regulated e-match equivalent | Instantaneous; inserted directly into lift charge or e-match port | Consumer pyromusicals needing e-match-like timing without a license |
| **Talon / clip-on igniter** | Non-regulated | Clips onto visco (consumer) fuse; lights the fuse, so there is fuse-burn delay of several seconds | Backyard 1.4G shows where timing is loose |
| **Nichrome / bare-wire consumer igniters** | Non-regulated | Resistance wire wrapped to fuse; needs more current, slower | Cheap 433 MHz systems, DIY |

Practical modeling consequence: igniter type determines **pre-fire delay** (instant vs. fuse burn time), which any scripting/audio-sync layer must compensate for.

### Wireless vs wired

- **Cheap consumer**: one-way 433 MHz remote → receivers; no acknowledgment, no continuity feedback to the remote.
- **Prosumer**: two-way proprietary RF mesh (COBRA-style), long-range BLE 5.0 (Ignite), Wi-Fi (FireFly), or spread-spectrum radio with PC base station (Mongoose). Two-way links enable remote continuity reporting and synchronized clocks.
- **Wired/hybrid**: 2-wire bus networks (Firelinx "2Wire", FireTEK physical network) survive RF-hostile environments; several systems do both.

### Audio sync approaches (weakest → strongest)

1. **None** — operator fires manually while music plays.
2. **App-local playback** — phone/controller plays the track and runs the script off the same clock (Ignite, FireFly). Good enough for backyard shows.
3. **Pre-synchronized script + shared start** — script downloaded into modules; everything keyed to a common "GO" or GPS time.
4. **Timecode-driven** — controller chases **SMPTE LTC** or **FSK** timecode from the sound system (Firelinx, FireTEK, Mongoose, Pyrodigital); frame-accurate, the professional standard.

### Typical cue counts

- Per module: **2, 4, 6, 12, 18, 24, 36, 48** are the common sizes (4 and 12 dominate the cheap tier; 18/24/36/48 the prosumer tier).
- Per system: consumer BLE/Wi-Fi systems cap around **216–750+** cues; pro-grade radio/wired systems scale to thousands (Firelinx CM: 999 modules / ~60,000 timed cues; FireTEK master: 99 slaves / 6,336 channels).

---

## 2. System Survey (non-COBRA)

### Firelinx
- Architecture: **Command Module (CM)** controller + 24-cue **Firing Module (FM)**; also a palm-size 2-cue **Double-Shot** module. Wireless and "2Wire" wired operation.
- Scale: CM handles up to **999 modules / ~60,000 timed cues** (claimed ~407k e-matches).
- FM charges a super-capacitor bank on arm — can fire all 24 cues simultaneously.
- Scripting: yes — **CSV show files**; scripts auto-download into each FM and synchronize to ~1 ms. Finale 3D and FWsim Pro both export Firelinx format.
- Audio sync: manual, scripted, and **SMPTE timecode** firing.
- Marketed to both consumers and professionals.

### Ignite Firing Systems (i18 / i36)
- Architecture: smartphone/tablet app (iOS/Android) controls modules over **long-range BLE 5.0** (Fanstel amplified transceiver), 50–100 m+ range.
- Modules: **i18 (18 cues)** and **i36 (36 cues)**; mix up to **6 modules = 216 cues max** per app session. Cues use quick-plug connectors for Ignite clip-on igniters/MJG initiators.
- Modes: free-shoot manual, "select cue on all modules," and fully automated scripted shows.
- Scripting: yes — scripts built in the app or the web **designer.ignitefiringsystems.com**; Finale 3D exports a **tab-separated text / XLSX** row format (Event Time, Color, Cue, Firework Name, Duration, Igniter Pre-fire) pasted into the web designer.
- Audio sync: music-synced shows with playback on the phone via the app (script clock = phone audio clock). No SMPTE.

### Mongoose (SimpliFire)
- Architecture: Windows PC running **Display Director** software + USB **base radio** → any number of **48-cue field units** (2× DB25 connectors, 24 cues each, used with slats). Spread-spectrum RF chosen to avoid Wi-Fi congestion.
- Each cue can fire 15+ e-matches; onboard cue resistance/continuity checking.
- Scripting: yes — imports **Finale 3D, FireOne, PyroMate, StarFire** script files.
- Audio/timing: internal clock, music track, **FSK, SMPTE, and GPS** timing options — one of the broadest sync menus in the prosumer tier.
- Note: a "Wave/M series" product line could not be verified — SimpliFire documents the system as base radio + Mongoose Field Units. Treat "Wave/M series" as **unverified**.

### Bilusocn
- Architecture: classic budget tier — **433 MHz one-way remote (transmitter) + small receiver boxes**; e.g. the 12-cue kit = 1 remote + 3 receivers of 4 cues each. Product lines BL1200, BL12TC, BL08D, etc.
- Receivers are independent (one failing doesn't stop others) and re-pairable to any remote button via a learning-hole/paperclip procedure; system expands by buying more receivers.
- Firing modes: individual button fire and (on many models) sequential/salvo fire from the remote. **No scripting files, no PC/app integration, no audio sync.**
- Continuity: LED on receiver only; no feedback to remote.
- Igniters: typically bundled with generic consumer igniters (nichrome/clip style); fires talon-class igniters fine.

### ShowStarter — **unverified**
- Could not be confirmed as a distinct firing-system brand (results collide with a "Show Starter" 500 g cake and generic "Starter" wireless kits). If it exists, community references suggest a **generic 433 MHz remote/receiver system of the Bilusocn class** (per-button cues, learning-button pairing, no scripting/audio). Do not cite specs.

### AlphaFire (RFRemotech)
- Architecture: **distributed** system — instead of multi-cue boxes, each cue is its own tiny single-cue firing module paired to a multi-button remote (1Q, 4Q, 12Q kits; Pro and X series). 9th generation ("AlphaFire X") current; ~200,000 units sold (vendor claim).
- 12Q kit ships with an **Individual-Firing transmitter and an Interval-Firing transmitter**; modes: individual, interval sequential, and script firing on newer generations.
- "Full Current Output" module (RF1XG9) fires up to 15 standard igniters, and supports **nichrome wire / reusable igniters** — unusual at this tier.
- Learning button re-maps any module to any remote cue.
- Scripting/audio: basic on-remote sequencing; no desktop script file ecosystem or SMPTE. Range 100–2000 m depending on series.

### FireTEK
- Architecture: smart modules (e.g. **FTQ-16×64**) that act as standalone, **master** (up to 99 slave modules / 6,336 channels over the FireTEK wireless mesh), or slave; also physical 2-wire network. Controlled from **FTKontrol Android app** or dedicated controllers/MusicBox.
- Timing inputs: internal, **SMPTE LTC, FSK timecode, GPS**, external trigger. Some modules embed an audio player that can emit/chase timecode — single-module pyromusicals are possible.
- Scripting: yes — own scripting software plus **Finale 3D export (binary-ish fireTEK script file, machine-oriented, not human-editable)** and Pyro Ignition Control compatibility; wireless script upload and on-the-fly editing.
- Extras: DMX and audio control alongside pyro; USB-C charging, LiPo batteries.

### PyroSure
- Architecture: dedicated controller (v2 "Advanced Controller") + wireless **24-cue digital modules**; cues arranged as **6 slats × 4 connectors, addressed A1–F4** (two-part module/slat addresses like `10-A`).
- Firing power: capacitor bank per module, up to 80 A at 30 V — hundreds of igniters per cue (vendor claim).
- Timing resolution 0.01 s across modules.
- Scripting: yes — scripts designed on the controller screen and saved to its drive, or authored on PC (Finale 3D partner) and loaded **via USB stick together with the music**; the controller plays the music and fires the show (integrated audio sync rather than external timecode).

### Other widely used systems (brief)
- **FireFly / Titan-FireFly** — Wi-Fi app-controlled consumer system; **15-cue modules** using Titan Multiclip fuse clips, 50+ modules linkable (**750+ cues**); in-app show designer with **music sync from the phone's library**; ~500 ft range. No SMPTE, no desktop script format.
- **TNT Hot Shot** — mass-retail 6-cue Bluetooth module fired from a free phone app; entry-level, manual/app-button firing only.
- **Pyrodigital** — long-standing professional standard; **FSK timecode over audio** plus SMPTE; addressable modules; the origin of much timecode practice.
- **Galaxis (Germany) / EasyPyro (UK)** — established pro/prosumer wireless systems in Europe; module + handheld controller architecture with scripting; not surveyed in depth here.

---

## 3. Generic YAML Schema for Describing a Firing Setup

Design notes: the model separates **system capability** (what the make/model can do) from **inventory** (what the user owns) from **addressing** (how a cue is referenced). A universal cue address is the pair `(module_id, cue_number)`, with an optional `channel`/zone layer for systems that address modules by channel, and optional `slat` for slat-addressed systems (PyroSure, Mongoose).

```yaml
# Generic description of a user's fireworks firing system.
# The root equipment.yaml uses a pragmatic subset of this; use these fields
# when a setup needs them.

firing_system:
  make: "Ignite"                  # manufacturer/brand, e.g. COBRA, Firelinx, Bilusocn
  model: "i36"                    # model or series name
  tier: prosumer                  # consumer | prosumer | professional

  controller:
    type: app                     # app | dedicated_remote | pc_software | panel_controller
    platform: "iOS/Android"       # phone OS, remote model, or PC app name; null if N/A
    link: ble                     # ble | wifi | rf433 | proprietary_rf | wired_bus | usb
    range_m: 100                  # nominal max controller<->module range in meters
    two_way: true                 # false = fire-and-forget remotes (no ack/continuity)

  modules:                        # the firing modules/receivers the user owns
    count: 3                      # how many modules in this setup
    cues_per_module: 36           # cues (outputs) on each module
    max_modules_per_system: 6     # vendor limit for one controller session (null = unbounded)
    connector: quickplug          # quickplug | screw_terminal | db25_slat | clip_terminal
    continuity_test: true         # module can report igniter circuit integrity
    slats:                        # OPTIONAL — only for slat-addressed systems
      per_module: 0               #   e.g. PyroSure: 6 (A-F), Mongoose: 2 (DB25)
      cues_per_slat: 0

  channel_scheme:                 # how a cue is addressed system-wide
    style: module_cue             # module_cue      -> (module #, cue #)   e.g. Ignite, Firelinx
                                  # flat_channel    -> remote button N = receiver N (Bilusocn-class)
                                  # module_slat_pin -> (module, slat, pin) e.g. PyroSure 10-A-3
    modules_addressable: true     # can one controller target modules independently?
    notes: "App addresses modules 0-5; cues 1-36 within each."

  scripting:
    supported: true               # can the system run a pre-programmed timed show?
    modes: [manual, sequential, scripted]   # subset of: manual | sequential | semi_auto | scripted
    script_format: "tab-separated text (Finale 3D IGNITE export) pasted into web designer"
                                  # e.g. "CSV (.csv)", "fireTEK binary script", null if none
    authoring_tools: ["IGNITE app", "designer.ignitefiringsystems.com", "Finale 3D"]
    script_storage: controller    # controller | module | both  (where the script executes from)

  audio_sync:
    supported: true
    method: app_playback          # none | app_playback | integrated_player | smpte | fsk | gps_clock
    timecode_chase: false         # true if it can follow external SMPTE/FSK from a sound board
    notes: "Show clock locked to phone audio playback in the IGNITE app."

  igniters:
    types_supported: [talon_clip, mjg_initiator, ematch]
                                  # subset of: ematch | mjg_initiator | talon_clip | nichrome
    type_in_use: talon_clip       # what this user actually wires
    per_cue_capacity: 3           # max igniters reliably fired on one cue (vendor spec)
    prefire_delay_s: 4.5          # ignition-to-effect delay to compensate in scripts
                                  #   (~0 for e-match/MJG; fuse burn time for clip-ons)

  power:
    module_battery: "internal Li-ion, USB-C"   # free text
    field_rechargeable: true
```

### Minimal example for a budget system (contrast)

```yaml
firing_system:
  make: "Bilusocn"
  model: "BL1200 12-cue kit"
  tier: consumer
  controller: { type: dedicated_remote, platform: null, link: rf433, range_m: 500, two_way: false }
  modules:
    count: 3
    cues_per_module: 4            # kit = 3 receivers x 4 cues
    max_modules_per_system: null  # expandable by pairing more receivers
    connector: clip_terminal
    continuity_test: false        # LED on receiver only; nothing reported to remote
  channel_scheme: { style: flat_channel, modules_addressable: false,
                    notes: "Remote button N fires whichever receiver learned button N." }
  scripting: { supported: false, modes: [manual, sequential], script_format: null,
               authoring_tools: [], script_storage: null }
  audio_sync: { supported: false, method: none, timecode_chase: false }
  igniters: { types_supported: [nichrome, talon_clip], type_in_use: talon_clip,
              per_cue_capacity: 2, prefire_delay_s: 5.0 }
  power: { module_battery: "AA / 9V", field_rechargeable: false }
```

---

## Unverified / caveats

- **ShowStarter**: could not verify as a distinct firing-system brand; likely a generic 433 MHz remote/receiver kit. All ShowStarter details omitted.
- **Mongoose "Wave/M series"**: no such product line found on SimpliFire's site; only base radio + 48-cue Field Units are documented.
- **FireTEK "Xplode app"**: FireTEK's app is FTKontrol; "Xplode" appears to be a separate (Australian) firing system brand, not researched here.
- Vendor scale claims (Firelinx 999 modules/60k cues, PyroSure 80 A/hundreds of igniters per cue, AlphaFire 200k units sold) are marketing figures, not independently verified.
- Bilusocn igniter bundling details and FireFly per-cue capacity are inferred from retail listings, not formal spec sheets.

## Sources

- COBRA product overview (terminology baseline): https://www.cobrafiringsystems.com/product_overview.html
- COBRA help — Talon vs MJG vs e-match: https://help.cobrafiringsystems.com/hc/en-us/articles/5673695569179-Which-is-better-Talon-Clip-on-Igniter-clips-or-MJG-initiators
- UKFR — Lighting Fireworks Remotely (consumer system landscape): https://www.ukfr.com/lighting-fireworks-remotely
- Skylighter — Wiring firing systems (series/parallel, igniter basics): https://www.skylighter.com/blogs/fireworks-information/wiring-firing-systems
- Ignite — How it works: https://www.ignitefiringsystems.com/howitworks | i18: https://www.ignitefiringsystems.com/i18 | i36: https://www.ignitefiringsystems.com/i36 | Integrations: https://www.ignitefiringsystems.com/integrations
- Finale 3D — IGNITE export format: https://finale3d.com/documentation/ignite/
- Firelinx — Features: https://www.firelinx.com/features/ | Command Module: https://www.firelinx.com/product/command-module/ | Firing Module: https://www.firelinx.com/product/firing-module/ | Double-Shot: https://www.firelinx.com/product/double-shot/ | FAQs: https://www.firelinx.com/support/faqs/
- Finale 3D — Firelinx: https://finale3d.com/documentation/firelinx/ | FWsim Firelinx export: https://www.fwsim.com/doc/data_export_firelinx.html
- SimpliFire Mongoose — System overview: https://www.simplifirepyro.com/system-overview | How it works: https://www.simplifirepyro.com/how-mongoose-works | Field Unit: https://www.simplifirepyro.com/product-page/mongoose-field-unit
- Finale 3D — Mongoose: https://finale3d.com/partners/mongoose/
- Bilusocn — 12-cue kit: https://www.bilusocn.com/3-pcs-12-Cue-Wireless-Fireworks-Firing-system-equipment-Remote-control-p2564329.html | Home: https://www.bilusocn.com/
- RFRemotech AlphaFire — Series: https://www.rfremotech.com/AlphaFire2BSeries.html | X series: https://www.rfremotech.com/AlphaFireX/ | 12QS: https://www.rfremotech.com/AlphaFire2B12QS.html
- FireTEK — Modules: https://firetekfiringsystem.com/modules/ | Controllers/MusicBox: https://firetekfiringsystem.com/controllers-musicbox/ | FTQ-99Sx: https://firetekfiringsystem.com/ftq-99sx-with-wireless-audio-and-time-code/
- Finale 3D — fireTEK script format: https://finale3d.com/documentation/firetek-script-file-format/
- PyroSure — System overview: https://pyrosure.com/system-overview/ | Firing modules: https://pyrosure.com/firing-modules/ | Controller: https://pyrosure.com/controller/
- Finale 3D — PyroSure: https://finale3d.com/partners/pyrosure/ | Supported firing systems: https://finale3d.com/supported-firing-systems/
- FireFly — How it works: https://shootfirefly.com/pages/how-it-works | FAQ: https://shootfirefly.com/pages/faq
- TNT Hot Shot: https://www.tntfireworks.com/fireworks/cat/firing-systems/3807-hot-shot-6-cue-firing-system
- Pyrodigital (FSK/SMPTE background): https://pyroinnovations.com/fireworkstraining_pyrodigital_advanced.html
- COBRA SMPTE background: https://www.cobrafiringsystems.com/smpte
- Talon igniters (retail spec): https://backyard-pyro.com/product/1m-talon-igniter-quick-connect-25-pack/
- MJG Technologies: https://electricmatch.com/pyrotechnics
