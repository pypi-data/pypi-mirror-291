from . import utils
from . import uattributes
from . import fileRunner
from . import db
from . import update
from . import auth2


def showRunner(self, basePath):
    basePath = utils.sanitizePath(self, basePath)
    hashDict = db.fetchEncDataPathRegexp(self, basePath)

    authStatus = auth2.authorize(self)
    if(authStatus == True):
        pass
    else:
        return False

    creds = utils.getCreds(self)
    passwords = creds.passwordsReverse
    rows = []

    for irow, row in enumerate(hashDict):
        filePath = row["path"]
        if(row["arena"] in ["committed"] and row["type"] == "file" and (utils.checkIfPathShouldBeIgnored(self, filePath) == False)):
            rows.append(row)

    shownFilesLen = len(rows)
    for irow, row in enumerate(rows):
        hiddenFilePath = row["path"]
        print(
            f'[{irow+1}/{shownFilesLen}]{uattributes.colors.fg.blue}[SHOW]: {uattributes.colors.fg.lightgrey}', hiddenFilePath)
        update.unCommitFile(self, hiddenFilePath)
        fileRunner.fileShow(self, hiddenFilePath, passwords)
    return True


def showRunnerAll(self):
    dataDict = db.fetchEncDataCommitted(self)

    authStatus = auth2.authorize(self)
    if(authStatus == True):
        pass
    else:
        return False

    creds = utils.getCreds(self)
    passwords = creds.passwordsReverse
    shownFiles = []

    for row in dataDict:
        filePath = row["path"]
        if(filePath not in self.config.allIgnoredFiles and utils.checkIfPathShouldBeIgnored(self, filePath) == False):
            shownFiles.append(filePath)
    shownFilesLen = len(shownFiles)

    for ifilePath, filePath in enumerate(shownFiles):
        print(
            f'[{ifilePath+1}/{shownFilesLen}]{uattributes.colors.fg.blue}[SHOW]: {uattributes.colors.fg.lightgrey}', filePath)
        update.unCommitFile(self, filePath)
        fileRunner.fileShow(self, filePath, passwords)
    return True
