"""Exercise the actual Lua 5.1 option panel with server acknowledgements."""
from pathlib import Path
import os,sys
if os.environ.get('LUPA_PATH'):sys.path.insert(0,os.environ['LUPA_PATH'])
from lupa.lua51 import LuaRuntime
lua=LuaRuntime()
lua.execute('''
frames={};messages={};now=0;SlashCmdList={}
local methods={}
function methods:SetScript(k,v) self[k]=v end
function methods:SetText(v) self.text=v end
function methods:SetChecked(v) self.checked=v end
function methods:GetChecked() return self.checked end
function methods:GetName() return self.name end
function methods:Enable() self.enabled=true end
function methods:Disable() self.enabled=false end
function methods:SetPoint() end
function methods:SetWidth() end
function methods:SetJustifyH() end
function methods:RegisterEvent() end
function methods:CreateFontString() return setmetatable({},{__index=methods}) end
function CreateFrame(kind,name,parent,template)
 local f=setmetatable({name=name},{__index=methods});frames[#frames+1]=f
 if name then _G[name]=f;_G[name..'Text']=f:CreateFontString() end
 return f
end
function SendChatMessage(text) messages[#messages+1]=text end
function GetTime() return now end
function InterfaceOptions_AddCategory(p) category=p end
function InterfaceOptionsFrame_OpenToCategory(p) p.OnShow() end
function ChatFrame_AddMessageEventFilter(event,f) filter=f end
''')
lua.execute((Path(__file__).resolve().parents[1]/'client-addon/AdaptiveAutoAttack/Options.lua').read_text())
lua.execute('''
SlashCmdList.AUTOATTACKFOREVER()
assert(messages[1]=='.aaf ranged status')
local c=AutoAttackForeverRangedCheck;local e=frames[3]
assert(c.enabled==false)
e.OnEvent(nil,'CHAT_MSG_SYSTEM','AAF_RANGED 1')
assert(c.enabled and c.checked)
c:SetChecked(false);c.OnClick(c)
assert(messages[2]=='.aaf ranged off' and c.enabled==false)
e.OnEvent(nil,'CHAT_MSG_SYSTEM','AAF_RANGED 0')
assert(c.enabled and not c.checked)
c:SetChecked(true);c.OnClick(c)
assert(messages[3]=='.aaf ranged on')
now=9;e.OnUpdate();assert(not c.checked and not c.enabled)
category.OnShow();e.OnEvent(nil,'CHAT_MSG_SYSTEM','AAF_RANGED 1')
assert(c.enabled and c.checked)
assert(filter(nil,nil,'AAF_RANGED 0'))
assert(not filter(nil,nil,'Equip a ranged weapon to use Auto Ranged.'))
assert(not filter(nil,nil,'Other error'))
''')
print('PASS: actual Lua 5.1 options request/status/off/on, confirmed state, timeout/retry and scoped filtering.')
