# <Make> <Model> — Device Profile

<!-- status: verified | unverified (user-reported, research pending) -->

## Overview
One paragraph: what the system is, who makes it, what class of shows it suits.

## Architecture
- Controller/remote: model, display, power
- Firing modules (base stations/receivers): model(s), cues per module, power
- Connection: wireless protocol/frequency, range, wired options
- Max modules per show / per channel

## Channels & cues
- Channel scheme (range, how modules are assigned a channel)
- Cues per module; how cue numbers map to physical terminals
- Can multiple modules share one channel (mirrored firing)?

## Firing modes
- Manual / sequential-step / scripted — how each works on this hardware

## Scripting & audio sync
- Show-file format the controller imports (**exact** file type, header rows,
  columns, time format — this section is what /export-show consumes)
- How scripts get onto the controller (USB, app, SD)
- Audio sync mechanism (audio box, app playback, manual clock)

## Igniters & wiring
- Compatible igniter types, firing current, series/parallel limits

## Operating workflow
- Continuity test → arm → fire procedure; deadman/safety features

## Limits & gotchas
- Anything that bites: timing resolution, min delay between cues, import quirks

## Sources
- URLs (manufacturer manual/support first)
