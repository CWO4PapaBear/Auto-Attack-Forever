"""Compile the real packet hook against a minimal packet/session fixture."""
from pathlib import Path
import runpy,subprocess
context=runpy.run_path(str(Path(__file__).with_name('test_controller.py')))
out=context['out'];stub=context['stub'];command=context['command']
stub=stub.replace('#include <cassert>','#include <cassert>\n#include <vector>\n#include <initializer_list>\nusing uint8=uint8_t;\nstruct Player; struct WorldPacket;')
stub=stub.replace('struct Unit {','struct Unit { Player* ToPlayer(){return nullptr;} ')
stub=stub.replace('    Player(){guid.id=1;}', '''    Player(){guid.id=1;m_mover=this;}
    Player* m_mover;bool active=true,world=true,teleport=false,possess=false,vehicle=false;
    struct QueueEntry {bool cancelInProgress=false;};std::vector<QueueEntry> SpellQueue;
    bool HasActiveSpell(uint32 id){return active&&id==970100;}
    bool IsInWorld(){return world;}bool IsBeingTeleported(){return teleport;}
    bool GetVehicle(){return vehicle;}bool isPossessing(){return possess;}
''')
stub=stub.replace('struct SpellInfo {uint32 Id;};','struct SpellInfo {uint32 Id;bool IsPassive()const{return false;}};')
stub=stub.replace('struct SpellCastTargets {','struct SpellCastTargets {void Read(WorldPacket&,Player*);Unit* GetUnitTarget(){return target;} ')
stub=stub.replace('struct Config { template<class T> T GetOption(char const*,T value){return value;} };','struct Config { bool enabled=true;template<class T> T GetOption(char const*,T){return enabled;} };')
stub+=r'''
enum {SERVERHOOK_CAN_PACKET_RECEIVE,UNITHOOK_ON_UNIT_UPDATE,CMSG_ATTACKSTOP,CMSG_CANCEL_AUTO_REPEAT_SPELL,CMSG_ATTACKSWING,CMSG_CAST_SPELL};
struct WorldPacket {uint32 op=CMSG_CAST_SPELL,id=75;Unit* target=nullptr;uint32 bytes=6;
 uint32 GetOpcode()const{return op;}uint32 size()const{return bytes;}
 WorldPacket& operator>>(uint8& v){v=0;return *this;}
 WorldPacket& operator>>(uint32& v){v=id;return *this;}
 WorldPacket& operator>>(ObjectGuid& v){v=target?target->guid:ObjectGuid{};return *this;}
};
void SpellCastTargets::Read(WorldPacket& packet,Player*){target=packet.target;}
struct WorldSession {Player* player;Player* GetPlayer(){return player;}
 bool invalidate=false;void HandleClientCastFlags(WorldPacket&,uint8,SpellCastTargets&){if(invalidate)player->world=false;}
};
struct ServerScript {ServerScript(char const*,std::initializer_list<int>){}virtual bool CanPacketReceive(WorldSession*,WorldPacket const&){return true;}};
struct UnitScript {UnitScript(char const*,bool,std::initializer_list<int>){}virtual void OnUnitUpdate(Unit*,uint32){}};
'''
(out/'stub.h').write_text(stub)
for name in ('ScriptMgr.h','WorldSession.h','WorldPacket.h','Opcodes.h'):(out/name).write_text('#include "stub.h"\n')
source=(Path(__file__).resolve().parents[1]/'src/AttackHooks.cpp').as_posix()
test=r'''
int starts=0,stops=0;Unit* requested=nullptr;
void RangedAutoStart(Player*,Unit* target){++starts;requested=target;}
void RangedAutoStop(Player*){++stops;}
void RangedAutoClientCancel(Player*){}
void RangedAutoUpdate(Player*,uint32){}
int main(){
 adaptive_attack_packets hook;Player p;Unit enemy;WorldSession session{&p};WorldPacket packet;packet.target=&enemy;
 assert(!hook.CanPacketReceive(&session,packet)&&starts==1&&requested==&enemy); // native 75, not learned
 packet.id=970100;assert(!hook.CanPacketReceive(&session,packet)&&starts==2);
 packet.id=1978;assert(hook.CanPacketReceive(&session,packet)&&starts==2); // actual spell remains native
 packet.id=75;p.active=false;assert(hook.CanPacketReceive(&session,packet)&&starts==2);
 p.active=true;config.enabled=false;assert(hook.CanPacketReceive(&session,packet)&&starts==2);config.enabled=true;
 p.vehicle=true;assert(hook.CanPacketReceive(&session,packet)&&starts==2);p.vehicle=false;
 p.SpellQueue.push_back({true});assert(!hook.CanPacketReceive(&session,packet)&&starts==2);p.SpellQueue.clear();
 session.invalidate=true;assert(!hook.CanPacketReceive(&session,packet)&&starts==2);session.invalidate=false;p.world=true;
 packet.op=CMSG_ATTACKSTOP;assert(hook.CanPacketReceive(&session,packet)&&stops==1);
}
'''
(out/'hooks.cpp').write_text('#include "'+source+'"\n'+test)
subprocess.run(command+['-std=c++17','-I'+str(out),str(out/'hooks.cpp'),'-o',str(out/'hooks.exe')],check=True)
subprocess.run([str(out/'hooks.exe')],check=True)
print('PASS: compiled native/custom requests, authorization, ordinary spells, disabled module, vehicles, queued cancel, world changes and explicit stop routing.')
