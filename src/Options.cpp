// SPDX-License-Identifier: GPL-2.0-or-later
#include "Player.h"
#include "Chat.h"
#include "ScriptMgr.h"
#include "CommandScript.h"
#include "World.h"
#include "WorldSession.h"
#include "RBAC.h"
using namespace Acore::ChatCommands;

void RangedAutoUpdate(Player*, uint32);
namespace {
constexpr char Settings[] = "auto_attack_forever";
}
bool RangedAutoEnabled(Player* player)
{
    // Unset is enabled, preserving existing behavior for every character.
    return player->GetPlayerSetting(Settings, 0).value != 1;
}
namespace {
bool Status(ChatHandler* handler)
{
    handler->SendSysMessage(RangedAutoEnabled(handler->GetSession()->GetPlayer()) ? "AAF_RANGED 1" : "AAF_RANGED 0");
    return true;
}
bool Set(ChatHandler* handler, bool enabled)
{
    if (!sWorld->getBoolConfig(CONFIG_PLAYER_SETTINGS_ENABLED))
    {
        handler->SendSysMessage("Auto-Attack Forever: per-character settings are unavailable on this server.");
        return true;
    }
    Player* player = handler->GetSession()->GetPlayer();
    player->UpdatePlayerSetting(Settings, 0, enabled ? 0 : 1);
    // Apply to an already managed attack, including stopping a ranged repeat.
    RangedAutoUpdate(player, 100);
    return Status(handler);
}
bool On(ChatHandler* h){return Set(h,true);}
bool Off(ChatHandler* h){return Set(h,false);}
class Options final : public CommandScript {
public:
    Options():CommandScript("AutoAttackForeverOptions"){}
    ChatCommandTable GetCommands() const override
    {
        static ChatCommandTable ranged={{"on",On,rbac::RBAC_PERM_COMMAND_ACCOUNT,Console::No},{"off",Off,rbac::RBAC_PERM_COMMAND_ACCOUNT,Console::No},{"status",Status,rbac::RBAC_PERM_COMMAND_ACCOUNT,Console::No}};
        static ChatCommandTable root={{"ranged",ranged}};
        return {{"aaf",root}};
    }
};
}
void RegisterAdaptiveAttackOptions(){new Options();}
