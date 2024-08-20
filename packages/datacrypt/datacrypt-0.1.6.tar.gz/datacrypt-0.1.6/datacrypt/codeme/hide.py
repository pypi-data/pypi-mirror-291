from . import utils
from . import hashing
from . import uattributes

from . import fileRunner
from . import changed
from . import update
from . import auth2

# '''
# hideType = "normal" # default, changed and staged file are hidden
# hideType = "hard" # all staged file are hidden
# hideType = "extreme" # all (init + staged) are hidden
# '''


def hideRun(self, hideType):
    authStatus = auth2.authorize(self)
    if(authStatus == True):
        pass
    else:
        return False

    creds = utils.getCreds(self)
    passwords = creds.passwords
    changedFiles = changed.changedFilesList(self, self.basePath, hideType)
    changedFilesLen = len(changedFiles)
    # print("hideRun: ", authStatus, changedFiles)

    for ifilePath, filePath in enumerate(changedFiles):
        filePath = utils.sanitizePath(self, filePath)

        if(filePath in self.hashDict and (utils.checkIfPathShouldBeIgnored(self, filePath) == False)):
            # checking for same file content via hashing comparison
            comparison = (
                self.hashDict[filePath]["hashValue"] == hashing.hexxod(filePath)[1])

            if(comparison and utils.checkCorrespondingEncryptedFile(self, filePath) == True):
                if(self.hashDict[filePath]["arena"] in ["staged", "committed"] or (self.hashDict[filePath]["arena"] in ["init", "staged", "committed"] and hideType == "extreme")):
                    # shredding the data-file (un-encrypted file)
                    print(
                        f'[{ifilePath+1}/{changedFilesLen}]{uattributes.colors.fg.lightblue}[SHREDDING]: {uattributes.colors.fg.lightgrey}', filePath)
                    update.commitFile(self, filePath)
                    fileRunner.shreddFile(self, filePath)
            else:
                if(self.hashDict[filePath]["arena"] in ["staged", "committed"] or (self.hashDict[filePath]["arena"] in ["init", "staged", "committed"] and hideType == "extreme")):
                    # encrypting the data-file (un-encrypted file)
                    print(
                        f'[{ifilePath+1}/{changedFilesLen}]{uattributes.colors.fg.lightblue}[HIDE]: {uattributes.colors.fg.lightgrey}', filePath)
                    update.commitFile(self, filePath)
                    fileRunner.fileEncrypt(self, filePath, passwords)
        else:
            continue
            # Not possible case
    return True
