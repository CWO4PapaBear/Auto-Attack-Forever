local function UpdateIcon(button)
    if not button then return end
    local slot = button.action
    if not slot then return end
    local kind, id = GetActionInfo(slot)
    if kind ~= "spell" or id ~= 970100 then return end
    local texture = GetInventoryItemTexture("player", 18)
    local icon = button.icon or _G[button:GetName() .. "Icon"]
    if icon and texture then icon:SetTexture(texture) end
end
if hooksecurefunc then hooksecurefunc("ActionButton_Update", UpdateIcon) end
-- The dispatch button is not itself a shot. Reflect actual ranged repeats,
-- leaving the stock melee button's armed/flashing behavior unchanged.
local function UpdateRangedState(button)
    if not button or not button.action then return end
    local kind, id = GetActionInfo(button.action)
    if kind ~= 'spell' or id ~= 970100 then return end
    local active = IsAutoRepeatSpell(75) or IsAutoRepeatSpell(970101) or IsAutoRepeatSpell(970102)
    button:SetChecked(active and true or false)
    if active then
        if not ActionButton_IsFlashing(button) then ActionButton_StartFlash(button) end
    else
        ActionButton_StopFlash(button)
    end
end
if hooksecurefunc then
    hooksecurefunc('ActionButton_UpdateState', UpdateRangedState)
    hooksecurefunc('ActionButton_UpdateFlash', UpdateRangedState)
end
local frame = CreateFrame("Frame")
frame:RegisterEvent("PLAYER_ENTERING_WORLD")
frame:RegisterEvent("UNIT_INVENTORY_CHANGED")
frame:RegisterEvent("ACTIONBAR_SLOT_CHANGED")
frame:RegisterEvent("START_AUTOREPEAT_SPELL")
frame:RegisterEvent("STOP_AUTOREPEAT_SPELL")
frame:RegisterEvent("PLAYER_ENTER_COMBAT")
frame:RegisterEvent("PLAYER_LEAVE_COMBAT")
frame:SetScript("OnEvent", function(self, event, unit)
    if event == "UNIT_INVENTORY_CHANGED" and unit ~= "player" then return end
    for _, prefix in ipairs({"ActionButton", "MultiBarBottomLeftButton", "MultiBarBottomRightButton", "MultiBarRightButton", "MultiBarLeftButton"}) do
        for i=1,12 do
            local button = _G[prefix .. i]
            UpdateIcon(button)
            UpdateRangedState(button)
        end
    end
end)
