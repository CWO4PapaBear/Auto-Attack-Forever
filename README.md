[![Auto-Attack Forever — watch the showcase](docs/assets/showcase-thumbnail.jpg)](https://youtu.be/Dh1eWCPZBXg)

# Auto-Attack Forever

Created by [CWO4PapaBear](https://github.com/CWO4PapaBear). Third-party contributions are credited in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

Your most basic attacks should be the easiest part of combat. Switching between shooting and swinging is a small, familiar frustration—easy to overlook, but repeated across countless encounters. **Auto-Attack Forever** smooths out that friction, letting your equipped weapons handle the basics while you focus on the abilities, timing, and big plays that make your character fun to play.

Close the distance. Take the shot. Save your attention for the moves that matter.

For hunter-style characters in Free Pick or Wildcard systems, universal ranged attacks can also leave more room for specialization. When Auto Shot would otherwise consume an ability selection, making basic ranged attacks available to everyone lets that selection go toward another skill that defines the build. Spend it on becoming a better marksman, a stronger beast master, or something entirely your own.

This module supplies the basic attack controls; it does not itself refund ability selections or change a Free Pick/Wildcard system's ability pool. That system must treat the supplied attack as free to realize this benefit. Ordinary hunters keep their existing abilities, and all classes retain their normal weapon restrictions.

**0.1.2 preview — native Auto Shot dispatch and faster wand startup. The previous release passed stock-core testing; these updates were built and tested on a modified AzerothCore server. Wild Quiver and extended compatibility testing remain open.**

Auto Ranged dispatches native Auto Shot (spell 75) for bows, guns and crossbows, regardless of class, without teaching or requiring a separate Auto Shot ability. This preserves the native shot identity used by Hunter talent and proc rules. It does not grant Hunter talents or the Hunter's separate 15% haste passive. Wild Quiver recognition is supported by the spell identity, but its actual proc behavior has not yet been verified in game. Thrown weapons and wands retain their custom handlers. Custom wand attacks skip the core's artificial 500 ms startup floor without resetting remaining attack cooldowns or changing normal firing intervals.

Upgrading from 0.1.0/0.1.1? Read [the upgrade instructions](docs/UPGRADE-0.1.2.md) before changing the patched core.

Right-click an enemy to use the equipped ranged weapon outside melee reach and melee attacks at close range. If the target moves back into valid ranged distance, ranged attacks resume. The General spellbook contains **Auto Melee** and **Auto Ranged**; the optional addon changes Auto Ranged's icon to the equipped ranged weapon on Blizzard action bars.

Supports bows, guns, crossbows, thrown weapons and wands. Existing proficiency, ammunition, durability, range, facing, line-of-sight and movement checks still apply. Every character receives the attack controls, regardless of class or weapon proficiency. The module does not teach weapon skills, remove item class restrictions, or make a weapon equippable by an otherwise ineligible character.

## Demonstration

[Watch the showcase on YouTube](https://youtu.be/Dh1eWCPZBXg). The downloadable package also includes the original final-test MP4.

Recorded by the project owner during the successful final test on the Classless test server. This recording demonstrates the working predecessor. The packaged preview subsequently passed its stock-core build, activation and ordinary-class gameplay tests on September 14, 2026. The video is provided as a separate media asset, not under the source-code license.

Click the header thumbnail to watch the showcase.

The display name is **Auto-Attack Forever**. Installation folder and configuration identifiers remain `mod-adaptive-autoattack` and `AdaptiveAutoAttack.Enable` in this preview.

## Components

- `src/`: independent server module, no Classless Wildcard dependency.
- `patches/`: required core integration patch, including wand damage-school handling.
- `data/sql/db-world/`: three custom spell records and General-tab mappings.
- `tools/build_client.py`: generates client patches from your own 3.3.5a client; preserves unrelated entries in existing Z archives.
- `client-addon/AdaptiveAutoAttack/`: optional dynamic action-bar icon addon.
- `conf/`: enable/disable setting.

This is **not a drop-in module alone**. The core patch and matching client patches are required. No Blizzard client assets, account data, databases, executable files or server credentials are included.

## Installation

Start with the [step-by-step walkthrough](docs/INSTALL.md). `tools/prepare_server.py` checks the supported core before applying anything.


Use an isolated test server and back up its source, configuration, world/character databases and client patches. The core patch targets revision `e1823bb2db751a7cc0a90a8543e778449ebf7d84`; other revisions require review. The old experimental `mod-ranged-autoattack` must not be installed alongside this module: the IDs and integration symbols overlap.

1. Put this repository at `modules/mod-adaptive-autoattack` in the AzerothCore checkout. The repository is named Auto-Attack-Forever; the installation directory must use the module loader name shown here. From your core root:

```bash
git clone https://github.com/CWO4PapaBear/Auto-Attack-Forever.git modules/mod-adaptive-autoattack
```
2. From the core root, check and apply the patch:

```bash
git apply --check modules/mod-adaptive-autoattack/patches/azerothcore-e1823bb.patch
git apply modules/mod-adaptive-autoattack/patches/azerothcore-e1823bb.patch
```

3. Verify that IDs 970100–970102 are unused in **both** `spell_dbc` and `skilllineability_dbc`, and absent from your client DBCs. The SQL uses plain INSERT intentionally; resolve collisions rather than replacing unrelated data.

```sql
SELECT Id FROM spell_dbc WHERE Id BETWEEN 970100 AND 970102;
SELECT ID, Spell FROM skilllineability_dbc WHERE ID BETWEEN 970100 AND 970102 OR Spell BETWEEN 970100 AND 970102;
```

4. Build AzerothCore with static modules enabled. Apply the included world SQL through the normal module database updater. Copy `conf/adaptive_autoattack.conf.dist` to the server's module configuration directory as `adaptive_autoattack.conf`. Restart the worldserver after the build and database update.
5. Build the client patches with Python 3.10 or newer, using paths for your machine:

```bash
python tools/build_client.py --client "/path/to/WoW-3.3.5a" --output "/path/to/new-build-client" --locale enUS
```

The builder only writes to the output directory. It fails on reserved-ID collisions, including an already-installed version. It does not automatically upgrade custom installations. Output contains complete replacement Z archives, including preserved unrelated entries from your own existing Z archives. Keep both base and locale copies synchronized.

6. Close WoW. Back up existing `Data/patch-Z.MPQ` and the corresponding locale Z archive. Copy the generated `Data` contents into the client. Copy `client-addon/AdaptiveAutoAttack` into `Interface/AddOns` and enable it. Fully reopen WoW and relog the character.

## Verification and limits

The working predecessor was tested in game on a Classless Wildcard test server. Ranged repetition, animations, melee transitions, returning to ranged distance, wand startup and thrown repetition were confirmed by the tester. The packaged module subsequently compiled and linked on stock AzerothCore, activated with all ten normal classes retained, and passed the requested ordinary-class gameplay checks as reported by the tester on September 14, 2026. Configuration toggling and the extended edge-case checklist remain separate follow-up checks. See [validation](docs/VALIDATION.md).

There is a short transition window to distinguish a client response to a server-requested mode change from a stop request. High-latency and packet-loss testing is outstanding. Do not advertise competitive-PvP readiness yet.

Native spell IDs are preserved, including existing Shoot, Throw and wand abilities. The two custom implementation spells are hidden in the client. Action-bar replacement addons and non-enUS labels have not been tested. Built-in melee activation and right-click share a core attack command; a separate manual melee-only override is not implemented.

## Disable or uninstall

Set `AdaptiveAutoAttack.Enable = 0` and restart to stop automatic dispatch and new grants. This retains learned spells and client labels. For a complete rollback, stop the server, restore the prior core/module build and database backups, restore both prior client archives and remove the addon. Remove the required core patch together with the module; otherwise the core will reference missing module symbols. Do not remove only the module from a patched core.

## License

GPL-2.0-or-later. Bundled client archive utilities are adapted from `mod-classless-wildcard`; see [third-party notices](THIRD_PARTY_NOTICES.md). Generated client patches are for your own installation and are intentionally excluded from this source repository.
