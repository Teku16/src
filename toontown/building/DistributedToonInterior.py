import cPickle
import random

import ToonInterior
import ToonInteriorColors
from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedObject
from direct.distributed.ClockDelta import *
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from direct.interval.IntervalGlobal import *
from otp.speedchat import SpeedChatGlobals
from pandac.PandaModules import *
from toontown.dna.DNAParser import DNADoor
from toontown.hood import ZoneUtil
from toontown.toon import ToonDNA
from toontown.toon import ToonHead
from toontown.toon.DistributedNPCToonBase import DistributedNPCToonBase
from toontown.toonbase import ToontownGlobals
from toontown.toonbase.ToonBaseGlobal import *
from direct.interval.IntervalGlobal import *
from toontown.toon import Toon


SIGN_LEFT = -4
SIGN_RIGHT = 4
SIGN_BOTTOM = -3.5
SIGN_TOP = 1.5
FrameScale = 1.4

class DistributedToonInterior(DistributedObject.DistributedObject):

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        self.fsm = ClassicFSM.ClassicFSM('DistributedToonInterior', [State.State('toon', self.enterToon, self.exitToon, ['beingTakenOver']), State.State('beingTakenOver', self.enterBeingTakenOver, self.exitBeingTakenOver, []), State.State('off', self.enterOff, self.exitOff, [])], 'toon', 'off')
        self.fsm.enterInitialState()

    def generate(self):
        DistributedObject.DistributedObject.generate(self)

    def announceGenerate(self):
        DistributedObject.DistributedObject.announceGenerate(self)
        self.setup()

    def disable(self):
        try:
            self.interior.removeNode()
            self.p.removeNode()
            self.bar.removeNode()
            self.table.removeNode()
            self.table2.removeNode()
            self.bartender1.cleanup()
            self.bartender1.removeNode()
            self.bartender2.cleanup()
            self.bartender2.removeNode()
            self.stripper.cleanup()
            self.stripper.removeNode()
            self.bottle1.removeNode()
            self.bottle2.removeNode()
            self.bottle3.removeNode()
            self.mug.removeNode()
        except:
            pass
        del self.interior
        self.ignore(SpeedChatGlobals.SCStaticTextMsgEvent)
        DistributedObject.DistributedObject.disable(self)

    def delete(self):
        del self.fsm
        self.ignore(SpeedChatGlobals.SCStaticTextMsgEvent)
        DistributedObject.DistributedObject.delete(self)

    def randomDNAItem(self, category, findFunc):
        codeCount = self.dnaStore.getNumCatalogCodes(category)
        index = self.randomGenerator.randint(0, codeCount - 1)
        code = self.dnaStore.getCatalogCode(category, index)
        return findFunc(code)

    def replaceRandomInModel(self, model):
        baseTag = 'random_'
        npc = model.findAllMatches('**/' + baseTag + '???_*')
        for i in xrange(npc.getNumPaths()):
            np = npc.getPath(i)
            name = np.getName()
            b = len(baseTag)
            category = name[b + 4:]
            key1 = name[b]
            key2 = name[b + 1]
            if key1 == 'm':
                model = self.randomDNAItem(category, self.dnaStore.findNode)
                newNP = model.copyTo(np)
                c = render.findAllMatches('**/collision')
                c.stash()
                if key2 == 'r':
                    self.replaceRandomInModel(newNP)
            elif key1 == 't':
                texture = self.randomDNAItem(category, self.dnaStore.findTexture)
                np.setTexture(texture, 100)
                newNP = np
            if key2 == 'c':
                if category == 'TI_wallpaper' or category == 'TI_wallpaper_border':
                    self.randomGenerator.seed(self.zoneId)
                    newNP.setColorScale(self.randomGenerator.choice(self.colors[category]))
                else:
                    newNP.setColorScale(self.randomGenerator.choice(self.colors[category]))

    def setup(self):
        self.dnaStore = base.cr.playGame.dnaStore
        self.randomGenerator = random.Random()
        self.randomGenerator.seed(self.zoneId)
        if base.localAvatar.getZoneId() == 9501:
            self.interior = loader.loadModel('phase_4/models/modules/ttc_library_interior.bam')
            self.interior.reparentTo(render)
        else:
            interior = self.randomDNAItem('TI_room', self.dnaStore.findNode)
            self.interior = interior.copyTo(render)
        hoodId = ZoneUtil.getCanonicalHoodId(self.zoneId)
        self.colors = ToonInteriorColors.colors[hoodId]
        self.replaceRandomInModel(self.interior)
        doorModelName = 'door_double_round_ul'
        if doorModelName[-1:] == 'r':
            doorModelName = doorModelName[:-1] + 'l'
        else:
            doorModelName = doorModelName[:-1] + 'r'
        door = self.dnaStore.findNode(doorModelName)
        door_origin = render.find('**/door_origin;+s')
        doorNP = door.copyTo(door_origin)
        door_origin.setScale(0.8, 0.8, 0.8)
        door_origin.setPos(door_origin, 0, -0.025, 0)
        color = self.randomGenerator.choice(self.colors['TI_door'])
        DNADoor.setupDoor(doorNP, self.interior, door_origin, self.dnaStore, str(self.block), color)
        doorFrame = doorNP.find('door_*_flat')
        doorFrame.wrtReparentTo(self.interior)
        doorFrame.setColor(color)
        sign = hidden.find('**/tb%s:*_landmark_*_DNARoot/**/sign;+s' % (self.block,))
        if not sign.isEmpty():
            signOrigin = self.interior.find('**/sign_origin;+s')
            newSignNP = sign.copyTo(signOrigin)
            newSignNP.setDepthWrite(1, 1)
            #TODO: getSignTransform
            #mat = self.dnaStore.getSignTransformFromBlockNumber(int(self.block))
            inv = Mat4(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
            #inv.invertFrom(mat)
            newSignNP.setMat(inv)
            newSignNP.flattenLight()
            ll = Point3()
            ur = Point3()
            newSignNP.calcTightBounds(ll, ur)
            width = ur[0] - ll[0]
            height = ur[2] - ll[2]
            if width != 0 and height != 0:
                xScale = (SIGN_RIGHT - SIGN_LEFT) / width
                zScale = (SIGN_TOP - SIGN_BOTTOM) / height
                scale = min(xScale, zScale)
                xCenter = (ur[0] + ll[0]) / 2.0
                zCenter = (ur[2] + ll[2]) / 2.0
                newSignNP.setPosHprScale((SIGN_RIGHT + SIGN_LEFT) / 2.0 - xCenter * scale, -0.1, (SIGN_TOP + SIGN_BOTTOM) / 2.0 - zCenter * scale, 0.0, 0.0, 0.0, scale, scale, scale)
        trophyOrigin = self.interior.find('**/trophy_origin')
        trophy = self.buildTrophy()
        if trophy:
            trophy.reparentTo(trophyOrigin)
        del self.colors
        del self.dnaStore
        del self.randomGenerator
        self.interior.flattenMedium()
        for npcToon in self.cr.doFindAllInstances(DistributedNPCToonBase):
            npcToon.initToonState()
        #custom Snooze Bar :D
        if base.localAvatar.getZoneId() == 9503:
            try:
                self.p.removeNode()
                self.bar.removeNode()
                self.table.removeNode()
                self.table2.removeNode()
                self.bartender1.cleanup()
                self.bartender1.removeNode()
                self.bartender2.cleanup()
                self.bartender2.removeNode()
                self.stripper.cleanup()
                self.stripper.removeNode()
                self.bottle1.removeNode()
                self.bottle2.removeNode()
                self.bottle3.removeNode()
                self.mug.removeNode()
            except:
                pass
            base.localAvatar.setSystemMessage(0, "You're in the Snooze bar!")
            self.bar = loader.loadModel('phase_4/models/potco_files/interior_tavern_vip.bam')
            self.bar.find('**/storageframebar').setX(self.bar.find('**/storageframebar').getX()+1.5)
            self.bar.find('**/barcounterwall1').removeNode()
            self.bar.find('**/barcounterwall').removeNode()
            self.bar.find('**/int_vip_room:floor').setZ(self.bar.find('**/int_vip_room:floor').getZ()+1)
            self.bar.find('**/door_1').removeNode()
            self.bar.find('**/col_doors').removeNode()
            self.bar.find('**/door_locator').removeNode()
            self.bar.reparentTo(render)
            self.bar.setPos(-17.200,  16.95,  0)
            self.bar.setScale(.65)

            self.p = loader.loadModel('phase_11/models/lawbotHQ/LB_torch_lampB.bam')
            self.p.reparentTo(render)
            self.p.setPos(-49,  58,  .5)
            self.p.setScale(.8,.8,1)
            self.p.setColor(.6,.6,.6)

            self.table = loader.loadModel('phase_5.5/models/estate/UWtable.bam')
            self.table.reparentTo(render)
            self.table.setPos(-43.920,  11,  .675)
            self.table.setScale(1.25,1.25,.75)

            self.table2 = loader.loadModel('phase_5.5/models/estate/UWtable.bam')
            self.table2.reparentTo(render)
            self.table2.setPos(-24.340,  10,  .675)
            self.table2.setScale(1.25,1.25,.75)
            
            self.mug = loader.loadModel('phase_4/models/potco_files/mug_zero.bam')
            self.mug.reparentTo(render)
            self.mug.setPos(-12.973,  38.274,  3)
            self.mug.setScale(1.5)
            
            self.bottle1 = loader.loadModel('phase_4/models/potco_files/bottle_high.bam')
            self.bottle1.reparentTo(render)
            self.bottle1.setPos(-15.973,  44,  3.8)
            self.bottle1.setScale(2.5)
            self.bottle1.setHpr(0,90,0)
            self.bottle1.setColor(1,.8,1)

            self.bottle2 = loader.loadModel('phase_4/models/potco_files/bottle_high.bam')
            self.bottle2.reparentTo(render)
            self.bottle2.setPos(-14.973,  44,  3.75)
            self.bottle2.setScale(2.2)
            self.bottle2.setHpr(0,90,0)
            self.bottle2.setColor(1,.3,.8)

            self.bottle3 = loader.loadModel('phase_4/models/potco_files/bottle_high.bam')
            self.bottle3.reparentTo(render)
            self.bottle3.setPos(-16.973,  43.8,  3.7)
            self.bottle3.setScale(2)
            self.bottle3.setHpr(0,90,0)
            self.bottle3.setColor(.4,.4,.4)
                
            #remove toon int, broken gets rid of npc too
            bldg = base.cr.doFindAll("DistributedToonInterior")
            for bldg in base.cr.doFindAll("DistributedToonInterior"):
                bldg.interior.find('**/ceiling').removeNode()
                bldg.interior.find('**/random_tc1_TI_wallpaper').removeNode()
                bldg.interior.find('**/random_to1_TI_molding').removeNode()
                bldg.interior.find('**/random_tc1_TI_floor').removeNode()
                bldg.interior.find('**/walls_1').removeNode()
                bldg.interior.find('**/floor').removeNode()
                bldg.interior.find('**/random_mo1_TI_counter').removeNode()
                bldg.interior.find('**/random_mr1_TI_couch_1person').removeNode()
                bldg.interior.find('**/random_mr1_TI_couch_2person').removeNode()
                bldg.interior.find('**/random_mr2_TI_couch_2person').removeNode()
                bldg.interior.find('**/external').removeNode()
                bldg.interior.find('**/random_tc1_TI_wallpaper_border').removeNode()
                bldg.interior.find('**/random_tc1_TI_wainscotting').removeNode()
                bldg.interior.find('**/picture').removeNode()
                bldg.interior.find('**/arch').removeNode()
                bldg.interior.find('**/door').removeNode()
                bldg.interior.find('**/arch2').removeNode()
                bldg.interior.find('**/random_tc2_TI_floor').removeNode()
                bldg.interior.find('**/door_double_round_ur_flat').setX(0.68)
                bldg.interior.find('**/npc_origin_0').setPos(2.5,  19.597,  0.525)
                bldg.interior.find('**/npc_origin_0').setHpr(175,0,0)
            #move npc to behind counter, if it ever works
            # stuff = base.cr.doFindAll('render/toon')
            # for stuff in base.cr.doFindAll('render/toon'):
                # stuff.setPos(10.5,  14.222,  -1.7)
                # stuff.setScale(1.4)
                # stuff.setHpr(90,0,0)
                
            def talk0():
                name = base.localAvatar.getName()
                self.bartender1.displayTalk('Hey, %s!' % name)
            def talk01():
                name = base.localAvatar.getName()
                self.bartender2.displayTalk('Hey, %s! What can I getcha\'?' % name)
            def talk1():
                self.bartender1.displayTalk('Welcome to the Snooze Bar!')
            def talk2():
                self.bartender1.displayTalk('I\'m a bot!')
            def bartender1Talk():
                seq = Sequence()
                seq.append(Func(talk0))
                seq.append(Wait(4))
                seq.append(Func(talk1))
                seq.append(Wait(4))
                seq.append(Func(talk2))
                seq.append(Wait(4))
                seq.start()
                
            def bartender2Talk():
                seq = Sequence()
                seq.append(Wait(4))
                seq.append(Func(talk01))
                seq.append(Wait(4))
                seq.start()
            
            def createToon(instName, toonName, toonPos, toonHpr, toonScale=1, anim='neutral'):
                try:
                    newToon.cleanup()
                    newToon.removeNode()
                except:
                    pass
                newToon = instName
                newToon = Toon.Toon()
                newToon.reparentTo(render)
                newToon.doId = base.localAvatar.doId
                newToon.setupToonNodes()
                newToon.setName(toonName)
                newToon.setPos(toonPos)
                newToon.setHpr(toonHpr)
                newToon.setScale(toonScale)
                newToon.startBlink()
                newToon.showNametag2d()
                newToon.startLookAround()
                newToon.initializeBodyCollisions('FD_NPC-Collisions_' + str(newToon.doId))
                newToon.setDNAString('t\x01\x01\x00\x00\x50\x1b\x45\x1b\x21\x1b\x08\x02\x08\x08')
                newToon.loop(anim)
                pos = newToon.getPos()
                hpr = newToon.getHpr()
                strPos = '(%.3f' % pos[0] + '\n %.3f' % pos[1] + '\n %.3f)' % pos[2]
                strHpr = '(%.3f' % hpr[0] + '\n %.3f' % hpr[1] + '\n %.3f)' % hpr[2]
                print "%s = Toon.Toon()" % instName
                print "%s.reparentTo(render)" % instName
                print "%s.doId = base.localAvatar.doId" % instName
                print "%s.setupToonNodes()" % instName
                print "%s.setName('%s')" % (instName, toonName)
                print '%s.setPos' % instName, strPos.replace('\n', ',')
                print '%s.setHpr' % instName, strHpr.replace('\n', ',')
                print "%s.setScale(%d)" % (instName, toonScale)
                print "%s.startBlink()" % instName
                print "%s.showNametag2d()" % instName
                print "%s.startLookAround()" % instName
                print "%s.initializeBodyCollisions('FD_NPC-Collisions_' + str(%s.doId))" % (instName, instName)
                print '%s.setDNAString("t\x01\x01\x00\x00\x50\x1b\x45\x1b\x21\x1b\x08\x02\x08\x08")' % instName
                print "%s.loop('%s')" % (instName, anim)
                
            
            self.bartender1 = Toon.Toon()
            self.bartender1.reparentTo(render)
            self.bartender1.doId = base.localAvatar.doId
            self.bartender1.setupToonNodes()
            self.bartender1.setName('Bartender\nBri')
            self.bartender1.setPos(-13.579,  41,  1.5)
            self.bartender1.setHpr(180,0,0)
            self.bartender1.setScale(1)
            self.bartender1.startBlink()
            self.bartender1.showNametag2d()
            self.bartender1.startLookAround()
            self.bartender1.initializeBodyCollisions('FD_NPC-Collisions_' + str(self.bartender1.doId))
            self.bartender1.setDNAString('t\x01\x01\x00\x00\x50\x1b\x45\x1b\x21\x1b\x08\x02\x08\x08')
            bartender1Talk()
            #bartender1.displayTalk('Welcome to the Snooze Bar!')
            self.bartender1.loop('neutral')
            
            self.bartender2 = Toon.Toon()
            self.bartender2.reparentTo(render)
            self.bartender2.doId = base.localAvatar.doId
            self.bartender2.setupToonNodes()
            self.bartender2.setName('Bartender\nBrad')
            self.bartender2.setPos(-29.579,  41,  1.26)
            self.bartender2.setHpr(220,0,0)
            self.bartender2.setScale(1)
            self.bartender2.startBlink()
            self.bartender2.showNametag2d()
            self.bartender2.startLookAround()
            self.bartender2.initializeBodyCollisions('FD_NPC-Collisions_' + str(self.bartender1.doId))
            self.bartender2.setDNAString('t\x05\x02\x00\x01\x83\x1b\x76\x1b\x0d\x1b\x0d\x00\x0d\x0d')
            bartender2Talk()
            #bartender2.displayTalk('Welcome to the Snooze Bar!')
            self.bartender2.loop('neutral')
            
            self.stripper = Toon.Toon()
            self.stripper.reparentTo(render)
            self.stripper.doId = base.localAvatar.doId
            self.stripper.setupToonNodes()
            self.stripper.setName('Crystal')
            self.stripper.setPos(-49.5,  57.85,  1.1)
            self.stripper.setHpr(220,0,0)
            self.stripper.setScale(.85)
            self.stripper.startBlink()
            self.stripper.showNametag2d()
            self.stripper.startLookAround()
            self.stripper.initializeBodyCollisions('FD_NPC-Collisions_' + str(self.stripper.doId))
            self.stripper.setDNAString('t\x01\x07\x00\x00\x29\x1b\x1e\x1b\x25\x1b\x24\x1a\x24\x24')
            #stripper.displayTalk('Welcome to the Snooze Bar!')
            self.stripper.loop('swing')
        else:
            try:
                p.removeNode()
                self.bar.removeNode()
                self.table.removeNode()
                self.table2.removeNode()
                self.bartender1.cleanup()
                self.bartender1.removeNode()
                self.bartender2.cleanup()
                self.bartender2.removeNode()
                self.stripper.cleanup()
                self.stripper.removeNode()
                self.bottle1.removeNode()
                self.bottle2.removeNode()
                self.bottle3.removeNode()
                self.mug.removeNode()
            except:
                pass
        
        

    def setZoneIdAndBlock(self, zoneId, block):
        self.zoneId = zoneId
        self.block = block

    def setToonData(self, toonData):
        savedBy = cPickle.loads(toonData)
        self.savedBy = savedBy

    def buildTrophy(self):
        if self.savedBy == None:
            return
        numToons = len(self.savedBy)
        pos = 1.25 - 1.25 * numToons
        trophy = hidden.attachNewNode('trophy')
        for avId, name, dnaTuple in self.savedBy:
            frame = self.buildFrame(name, dnaTuple)
            frame.reparentTo(trophy)
            frame.setPos(pos, 0, 0)
            pos += 2.5

        return trophy

    def buildFrame(self, name, dnaTuple):
        frame = loader.loadModel('phase_3.5/models/modules/trophy_frame')
        dna = ToonDNA.ToonDNA()
        apply(dna.newToonFromProperties, dnaTuple)
        head = ToonHead.ToonHead()
        head.setupHead(dna)
        head.setPosHprScale(0, -0.05, -0.05, 180, 0, 0, 0.55, 0.02, 0.55)
        if dna.head[0] == 'r':
            head.setZ(-0.15)
        elif dna.head[0] == 'h':
            head.setZ(0.05)
        elif dna.head[0] == 'm':
            head.setScale(0.45, 0.02, 0.45)
        head.reparentTo(frame)
        nameText = TextNode('trophy')
        nameText.setFont(ToontownGlobals.getToonFont())
        nameText.setAlign(TextNode.ACenter)
        nameText.setTextColor(0, 0, 0, 1)
        nameText.setWordwrap(5.36 * FrameScale)
        nameText.setText(name)
        namePath = frame.attachNewNode(nameText.generate())
        namePath.setPos(0, -0.03, -.6)
        namePath.setScale(0.186 / FrameScale)
        frame.setScale(FrameScale, 1.0, FrameScale)
        return frame

    def setState(self, state, timestamp):
        self.fsm.request(state, [globalClockDelta.localElapsedTime(timestamp)])

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def enterToon(self):
        pass

    def exitToon(self):
        pass

    def enterBeingTakenOver(self, ts):
        messenger.send('clearOutToonInterior')

    def exitBeingTakenOver(self):
        pass
        
#    def removeToonInt(self):
#        self.interior.removeNode()
