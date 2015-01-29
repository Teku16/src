from toontown.minigame.DistributedMinigame import DistributedMinigame
from toontown.minigame import IceGameGlobals
from toontown.dna.DNAParser import DNABulkLoader
from toontown.dna.DNAStorage import DNAStorage
from toontown.toonbase import TTLocalizer


class DistributedIceGame(DistributedMinigame):
    notify = directNotify.newCategory('DistributedIceGame')

    def __init__(self, cr):
        DistributedMinigame.__init__(self, cr)

        self.spawnPosition = None
        self.scene = None

    def getTitle(self):
        return TTLocalizer.IceGameTitle

    def getInstructions(self):
        return 'No Instructions :('

    def getMaxDuration(self):
        return 0

    def load(self):
        DistributedMinigame.load(self)

        dnaStorage = DNAStorage()
        bulkLoader = DNABulkLoader(dnaStorage, ('phase_4/dna/storage.pdna', 'phase_8/dna/storage_BR.pdna',
                                                'phase_8/dna/storage_BR_sz.pdna')
        )
        bulkLoader.loadDNAFiles()

        sceneNode = loader.loadDNAFile(dnaStorage, 'phase_8/dna/the_burrrgh_sz.pdna')
        self.scene = hidden.attachNewNode(sceneNode)

        dnaStorage.cleanup()

    def unload(self):
        DistributedMinigame.unload(self)

        self.scene.removeNode()
        del self.scene

    def onstage(self):
        DistributedMinigame.onstage(self)

        self.scene.reparentTo(render)

    def offstage(self):
        self.scene.hide()

        DistributedMinigame.offstage(self)

    def setSpawnPosition(self, spawnPosition):
        self.spawnPosition = spawnPosition

        base.localAvatar.setPos(IceGameGlobals.StartingPositions[self.spawnPosition][0])
        base.localAvatar.setH(IceGameGlobals.StartingPositions[self.spawnPosition][1])
