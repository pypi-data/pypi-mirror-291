import utilum
import json

from codeme import update
from codeme import db
from codeme import dbAdmin


class Creds:
    def __init__(self, salt=None, ivString=None, keyString=None, childrenKey=None):
        if(salt is None):
            self.salt = utilum.string.randomCharStream(16, False)
        else:
            self.salt = salt
        if(ivString is None):
            self.ivString = utilum.string.randomCharStream(16, False)
        else:
            self.ivString = ivString
        if(keyString is None):
            self.keyString = utilum.string.randomCharStream(32, False)
        else:
            self.keyString = keyString
        if(childrenKey is None):
            self.childrenKey = utilum.string.randomCharStream(32, False)
        else:
            self.childrenKey = childrenKey


def run(self):
    # 1) Base Folder
    utilum.file.createPath(self.config.encBasePath)

    # 2) Storage
    utilum.file.createPath(self.config.storageBasePath)
    utilum.file.createPath(self.config.storageGitKeepPath)

    # 3) Database
    utilum.file.createPath(self.config.databasePath)

    # 4) Credentials
    utilum.file.createPath(self.config.credsPath)
    if(utilum.file.isFileEmpty(self.config.credsPath) == True):
        creds = Creds()
        credsContext = {
            "salt": creds.salt,
            "ivString": creds.ivString,
            "keyString": creds.keyString,
            "childrenKey": creds.childrenKey,
        }
        self.config.setCredentials(creds)
        stringifiedJson = json.dumps(credsContext, separators=(',', ':'))
        utilum.file.clearFile(self.config.credsPath)
        utilum.file.writeFile(self.config.credsPath, stringifiedJson)
    else:
        credsData = json.load(open(self.config.credsPath))
        creds = Creds(credsData['salt'], credsData['ivString'],
                      credsData['keyString'], credsData['childrenKey'])
        self.config.setCredentials(creds)

    return None


def run2(self):
    # 5) Initialization
    db.createEncTable(self)
    db.createEncTableIndex(self)
    dbAdmin.createAdminTable(self)
    dbAdmin.createPasswordsTable(self)
    update.initializeEnc(self)

    return None
