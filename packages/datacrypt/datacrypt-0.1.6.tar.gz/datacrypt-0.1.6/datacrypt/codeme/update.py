import utilum
import os
from . import hashing
from . import utils
from . import db
from . import sslKey
from . import uattributes
from . import otp
from . import status

# '''<BfsTemplate>'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


# class myDict(dict):
#     def __init__(self):
#         self = dict()

#     def add(self, key, value):
#         self[key] = value


# def bfsTraversal(self, start_path):
#     def deepBfs(paths, hashDict):
#         for p in paths:
#             if(os.path.isdir(p)):
#                 if(utils.checkIfPathShouldBeIgnored(self, p)):
#                     continue
#                 else:
#                     files = utils.listDirPathSlashFiltered(p)
#                     hashDict.add(p, myDict())
#                     if(len(files) > 0):
#                         hashDict[p].add("hashValue", hashing.hexxodFolder(p))
#                     else:
#                         hashDict[p].add("hashValue", -1)
#                     hashDict[p].add("type", "folder")
#                     hashDict[p].add("children", files)
#                     hashDict = deepBfs(files, hashDict)
#             elif(os.path.isfile(p)):
#                 if(utils.checkIfPathAndEpShouldBeIgnored(self, p)):
#                     continue
#                 else:
#                     hashDict.add(p, myDict())
#                     hashDict[p].add("hashValue", hashing.hexxod(p)[1])
#                     hashDict[p].add("type", "file")
#                     hashDict[p].add("children", [])
#             else:
#                 continue
#         return hashDict

#     hashDict = myDict()
#     hashDict = deepBfs([start_path], hashDict)
#     return hashDict
# '''</BfsTemplate>'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def processForDeletedEntities(self, hashDict):
    for filePath in hashDict:
        fileInfo = hashDict[filePath]
        if(fileInfo["deletedAt"] is None and fileInfo["type"] == 'file'):
            placeHolderPath = utils.associatedPlaceHolderPath(self, filePath)
            # print("placeHolderPath: ", placeHolderPath)
            if(utilum.file.isPathExist(filePath) == False and utilum.file.isPathExist(placeHolderPath) == False):
                db.deleteEncData(self, filePath)
        elif(fileInfo["deletedAt"] is None and fileInfo["type"] == 'folder'):
            if(utilum.file.isPathExist(filePath) == False):
                db.deleteEncData(self, filePath)
    return None


def printInitPath(self, p, initText):
    printableP = p
    if(os.path.isdir(p) == True):
        print(
            f'{uattributes.statusColor["init"]["folder"]}[{initText}][d]: {uattributes.colors.fg.lightgrey}{printableP}')
    else:
        print(
            f'{uattributes.statusColor["init"]["file"]}[{initText}][f]: {uattributes.colors.fg.lightgrey}{printableP}')
    return None


def initializeEnc(self, noPrint=False):
    hashDict, _ = status.statusEnc(self, True, [], True)
    self.hashDict = hashDict
    processForDeletedEntities(self, hashDict)

    def deepBfs(paths, noPrint):
        for p in paths:
            p = utils.sanitizePath(self, p)
            initText = 'Re-INITIALIZING'
            # print("p: ", p, os.path.isdir(p),
            #       utils.checkIfPathShouldBeIgnored(self, p))

            # 1) Traversing and Action
            if(os.path.isdir(p)):
                # 1) Folder
                if(utils.checkIfPathShouldBeIgnored(self, p)):
                    continue
                else:
                    files = utils.listDirPathSlashFiltered(self, p)
                    try:
                        hashValue = hashing.hexxodFolder(self, p)
                    except:
                        hashValue = -1
                    children = str(files)
                    encryptedChildren = sslKey.Crypt().encrypt(
                        children, self.config.creds.childrenKey)
                    try:
                        initText = "INITIALIZING"
                        db.insertEncData(self, p, hashValue, encryptedChildren,
                                         "folder", "init", "init")
                    except:
                        initText = "Re-INITIALIZING"
                        # 1) already commited
                        # error due to attempt of duplicate entry, this prevents hard-re-init

                        # 2) deleted
                        if(self.hashDict and self.hashDict[p] and self.hashDict[p]["deletedAt"] is not None):
                            # un-soft-delete
                            db.updateEncData(self, p, hashValue, encryptedChildren,
                                             "folder", "init")
                            utils.shreddAssociatedEncryptedFile(self, p)
                        pass
                    deepBfs(files, noPrint)
            elif(os.path.isfile(p)):
                # print("p: ", p)
                # 2) File
                if(utils.checkIfPathAndEpShouldBeIgnored(self, p)):
                    continue
                else:
                    # print("self.hashDict[p]: ", self.hashDict[p])
                    hashValue = hashing.hexxod(p)[1]
                    children = str([])
                    encryptedChildren = sslKey.Crypt().encrypt(
                        children, self.config.creds.childrenKey)
                    try:
                        initText = "INITIALIZING"
                        db.insertEncData(self,
                                         p, hashValue, encryptedChildren, "file", "init", "init")
                    except:
                        initText = "Re-INITIALIZING"
                        # 1) already commited
                        # error due to attempt of duplicate entry, this prevents hard-re-init

                        # 2) deleted
                        if(self.hashDict and self.hashDict[p] and self.hashDict[p]["deletedAt"] is not None):
                            # un-soft-delete
                            db.updateEncData(
                                self, p, hashValue, "file", "init")
                            utils.shreddAssociatedEncryptedFile(self, p)
                        pass
            else:
                continue

            # 2) Printing
            if(noPrint == False and utils.checkIfPathAndEpShouldBeIgnored(self, p) == False):
                printInitPath(self, p, initText)

        self.hashDict, _ = status.statusEnc(self, True, [], True)
        return True

    return deepBfs([self.basePath], noPrint)


def deleteFromDbAndStorage(self, entityPath):

    # 1) Db Shred
    db.deleteEncData(self, entityPath)

    # 2) File Shred
    if("/" in entityPath):
        rev = entityPath[::-1]
        ri = len(rev) - rev.index("/")
    else:
        ri = 0
    first = entityPath[:ri]
    last = entityPath[ri:]

    encEntityPath = self.config.storageBasePath + "/" + self.config.basePath
    encEntityPath = encEntityPath + "/" + f"{first}.{last}.enc259"

    if(os.path.isfile(encEntityPath) and (encEntityPath[-7:] == ".enc259" and encEntityPath[-9:] != ".name.txt")):
        print(
            f'{uattributes.colors.fg.red}[DELETING]: {uattributes.colors.fg.lightgrey}{entityPath}')
        utilum.file.removeFile(encEntityPath)
    return None


def deleteEnc(self, entityPath, deletingProceed=None):
    entityPath = utils.sanitizePath(self, entityPath)
    if(deletingProceed == None):
        deletingProceed = otp.deleteRecordOtp()
        if(deletingProceed == True):
            pass
        else:
            return

    fedep = db.fetchEncData(self, entityPath)
    if(len(fedep) >= 1):
        fedep = fedep[0]
        hashDict = dict()
        hashDict[entityPath] = fedep
    else:
        hashDict = {}
    if(utilum.file.isPathExist(entityPath)):
        if(len(hashDict) >= 1):
            if(os.path.isdir(entityPath)):
                files = utils.listDirPathSlashFiltered(self, entityPath)
                hashValue = -1 if (len(files) ==
                                   0) else hashing.hexxodFolder(entityPath)
                children = str(files)
                encryptedChildren = sslKey.Crypt().encrypt(
                    children, self.config.creds.childrenKey)
                db.updateEncData(self, entityPath, hashValue,
                                 encryptedChildren, "folder")
                deleteFromDbAndStorage(self, entityPath)
                for filePath in files:
                    deleteEnc(self, filePath, deletingProceed)
            else:
                db.updateEncData(self, entityPath, hashing.hexxod(
                    entityPath)[1], str([]), "file")
                deleteFromDbAndStorage(self, entityPath)
        else:
            if(os.path.isdir(entityPath)):
                files = utils.listDirPathSlashFiltered(self, entityPath)
                hashValue = -1 if (len(files) ==
                                   0) else hashing.hexxodFolder(entityPath)
                children = str(files)
                encryptedChildren = sslKey.Crypt().encrypt(
                    children, self.config.creds.childrenKey)
                db.insertEncData(self, entityPath, hashValue,
                                 encryptedChildren, "folder")
                deleteFromDbAndStorage(self, entityPath)
                for filePath in files:
                    deleteEnc(self, filePath, deletingProceed)
            else:
                db.insertEncData(self, entityPath, hashing.hexxod(
                    entityPath)[1], str([]), "file")
                deleteFromDbAndStorage(self, entityPath)
    else:
        deleteFromDbAndStorage(self, entityPath)


# deleteEnc(".")
# deleteEnc("api/")


def commitFile(self, filePath):
    filePath = utils.sanitizePath(self, filePath)
    dataDict = db.fetchEncData(self, filePath)[0]
    db.updateEncData(self, filePath, hashing.hexxod(filePath)[1], str(
        []), "file", "committed", dataDict["arena"])
    return None


def unCommitFile(self, filePath):
    filePath = utils.sanitizePath(self, filePath)
    dataDict = db.fetchEncData(self, filePath)[0]
    # print(f'{statusColor["committed"]}[UN-COMMITTING]: {colors.fg.lightgrey}{filePath}')
    db.updateEncData(self, filePath, dataDict["hashValue"], str(
        []), "file", dataDict["arenaBeforeCommit"])
    return None


def deleteAllEncStorage(self): utilum.file.deleteFolder(
    self.config.storageBasePath)

# use sqlite3, instead of json, because it will be superfast
# only files in staged will be encrypted(later only commited files will be encrypted)
