import os
from . import hashing
from . import utils


def changedFilesList(self, basePath, hideType="normal"):

    def isEntityChanged(entityPath):
        if(os.path.isdir(entityPath)):
            try:
                hashValue = hashing.hexxodFolder(entityPath)
            except:
                hashValue = -1
            if(self.hashDict[entityPath]["hashValue"] == hashValue):
                return False
        else:
            hashValue = hashing.hexxod(entityPath)[1]
            if(self.hashDict[entityPath]["hashValue"] == hashValue):
                return False
        return True

    def bfsHide(self, start_path):
        # Bfs Traversing
        def deepBfs(self, paths, allFiles):
            for entityPath in paths:
                # print("entityPath: ", entityPath)

                if(entityPath in self.hashDict):
                    # checking for initialization inside hash-map
                    if(os.path.isdir(entityPath) == True):
                        # 1) Folder Commit
                        if((self.hashDict[entityPath]["arena"] in ["init", "staged"]) or hideType == "extreme"):
                            isChanged = isEntityChanged(entityPath)
                            if(isChanged == True or hideType in ["hard", "extreme"]):
                                files = utils.listDirPathSlashFiltered(
                                    self, entityPath)
                                allFiles = deepBfs(self, files, allFiles)
                        else:
                            return allFiles
                    else:
                        # 2) File Commit
                        if(self.hashDict[entityPath]["arena"] in ["staged", "committed"] or hideType in ["hard", "extreme"]):
                            isChanged = isEntityChanged(entityPath)
                            if(isChanged == True or hideType in ["hard", "extreme"] or utils.checkCorrespondingEncryptedFile(self, entityPath) == False):
                                allFiles.append(entityPath)
                else:
                    # file/folder is ignored
                    continue
            return allFiles
        allFiles = []
        allFiles = deepBfs(self, [start_path], allFiles)
        return allFiles

    changedFiles = bfsHide(self, basePath)
    return changedFiles
