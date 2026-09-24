from pathlib import Path
import os,sys
if os.environ.get('LUPA_PATH'):sys.path.insert(0,os.environ['LUPA_PATH'])
from lupa.lua51 import LuaRuntime
lua=LuaRuntime()
lua.execute('''
hooks={};repeats={};starts=0;stops=0
function hooksecurefunc(name,f) hooks[name]=f end
function GetActionInfo(slot) return 'spell',slot==1 and 6603 or 970100 end
function GetInventoryItemTexture() return nil end
function IsAutoRepeatSpell(id) return repeats[id] end
function ActionButton_IsFlashing(b) return b.flashing end
function ActionButton_StartFlash(b) b.flashing=true;starts=starts+1 end
function ActionButton_StopFlash(b) b.flashing=false;stops=stops+1 end
function CreateFrame() return {RegisterEvent=function()end,SetScript=function(self,k,f) self[k]=f end} end
button={action=2,SetChecked=function(self,v)self.checked=v end}
melee={action=1,flashing=true,SetChecked=button.SetChecked}
''')
lua.execute((Path(__file__).resolve().parents[1]/'client-addon/AdaptiveAutoAttack/AdaptiveAutoAttack.lua').read_text())
lua.execute('''
hooks.ActionButton_UpdateState(button);assert(not button.checked and not button.flashing)
for _,id in ipairs({75,970101,970102}) do
 repeats[id]=true;hooks.ActionButton_UpdateState(button);assert(button.checked and button.flashing)
 local count=starts;hooks.ActionButton_UpdateFlash(button);assert(starts==count)
 repeats[id]=false;hooks.ActionButton_UpdateState(button);assert(not button.checked and not button.flashing)
end
local count=stops;hooks.ActionButton_UpdateState(melee);assert(melee.flashing and stops==count)
repeats[970100]=true;hooks.ActionButton_UpdateState(button);assert(not button.checked and not button.flashing)
''')
print('PASS: actual ranged indicator follows native shots, thrown and wand repeats; no pulse reset, no control-spell false positive, stock melee indicator unchanged.')
