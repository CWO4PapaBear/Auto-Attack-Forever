# Release validation

## Already observed on the predecessor

- Bow/gun/wand/thrown repeat behavior, ranged animation and melee handoff tested in game.
- Returning to range resumes firing.
- Wand startup improved after reducing the transition delay.
- Thrown repetition corrected by clearing both native client-side melee-initiation flags.

## Stock-server validation — September 14, 2026

- Compiled and linked the packaged module against stock core `e1823bb2db751a7cc0a90a8543e778449ebf7d84`, with no Classless Wildcard module.
- Verified activation, all three attack spell records, ten ordinary classes and matching base/locale client patches generated from a separate clean baseline copy.
- Tester reported “All tests good” after the requested ordinary-class test sequence, including bow, gun, crossbow, thrown and wand coverage, ranged/melee transitions, stop/target/relog checks and normal proficiency restrictions. This is user-reported gameplay validation, not an automated packet trace or a per-character test log.
- Corrected the compatibility manifest's Unit.cpp comment-encoding mismatch. The test restore's configuration ownership issue was corrected before successful activation.

## Extended checks still open before a stable public release
- Verify configuration off/on and logout cleanup.
- Verify `/stopattack` controls, Escape, ranged-button cancellation, death, target changes, movement, weapon swaps, broken weapons and exhausted ammunition.
- Test high latency, packet loss, rapid close-range boundary crossings and large hitboxes.
- Verify wand damage school against resistances and thrown durability consumption.
- Check the dynamic icon with default action bars. Third-party action bars require separate compatibility work.
- Test the complete uninstall/restore sequence on disposable data.

Local stubbed-core tests validate controller branches, not network protocol or live animation behavior. Local patch-builder tests verify record integrity, unrelated archive preservation and collision refusal; they do not prove runtime compatibility on every 3.3.5a client.
