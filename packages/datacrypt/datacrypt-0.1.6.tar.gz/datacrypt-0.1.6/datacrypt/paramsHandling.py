from codeme import hide
from codeme import admin
from codeme import show
from codeme import update
from codeme import status
from codeme import git
from codeme import auth2


def adminHandling(self, param2, param3, param4, param5):
    if(param2 == "create-reset-creds"):
        return admin.auth2.createResetCreds(self, param3, param4)
    elif(param2 == "authorize"):
        return auth2.authorizeToken(self, param3) and admin.auth2.authorize(self)
    else:
        print("Invalid Parameter Format")


def hideHandling(self, param2):
    if(param2 == "normal"):
        hide.hideRun(self, "normal")
    elif(param2 == "hard"):
        hide.hideRun(self, "hard")
    elif(param2 == "extreme" or param2 == "all"):
        return hide.hideRun(self, "extreme")
    else:
        print("Invalid Parameter Format")


def showHandling(self, param2):
    if(param2 == "." or param2 == "all"):
        show.showRunnerAll(self)
    elif(len(param2) > 0):
        show.showRunner(self, param2)
    else:
        print("Invalid Parameter Format")


def gitHandling(self, param2):
    if(param2 == "regular"):
        return git.regularSafeProcess(self)
    else:
        print("Invalid Parameter Format")
        return False


def statusHandling(self):
    dataDict, records = status.statusEnc(self, noPrint=True)
    return records


def handleSingleParam(self, param1):
    if(param1 == 'status'):
        return statusHandling(self)
    elif(param1 == 'init'):
        return update.initializeEnc(self)
    else:
        print("Invalid Parameter1 Format")
        return False


def handleDoubleParam(self, param1, param2):
    if(param1 == "hide"):
        return hideHandling(self, param2)
    elif(param1 == 'show'):
        showHandling(self, param2)
    elif(param1 == 'git'):
        return gitHandling(self, param2)
    else:
        print("Invalid Parameter1 Format")


def handleQuintupleParam(self, param1, param2, param3, param4, param5):
    if(param1 == 'admin'):
        return adminHandling(self, param2, param3, param4, param5)
    else:
        print("Invalid Parameter1 Format")
        return False


def run(self, param1, param2, param3, param4, param5):
    if(param1 is not None and param2 is None and param3 is None):
        # Single Params Handling
        return handleSingleParam(self, param1)
    if(param1 is not None and param2 is not None and param3 is None):
        # Double Params Handling
        return handleDoubleParam(self, param1, param2)
    elif(param1 is not None and param2 is not None and param3 is not None and param4 is not None and param5 is not None):
        # Triple Params Handling
        return handleQuintupleParam(self, param1, param2, param3, param4, param5)

# alias credshow="python3 .enc259/run.py show $1"
# alias credsave="python3 .enc259/run.py git regular"


def authenticate(self, origin):
    return auth2.authenticate(self, origin)
