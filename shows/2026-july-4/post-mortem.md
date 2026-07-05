# 2026 Show — Post-Mortem (show fired 2026-07-04)

## What happened

~40% of cues did NOT fire, scattered across BOTH stations. All cues tested
green continuity before arming. Music, sync (3-press STEP ritual), and the
script itself ran correctly.

## Diagnosis

- Ruled out by owner inspection: igniter-type/pulse mismatch (mode was
  correct for the igniters used) and igniter-to-fuse attachment (failed
  igniters were intact, not popped-without-lighting).
- **Prime suspect: battery sag under firing load.** Continuity testing draws
  milliamps; firing draws amps. Weak module batteries pass every pre-show
  test and then deliver pulses too weak at show pace.
- Confirmation tests (see repo history for full procedure): (1) failure
  pattern vs time (sag worsens late + on multi-fires; contiguous blocks =
  brownout/self-disarm instead), (2) per-battery voltage UNDER LOAD
  (<~7 V loaded = dead even if idle looks fine), (3) re-fire recovered
  igniters individually then at show pace on the show-night batteries,
  (4) control run on fresh power.
- RESULT: _fill in after tests_.

## Why our validation missed it

The no-wires bench dry-run passed 100% — empty terminals draw no current,
so it validates logic/comms/timing but can NEVER catch a power-delivery
problem. Continuity green ≠ firing energy available.

## 2027 prevention (now in the field-setup skill)

1. FRESH batteries (or the COBRA 14.8 V LiPo / 12 V external) installed in
   every module ON show day — never holdovers.
2. Under-load voltage check in the arming checklist.
3. Live-fire a few SACRIFICIAL igniters at show pace (rapid sequence + one
   simultaneous pair) on the actual show batteries during setup-day testing.
