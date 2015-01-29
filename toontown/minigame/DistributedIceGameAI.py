from direct.fsm.ClassicFSM import ClassicFSM
from direct.fsm.State import State

from toontown.minigame.DistributedMinigameAI import DistributedMinigameAI


class DistributedIceGameAI(DistributedMinigameAI):
    notify = directNotify.newCategory('DistributedIceGameAI')

    def __init__(self, air, minigameId):
        DistributedMinigameAI.__init__(self, air, minigameId)

        self.gameFSM = ClassicFSM('DistributedIceGameAI',
                                  [State('off', self.enterOff, self.exitOff, ['game']),
                                   State('game', self.enterGame, self.exitGame, ['cleanup', 'showScores']),
                                   State('showScores', self.enterShowScores, self.exitShowScores, ['cleanup']),
                                   State('cleanup', self.enterCleanup, self.exitCleanup, ['off'])], 'off', 'off')
        self.addChildGameFSM(self.gameFSM)

        self.spawnPosIndex = 0

    def setAvatarJoined(self):
        DistributedMinigameAI.setAvatarJoined(self)

        avId = self.air.getAvatarIdFromSender()
        self.sendUpdateToAvatarId(avId, 'setSpawnPosition', [self.spawnPosIndex])
        self.spawnPosIndex += 1

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def enterGame(self):
        pass

    def exitGame(self):
        pass

    def enterShowScores(self):
        pass

    def exitShowScores(self):
        pass

    def enterCleanup(self):
        pass

    def exitCleanup(self):
        pass
