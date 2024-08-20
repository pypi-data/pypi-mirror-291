import utilum
from . import hide
from . import update


def initializeIgnoreFile():
    utilum.system.shell("echo '*' > .gitignore")
    return True


def shreddIgnoreFile():
    utilum.system.shell("rm .gitignore")
    return True


def addAll(self): utilum.system.shell(f"git add {self.basePath}")


def commitRegular(): utilum.system.shell(
    'git commit -m "DataCrypt Regular Update"')


def pushOriginPasscode(self):
    utilum.system.shell(
        f"git push origin {self.config.gitBranch}")
    return True


def regularSafeProcess(self):
    # 1) Init for safety
    update.initializeEnc(self)
    # 2) Hide
    hideStatus = hide.hideRun(self, "extreme")
    # print("regularSafeProcess:hideStatus0", hideStatus)
    if(hideStatus == True):
        pass
    else:
        return False

    # print("regularSafeProcess:hideStatus1", hideStatus)
    addAll(self)
    commitRegular()
    pushOriginPasscode(self)
    # print("regularSafeProcess:hideStatus2", hideStatus)
    return True
