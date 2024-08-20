import utilum
from . import show
from . import otp
from . import auth2

# allowed only in 100% show mode


def purgeInit(self):

    otpStatus = otp.purgeInitOtp()
    if(otpStatus == True):
        pass
    else:
        return False

    authStatus = auth2.authorize(self)
    if(authStatus == True):
        pass
    else:
        return False

    showStatus = show.showRunner(self, self.basePath)
    if(showStatus == True):
        pass
    else:
        return False

    print()
    print("Purging Database and Storage.... You may have to Re-Initialize to use encryption again.")
    print()
    utilum.system.shell(f'''rm -rf "{self.config.storageBasePath}"''')
    utilum.system.shell(f'''rm  "{self.config.databasePath}"''')
    return True
