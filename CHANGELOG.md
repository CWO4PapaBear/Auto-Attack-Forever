## Pending client indicator retest

- Clear inherited native ranged-combat flags on control spell 970100.
- Show Auto Ranged as active only for actual shot, thrown or wand repeats; preserve stock melee indicator.
- Lua indicator/options checks pass; local client installed, gameplay retest pending. Launcher release remains separate.

## 0.2.3-preview - neutral control and feral melee

- Stop treating the client dispatch control as an actual ranged repeat: clear ranged-slot/autorepeat flags and use a dummy effect. Actual server shots retain native checks and Auto Shot identity.
- Do not force humanoid melee weapon stance in feral forms. Compiled controller/hook tests passed; full build and gameplay retest pending. Both root and locale client archives staged; not installed yet.

## Control spell form and duplicate-archive correction

- Remove the inherited not-shapeshifted flag from control spell 970100, preserving restrictions on native ranged shots.
- Repair both root and locale client patch copies; the root copy still contained the old equipment restriction. Verified that only control flags changed and unrelated archive entries were preserved. Installed locally with backups; gameplay retest pending.

## Minimap settings shortcut

- Add the existing AAF logo as a custom 64x64 RGBA TGA minimap icon. Click opens the existing Interface options; drag position is saved per character.
- Installed locally with backups; Lua 5.1 syntax passed. Visual verification pending.
- Ranged-options server build and activation confirmed; gameplay tests in progress. Launcher publication pending.

## 0.2.2-preview - ranged preference

- Add per-character ranged toggle, silent right-click melee fallback and generic Auto Ranged weapon notice.
- Controller/hook compiled tests and Lua 5.1 options tests passed. Full PTR build and gameplay validation pending. No launcher release yet.

# Changelog

## Unreleased — spell opener fix

- Route authorized native Auto Shot requests into the adaptive controller.
- Preserve running repeats and transition timers on duplicate start requests.
- Recheck world/vehicle/possession state after movement flags.
- Compiled controller and packet regression tests pass; PTR compile passed with source restored; activation and gameplay verification pending.
- No client or database update required.

## 0.2.0-preview

- Replace all core integration edits with existing ServerScript and UnitScript hooks.
- Preserve native Auto Shot dispatch, all five weapon types and automatic melee/ranged switching.
- Retain stock wand startup timing and normal equipment restrictions.
- Build and gameplay validated on unmodified stock AzerothCore.
- Replace patch installer with a read-only preflight; document migration from older patched versions.
- Existing spell IDs, SQL and client patches remain compatible.
- Record successful Wild Quiver testing on the preceding native-shot implementation.


## 0.1.2-preview

- Dispatch native Auto Shot (75) for bows, guns and crossbows on every class. The universal control is sufficient; native Auto Shot need not be learned separately.
- Preserve ordinary native Auto Shot when the controller is not managing it, including while the module is disabled.
- Remove the artificial 500 ms first-repeat floor only for custom wand spell 970102. Preserve remaining cooldowns and normal shot intervals.
- Keep native spell records, weapon restrictions, talents and passive grants unchanged. No new Hunter haste bonus is granted.
- Recorded 67 Hunter shots and 38 Warrior shot attempts using spell 75. The Warrior had not learned Auto Shot. Wild Quiver was not learned on either test character and remains unverified.
- User confirmed snappier wand startup. Latest changes were built on the modified playerbots core; a new full stock-core build remains pending.

## 0.1.1-preview

- Replaced inherited Auto Shot tooltip text with a description of automatic ranged/melee switching. Auto Ranged no longer claims a Hunter attack-speed bonus.
- Gave the hidden thrown and wand implementation spells their own descriptions.
- Verified that generated patches change only the custom spell descriptions; gameplay values and other spell text remain unchanged.
- This is a client-builder correction. Server code and SQL are unchanged from 0.1.0-preview, so the server startup message still identifies that controller version.
- Existing installations should restore their pre-installation client archives before regenerating patches; the builder intentionally refuses already-installed custom spell IDs. Back up current archives and follow the installation guide rather than overwriting unrelated patches.

## 0.1.0-preview

- Packaged the tested automatic ranged/melee controller as Adaptive Auto Attack.
- Included required core integration and weapon-based wand school selection.
- Included a local client builder with the final thrown-repeat corrections.
- Preserved all equipment class and proficiency restrictions; every character receives the unified controls.
- Added an enable setting, logout cleanup and optional Blizzard action-bar icons.
- Added guarded installation documentation, rollback guidance and release validation checklist.

Stock-core build, activation and user-reported ordinary-class combat validation subsequently passed on September 14, 2026. Extended checks remain listed in docs/VALIDATION.md.
