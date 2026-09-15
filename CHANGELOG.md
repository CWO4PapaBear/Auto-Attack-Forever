# Changelog

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
