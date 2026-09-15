# Release validation

## 0.1.2 native dispatch and wand update

- Built and activated on modified AzerothCore/playerbots revision `efe123fab543c5faf3c477674ec17a18fd59f09f` with the server's existing modules retained. This required an adapted core patch; the public full patch still targets the stock revision below.
- Combat trace recorded 67 Hunter shots and 38 Warrior shot attempts (36 hits, 2 misses), all using native spell 75. The Warrior's client reported Auto Shot unlearned while Auto Ranged was learned.
- Neither character had Wild Quiver learned. Its proc behavior, Hunter Tier 10 interactions and complete Hunter talent compatibility remain untested.
- The separate Hunter passive 34082 applies ranged haste through the core's attack timer. No new passive grant was introduced. Client traces cannot reliably observe hidden passive auras; the 15% magnitude was not independently measured in a controlled comparison.
- The Hunter mostly killed each target with one shot; characters had different weapons, leveled, and received equipment buffs. These recordings are not controlled attack-speed benchmarks.
- User confirmed noticeably snappier wand startup after removing only the custom wand's artificial startup floor.
- Local controller tests cover bow/gun/crossbow dispatch without learned spell 75, thrown/wand handlers, melee transitions, cancellations, and preserving unmanaged native Auto Shot. Full stock-core rebuild of 0.1.2 remains pending.

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
