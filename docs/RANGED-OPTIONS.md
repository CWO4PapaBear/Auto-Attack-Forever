# Ranged preference and melee fallback (0.2.2)

Status: compiled controller/packet-hook tests and Lua 5.1 panel tests passed. Full PTR build, client installation and activation confirmed. Gameplay verification pending.

Right-clicking a distant enemy without a usable ranged weapon starts melee silently. This does not move the character or permit melee damage at range. Explicit Auto Ranged requests without a weapon give `Equip a ranged weapon to use Auto Ranged.` only when the character has ranged proficiency; otherwise they silently start melee. Capability uses learned skills, not original class, so Hybrid characters are supported.

Client control spell 970100 must have EquippedItemClass=-1, EquippedItemSubclass=0 and EquippedItemInvTypes=0. Otherwise client validation can reject the request before server fallback. Native Auto Shot 75 and actual thrown/wand attacks retain equipment checks. The builder applies this for new installations. For customized clients, patch only those three fields in the effective Spell.dbc and preserve every other archive entry. No world SQL migration is needed: the packet hook intercepts authorized control requests before normal spell validation.

Open Interface > AddOns > Auto-Attack Forever, or `/aaf`. Disable **Enable automatic ranged attacks** to keep current and future managed attacks in melee mode. This prevents automatic ranged switching when a target moves away from a shapeshifted character. Manually cast spells retain normal behavior.

Commands: `.aaf ranged status`, `.aaf ranged on`, `.aaf ranged off`. Server PlayerSettings source `auto_attack_forever`, index 0, stores 1 for disabled and 0/unset for enabled. PlayerSettings persistence must be enabled. Normal character saves/logout persist changes; no new schema. The UI waits for server confirmation and reports a timeout rather than assuming success.

Before release, test silent distant right-click and explicit requests on characters without ranged proficiency; generic notices for capable characters lacking weapons; disabling during a ranged repeat; remaining shapeshifted as a target leaves melee; re-enabling all five weapon types and spell openers; and per-character persistence after logout. Local mocks do not replace these checks.

Publish source to `main`. Client assets and launcher promotion are separate. Retain the old server image and backed-up client files for rollback.

## Client correction after initial testing

Spell 970100 also needs its Attributes NOT_SHAPESHIFTED bit (0x10000) cleared: it is a dispatch control that may select melee in form. Native Auto Shot and actual ranged attacks keep their restrictions. Inspect both root and locale patch copies rather than assuming one archive wins; the first installation left the root copy with an old weapon requirement. Both copies were corrected locally, verifying every other spell field and archive entry unchanged. Owner gameplay retest remains pending; do not claim the approach-triggered bear-form issue resolved until tested.
