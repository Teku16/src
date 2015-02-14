from toontown.toonbase.ToontownGlobals import *
from direct.gui.DirectGui import *
from direct.showbase.InputStateGlobal import inputState
from otp.ai.MagicWordGlobal import *
from otp.otpbase import OTPLocalizer
from toontown.toonbase import ToontownGlobals
from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *

class ModPanel():

    def unlocks():
        """
        #Unlocks the invoker's teleport access, emotions, and pet trick phrases.
            """
        target = spellbook.getTarget()

        # First, unlock their teleport access:
        hoods = list(ToontownGlobals.HoodsForTeleportAll)
        target.b_setHoodsVisited(hoods)
        target.b_setTeleportAccess(hoods)

        # Next, unlock all of their emotions:
        emotes = list(target.getEmoteAccess())
        for emoteId in OTPLocalizer.EmoteFuncDict.values():
            if emoteId >= len(emotes):
                continue
            # The following emotions are ignored because they are unable to be
            # obtained:
            if emoteId in (17, 18, 19):
                continue
            emotes[emoteId] = 1
        target.b_setEmoteAccess(emotes)

    # Finally, unlock all of their pet phrases:
        if simbase.wantPets:
            target.b_setPetTrickPhrases(range(7))

    def gmIcon(accessLevel=None):
        """
        #Toggles the target's GM icon. If an access level is provided, however, the
        #target's GM icon will be overridden.
        """
        invoker = spellbook.getInvoker()
        target = spellbook.getTarget()
        invokerAccess = spellbook.getInvokerAccess()
        if invokerAccess < CATEGORY_PROGRAMMER.defaultAccess:
            if accessLevel is not None:
                return "You must be of a higher access level to override your GM icon."
            target = spellbook.getInvoker()
        target.sendUpdate('setGM', [0])
        if target.isGM() and (accessLevel is None):
            target._gmDisabled = True
            if target == invoker:
                return 'Your GM icon has been disabled for this session!'
            return "%s's GM icon has been disabled for this session!" % target.getName()
        else:
            target._gmDisabled = False
            if accessLevel is None:
                accessLevel = target.getAdminAccess()
            if accessLevel != target.getGMType():
                if invokerAccess != CATEGORY_SYSTEM_ADMINISTRATOR.defaultAccess:
                    accessLevel = target.getGMType()
            if accessLevel not in (0,
                                   CATEGORY_COMMUNITY_MANAGER.defaultAccess,
                                   CATEGORY_MODERATOR.defaultAccess,
                                   CATEGORY_CREATIVE.defaultAccess,
                                   CATEGORY_PROGRAMMER.defaultAccess,
                                   CATEGORY_ADMINISTRATOR.defaultAccess,
                                   CATEGORY_SYSTEM_ADMINISTRATOR.defaultAccess):
                return 'Invalid access level!'
            target.b_setGM(accessLevel)
            if accessLevel == target.getAdminAccess():
                if target == invoker:
                    return 'Your GM icon is now enabled!'
                return "%s's GM icon is now enabled!" % target.getName()
            if target == invoker:
                return 'Your GM icon has been set to: ' + str(accessLevel)
            return "%s's GM icon has been set to: %d" % (target.getName(), accessLevel)

    def ghost():
        """
        #Toggles invisibility on the invoker. Anyone with an access level below the
        #invoker will not be able to see him or her.
        """
        invoker = spellbook.getInvoker()
        if invoker.ghostMode == 0:
            invoker.b_setGhostMode(2)
            return 'Ghost mode is enabled.'
        else:
            invoker.b_setGhostMode(0)
            return 'Ghost mode is disabled.'

    def badName():
        """
        #Revoke the target's name.
        """
        target = spellbook.getTarget()
        _name = target.getName()
        colorString = TTLocalizer.NumToColor[target.dna.headColor]
        animalType = TTLocalizer.AnimalToSpecies[target.dna.getAnimal()]
        target.b_setName(colorString + ' ' + animalType)
        target.sendUpdate('WishNameState', ['REJECTED'])
        return "Revoked %s's name!" % _name

    def globalTeleport():
        """
        #Activates the global teleport cheat.
        """
        invoker = spellbook.getInvoker()
        invoker.sendUpdate('setTeleportOverride', [1])
        invoker.setTeleportAccess(list(ToontownGlobals.HoodsForTeleportAll))
        return 'Global teleport has been activated.'

    def mute(minutes):
        """
        #Mute the target
        """
        if not MagicWordManager.lastClickedNametag:
            return "nobody selected"
        target = MagicWordManager.lastClickedNametag
        if spellbook.getInvokerAccess() <= target.getAdminAccess():
            return "Must be of a higher access level then target"
        base.cr.chatAgent.sendMuteAccount(target.doId, minutes)
        return 'Mute request sent'

    def unmute():
        """
        #Unmute the target
        """
        if not MagicWordManager.lastClickedNametag:
            return "nobody selected"
        target = MagicWordManager.lastClickedNametag
        if spellbook.getInvokerAccess() <= target.getAdminAccess():
            return "Must be of a higher access level then target"
        print ['unmute', target.doId]
        base.cr.chatAgent.sendUnmuteAccount(target.doId)
        return 'Unmute request sent'

    def run():
        """
        #Toggles debugging run speed.
        """
        inputState.set('debugRunning', inputState.isSet('debugRunning') != True)
        return 'Toggled debug run speed.'

    def collisionsOff():
        """
        #Turns collisions off.
        """
        base.localAvatar.collisionsOff()
        return 'Collisions are disabled.'

    def collisionsOn():
        """
        #Turns collisions on.
        """
        base.localAvatar.collisionsOn()
        return 'Collisions are enabled.'

    #Time for the buttons

    #Unlocks
    ButtonImage = loader.loadModel("phase_3/models/gui/quit_button.bam")
    ImgBtn1 = DirectButton(frameSize=None, text='Unlocks', image=(ButtonImage.find('**/QuitBtn_UP'), \
    ButtonImage.find('**/QuitBtn_DN'), ButtonImage.find('**/QuitBtn_RLVR')), relief=None, command=unlocks, text_pos=(0, -0.015), \
    geom=None, pad=(0.01, 0.01), suppressKeys=0, pos = (-1.15,-0,.31), text_scale=0.059, borderWidth=(0.015, 0.01), scale=.7)

    #gmIcon
    ButtonImage = loader.loadModel("phase_3/models/gui/quit_button.bam")
    ImgBtn2 = DirectButton(frameSize=None, text='gmIcon', image=(ButtonImage.find('**/QuitBtn_UP'), \
    ButtonImage.find('**/QuitBtn_DN'), ButtonImage.find('**/QuitBtn_RLVR')), relief=None, command=gmIcon, text_pos=(0, -0.015), \
    geom=None, pad=(0.01, 0.01), suppressKeys=0, pos = (-1.15,-0,.24), text_scale=0.059, borderWidth=(0.015, 0.01), scale=.7)

    #ghost
    ButtonImage = loader.loadModel("phase_3/models/gui/quit_button.bam")
    ImgBtn3 = DirectButton(frameSize=None, text='Ghost', image=(ButtonImage.find('**/QuitBtn_UP'), \
    ButtonImage.find('**/QuitBtn_DN'), ButtonImage.find('**/QuitBtn_RLVR')), relief=None, command=ghost, text_pos=(0, -0.015), \
    geom=None, pad=(0.01, 0.01), suppressKeys=0, pos = (-1.15,-0,.17), text_scale=0.059, borderWidth=(0.015, 0.01), scale=.7)

    #badName
    ButtonImage = loader.loadModel("phase_3/models/gui/quit_button.bam")
    ImgBtn4 = DirectButton(frameSize=None, text='Bad Name', image=(ButtonImage.find('**/QuitBtn_UP'), \
    ButtonImage.find('**/QuitBtn_DN'), ButtonImage.find('**/QuitBtn_RLVR')), relief=None, command=badName, text_pos=(0, -0.015), \
    geom=None, pad=(0.01, 0.01), suppressKeys=0, pos = (-1.15,-0,.10), text_scale=0.059, borderWidth=(0.015, 0.01), scale=.7)

    #globalTeleport
    ButtonImage = loader.loadModel("phase_3/models/gui/quit_button.bam")
    ImgBtn5 = DirectButton(frameSize=None, text='Global Teleport', image=(ButtonImage.find('**/QuitBtn_UP'), \
    ButtonImage.find('**/QuitBtn_DN'), ButtonImage.find('**/QuitBtn_RLVR')), relief=None, command=globalTeleport, text_pos=(0, -0.015), \
    geom=None, pad=(0.01, 0.01), suppressKeys=0, pos = (-1.15,-0,.03), text_scale=0.059, borderWidth=(0.015, 0.01), scale=.7)

    #mute
    ButtonImage = loader.loadModel("phase_3/models/gui/quit_button.bam")
    ImgBtn6 = DirectButton(frameSize=None, text='Mute', image=(ButtonImage.find('**/QuitBtn_UP'), \
    ButtonImage.find('**/QuitBtn_DN'), ButtonImage.find('**/QuitBtn_RLVR')), relief=None, command=mute, text_pos=(0, -0.015), \
    geom=None, pad=(0.01, 0.01), suppressKeys=0, pos = (1.1,-0,.31), text_scale=0.059, borderWidth=(0.015, 0.01), scale=.7)

