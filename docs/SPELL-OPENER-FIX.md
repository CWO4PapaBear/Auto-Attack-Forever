# Spell opener fix — staged PTR build

The controller previously recognized only custom control 970100. Client-generated native Auto Shot (75) requests bypassed it; the stock handler rejects 75 when only the universal control is learned. Repeated managed start requests also interrupted the current repeat and reset its transition window.

The patch routes 75 through the controller only when the player has active control 970100. Native behavior remains when the module is disabled or the control is absent. Requests for the same live victim preserve the running attack and pending transition. Explicit stop/cancel paths are unchanged. Ordinary spell casts still pass to the core. Movement processing is followed by world/vehicle/possession checks.

Compiled stub tests pass for both modified C++ files. Both regressions fail against the pre-patch code. Tests cover spell-opening cast waits, repeated requests, all five weapon categories, melee transitions, explicit stops, authorization, module disablement, queued cancel and world changes. Full PTR compile and in-game reproduction remain pending. The exact reported opening spell/weapon has not yet been supplied; this fixes two confirmed paths without claiming a live reproduction.

## Build

Run in WSL:

```bash
sudo python3 /mnt/c/Users/danie/Documents/Codex/2026-09-12/can/outputs/Auto_Attack_Spell_Opener/Build-Test.py
```

Build only. The script uses the current PTR compose/image configuration, verifies the two module files against the read-only export, backs up source, stages only those files, builds a new tagged image, and restores original source. No server restart, database writes or client installation. Activation follows review of build-state.json and build.log.

## In-game checks after activation

- Open with the reported ranged spell, then confirm ranged shots continue after the cast.
- Cast another ranged spell during auto attack; confirm no repeated restart or stall.
- Move into melee and back out; confirm switching resumes.
- Stop attacks explicitly; confirm they stay stopped.
- Check bows, guns, crossbows, thrown weapons and wands; retain ammo, range and movement restrictions.

No SQL, DBC, MPQ, client addon or launcher changes. Bear Cave Main is not activated by this package. This work belongs solely to Auto-Attack-Forever.
