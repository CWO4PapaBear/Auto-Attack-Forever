# Installation walkthrough (preview)

This package is source code, an integration patch, a client-patch generator and an optional addon. It requires your own AzerothCore checkout, build dependencies, database service and WoW 3.3.5a client (build 12340). It does not include the game, databases, compiler or credentials. Python 3.10+ and Git are required for the helper scripts.

The packaged preview has passed its build, activation and user-reported ordinary-class gameplay tests on the supported stock revision. Extended compatibility and recovery testing remains open. Test it separately before using it on a public realm. Docker installations must rebuild their actual worldserver image; the native build commands below do not rebuild Docker images.

## 1. Back up and identify your installation

Save your current core revision, local source changes, server configuration, world and character database backups, running server binaries/images, and both client Z archives. Keep a record if either archive did not previously exist. Confirm you can restore these backups. Database backup commands depend on your installation and credentials; never put passwords in this repository.

Supported core: `e1823bb2db751a7cc0a90a8543e778449ebf7d84`. Other revisions need a separate compatibility review. Do not reset an existing checkout to this revision and lose local work.

## 2. Place the module and check the core

Extract the repository as `modules/mod-adaptive-autoattack` inside the core checkout. Do not nest an extra directory. Run from the core root:

```bash
python3 modules/mod-adaptive-autoattack/tools/prepare_server.py --core .
```

A failed check stops without editing core files. Resolve the reported conflict; do not force it. The helper intentionally refuses an already modified or patched core.

## 3. Check the database IDs

Run these in your world database. Both results must be empty:

```sql
SELECT Id FROM spell_dbc WHERE Id BETWEEN 970100 AND 970102;
SELECT ID, Spell FROM skilllineability_dbc
WHERE ID BETWEEN 970100 AND 970102 OR Spell BETWEEN 970100 AND 970102;
```

## 4. Apply the integration patch

```bash
python3 modules/mod-adaptive-autoattack/tools/prepare_server.py --core . --apply
```

Keep the module and core patch together. Removing only the module causes unresolved core references.

## 5. Build and configure

For a native installation, reconfigure your existing build directory with its original installation prefix and other settings, enabling static modules. Example from the core root; replace the build directory if yours differs:

```bash
cmake -S . -B build -DMODULES=static
```

```bash
cmake --build build --parallel 2
```

Only after a successful build, stop the worldserver and install using your normal deployment procedure. For a native CMake installation:

```bash
cmake --install build
```

Copy `conf/adaptive_autoattack.conf.dist` to the installed server's `etc/modules/adaptive_autoattack.conf`. Set `AdaptiveAutoAttack.Enable = 1`. Apply `data/sql/db-world/2026_09_14_00_adaptive_autoattack.sql` through your normal module database updater. Do not both import it manually and let the updater apply it again. Backups and collision checks must precede the database update.

## 6. Generate client patches

From the module directory, run the following on the machine with the client. Replace paths with yours; choose a new output directory outside the client. On Windows, use `python` rather than `python3` if appropriate.

```bash
python3 tools/build_client.py --client "/path/to/WoW-3.3.5a" --output "/path/to/new-client-patch" --locale enUS
```

The generator reads your own game data and verifies both output archives. It preserves unrelated files in existing Z archives and refuses reserved-ID collisions. It does not modify your client. Only enUS has been tested.

Close WoW completely. Back up existing `Data/patch-Z.MPQ` and `Data/enUS/patch-enUS-Z.MPQ`, then copy both generated files to those locations. Install `client-addon/AdaptiveAutoAttack` under `Interface/AddOns`. Do not overwrite a different client by mistake.

## 7. Start and validate

Start the updated worldserver, review its startup log, fully reopen WoW and enable the addon. Log in with an ordinary class. Confirm Auto Melee and Auto Ranged appear in General. Test only weapons the character can normally equip: right-click at range, repeated shots, approach melee, retreat to range, stop attacking, change targets, and logout. Include bow/gun, thrown and wand tests using eligible characters. Confirm ineligible weapons remain ineligible and no weapon skills were granted. See VALIDATION.md for remaining checks.

Missing client data usually means the wrong client was patched or base and locale archives differ. Link errors referencing RangedAuto functions mean the module and core patch are not installed/built together. Database duplicate errors require inspection, not INSERT IGNORE or replacement.

## Rollback

Stop the worldserver. Restore the prior core/module binaries or image, source/configuration and database backups as a matched set. With WoW closed, restore both previous Z archives (remove only newly installed archives that had no predecessor) and the prior addon state. Restart and verify. Reversing the source patch alone does not roll back installed binaries, learned spells or database updates.

The helpers do not guess Docker service names, sudo privileges, database credentials or restart commands. A fully verified Docker deployment recipe is still pending.
