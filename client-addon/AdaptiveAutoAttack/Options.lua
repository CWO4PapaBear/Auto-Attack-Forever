local panel = CreateFrame('Frame', 'AutoAttackForeverOptions')
panel.name = 'Auto-Attack Forever'
local title = panel:CreateFontString(nil, 'ARTWORK', 'GameFontNormalLarge')
title:SetPoint('TOPLEFT', 16, -16)
title:SetText(panel.name)
local description = panel:CreateFontString(nil, 'ARTWORK', 'GameFontHighlightSmall')
description:SetPoint('TOPLEFT', title, 'BOTTOMLEFT', 0, -14)
description:SetWidth(480)
description:SetJustifyH('LEFT')
description:SetText('Settings are saved for this character. Changes apply immediately.')
local check = CreateFrame('CheckButton', 'AutoAttackForeverRangedCheck', panel, 'InterfaceOptionsCheckButtonTemplate')
check:SetPoint('TOPLEFT', description, 'BOTTOMLEFT', 0, -20)
_G[check:GetName() .. 'Text']:SetText('Enable automatic ranged attacks')
local detail = panel:CreateFontString(nil, 'ARTWORK', 'GameFontHighlightSmall')
detail:SetPoint('TOPLEFT', check, 'BOTTOMLEFT', 4, -8)
detail:SetWidth(480)
detail:SetJustifyH('LEFT')
detail:SetText('When disabled, Auto-Attack Forever stays in melee mode even when your target moves away. Use this to avoid automatic ranged attacks taking you out of shapeshift forms. Manually casting other spells still follows their normal rules.')
local status = panel:CreateFontString(nil, 'ARTWORK', 'GameFontHighlightSmall')
status:SetPoint('TOPLEFT', detail, 'BOTTOMLEFT', 0, -18)
local confirmed, deadline
local function request(value)
    check:Disable()
    status:SetText('Waiting for server...')
    deadline = GetTime() + 8
    SendChatMessage('.aaf ranged ' .. value, 'SAY')
end
check:SetScript('OnClick', function(self) request(self:GetChecked() and 'on' or 'off') end)
panel:SetScript('OnShow', function() request('status') end)
local events = CreateFrame('Frame')
events:RegisterEvent('CHAT_MSG_SYSTEM')
events:SetScript('OnEvent', function(_, _, message)
    local value = type(message) == 'string' and message:match('^AAF_RANGED ([01])$')
    if not value then return end
    confirmed = value == '1'
    check:SetChecked(confirmed)
    check:Enable()
    deadline = nil
    status:SetText(confirmed and 'Automatic ranged attacks enabled.' or 'Melee only. Automatic ranged attacks disabled.')
end)
events:SetScript('OnUpdate', function()
    if deadline and GetTime() >= deadline then
        deadline = nil
        check:SetChecked(confirmed)
        status:SetText('Server did not confirm the setting. Reopen this panel to retry.')
    end
end)
ChatFrame_AddMessageEventFilter('CHAT_MSG_SYSTEM', function(_, _, message)
    return type(message) == 'string' and message:match('^AAF_RANGED [01]$') ~= nil
end)
InterfaceOptions_AddCategory(panel)
SLASH_AUTOATTACKFOREVER1 = '/aaf'
SlashCmdList.AUTOATTACKFOREVER = function() InterfaceOptionsFrame_OpenToCategory(panel) end
