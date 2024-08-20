import utilum
import datetime
import os
from . import hashing
from . import dbAdmin
from . import db
from . import show
from . import update
from . import otp


# 1) authorize password
# check/auth by password
def authorize(self):
    credsBasePath = self.config.credsBasePath
    if(utilum.file.isPathExist(credsBasePath)):
        pass
    else:
        return False

    files = utilum.file.listDirPath(credsBasePath)
    upath = os.path.join(credsBasePath, 'u.txt')
    pExist = True

    for ifile in range(1, len(files)):
        pf = os.path.join(credsBasePath, f'p{ifile}.txt')
        if(utilum.file.isPathExist(pf) == False):
            pExist = False
            break

    # print(pExist)
    if(utilum.file.isPathExist(upath) and pExist):
        username = utilum.file.readFile(upath)
        pCount = dbAdmin.fetchPasswordCount(self, username)
        if(pCount and pCount[0] and pCount[0]["count"] == len(files)-1):
            pass
        else:
            return False

        pfCount = 0
        for ifile in range(1, len(files)):
            pf = os.path.join(credsBasePath, f'p{ifile}.txt')
            pwd = utilum.file.readFile(pf)
            creds = dbAdmin.fetchPasswordData(self, username, ifile)
            # print(username, ifile, creds)
            # print(creds)
            if(len(creds) == 1):
                pass
            else:
                return False
            creds = creds[0]

            passwordSalt = creds["passwordSalt"]
            passwordHashed = creds["passwordHashed"]
            # print(passwordSalt, passwordHashed)
            if(hashing.sha512(pwd+passwordSalt) == passwordHashed):
                pfCount += 1

        if(pfCount == len(files)-1):
            return True
        return False
    else:
        return False


def checkIat(iat, mins=8):
    now = datetime.datetime.now()
    diffSeconds = (now - iat).total_seconds()
    diffMins = diffSeconds / 60

    if(diffMins <= mins):
        return True
    return False

# 2) authorize token


def authorizeToken(self, token):
    status = False
    # valid for 20 transactions and 8 mins, until reset
    if("value" in self.token and self.token["value"] == token):
        if(self.token["count"] <= 20 and checkIat(self.token["iat"], 8)):
            self.token["count"] += 1
            status = True
    else:
        self.token = {}
    return status


def createCreds(self, username, passwordFiles):
    credsBasePath = self.config.credsBasePath
    if(utilum.file.isPathExist(credsBasePath) and os.path.isdir(credsBasePath)):
        # 1) username file: u.txt
        uf = os.path.join(credsBasePath, 'u.txt')
        utilum.file.createPath(uf)
        utilum.file.clearFile(uf)
        utilum.file.writeFile(uf, username)

        # 2) password files
        t16 = 2**16
        # t16 = 2**8
        lastPnumber = 2056
        for pnumber in range(1, passwordFiles+1):
            pf = os.path.join(credsBasePath, f'p{pnumber}.txt')
            utilum.file.createPath(pf)
            utilum.file.clearFile(pf)
            pwd = utilum.string.randomCharStream(t16, False)
            utilum.file.writeFile(
                pf, pwd)

            # pwd
            passwordSalt = utilum.string.randomNumberStream(8)
            passwordHashed = hashing.sha512(pwd + passwordSalt)
            try:
                dbAdmin.insertPasswordData(
                    self, pnumber, username, passwordSalt, passwordHashed)
            except:
                dbAdmin.updatePasswordData(
                    self, username, pnumber, passwordSalt, passwordHashed)
            lastPnumber = pnumber + 1

        # deleting extra password files/entries
        dbAdmin.deletePasswordData(self, lastPnumber)
        presentFiles = utilum.file.listDirPath(credsBasePath)
        for pnumber in range(lastPnumber, len(presentFiles)-1+1):
            pf = os.path.join(credsBasePath, f'p{pnumber}.txt')
            try:
                utilum.file.removeFile(pf)
            except:
                # temporily handled this way
                pass
        return True
    else:
        return False


def processCreds(self, username, passwordFiles):
    # 1) shredding current creds if exist
    if(authorize(self)):
        # a)
        show.showRunnerAll(self)
        # b) removing .enc files
        update.deleteAllEncStorage(self)
        return createCreds(self, username, passwordFiles)
    else:
        commited = db.fetchEncDataCommitted(self)
        if(len(commited) == 0):
            pass
        else:
            if(otp.passwordResetOtp(6)):
                # removing all remaining .enc259 files
                update.deleteAllEncStorage(self)
                pass
            else:
                return False

        return createCreds(self, username, passwordFiles)

# create


def createResetCreds(self, username, passwordFiles):
    passwordFiles = int(passwordFiles)
    # print("createResetCreds:debug:")
    return processCreds(self, username, passwordFiles)

#


def issueToken(origin):
    return {'origin': origin, 'count': 0, "value": utilum.string.randomCharStream(16, False), "iat": datetime.datetime.now()}


def authenticate(self, origin, byPassOtp=False):
    status = False
    token = ""
    # : DEBUG: for byPassOtp = true
    if(otp.sessionOtp(6, False)):
        status = True
        tokenInternal = issueToken(origin)
        self.token = tokenInternal
        token = tokenInternal["value"]
    else:
        status = False
    return {"status": status, "token": token}
