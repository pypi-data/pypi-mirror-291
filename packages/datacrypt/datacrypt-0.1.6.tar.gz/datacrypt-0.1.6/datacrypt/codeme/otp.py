import utilum
from . import uattributes


def deleteRecordOtp(optLen=4, byPass=False):
    if(byPass == False):
        try:
            otp = utilum.string.randomNumberStream(optLen)
            choice = input(
                f"\n{uattributes.colors.fg.red}Deleting is Risky!! {uattributes.colors.fg.lightgrey}\nEnter the OTP to Proceed {uattributes.colors.fg.yellow}{otp}: {uattributes.colors.fg.lightgrey}")
            if(choice == otp):
                return True
            else:
                print(f"\n{uattributes.colors.fg.lightgrey}OTP Incorrect!!")
                return False
        except:
            print(f"\n\n{uattributes.colors.fg.lightgrey}Deleting Aborted!!")
            return False
    else:
        return True


def initializeRecordOtp(optLen=4, byPass=False):
    if(byPass == False):
        try:
            otp = utilum.string.randomNumberStream(optLen)
            choice = input(
                f"\n{uattributes.colors.fg.red}Are you sure about Re-Initializing ??{uattributes.colors.fg.lightgrey}\nEnter the OTP to Proceed {uattributes.colors.fg.yellow}{otp}: {uattributes.colors.fg.lightgrey}")
            if(choice == otp):
                return True
            else:
                print(f"\n{uattributes.colors.fg.lightgrey}OTP Incorrect!!")
                return False
        except:
            print(
                f"\n\n{uattributes.colors.fg.lightgrey}Re-Initializing Aborted!!")
            return False
    else:
        return True


def purgeInitOtp(optLen=4, byPass=False):
    if(byPass == False):
        try:
            otp = utilum.string.randomNumberStream(optLen)
            choice = input(
                f"\n{uattributes.colors.fg.red}Are you sure about Purging Init[Make sure the files are in Un-Encrypted State] ??{uattributes.colors.fg.lightgrey}\nEnter the OTP to Proceed {uattributes.colors.fg.yellow}{otp}: {uattributes.colors.fg.lightgrey}")
            if(choice == otp):
                return True
            else:
                print(f"\n{uattributes.colors.fg.lightgrey}OTP Incorrect!!")
                return False
        except:
            print(
                f"\n\n{uattributes.colors.fg.lightgrey}Re-Initializing Aborted!!")
            return False
    else:
        return True


def passwordResetOtp(optLen=6, byPass=False):
    if(byPass == False):
        try:
            otp = utilum.string.randomNumberStream(optLen)
            choice = input(
                f"\n{uattributes.colors.fg.red}Are you sure about Password Creation/Resetting (Not all files are SHOWN, and You are UN-Authenticated currently).\nYou may loose file(s) data without authentication ??{uattributes.colors.fg.lightgrey}\nEnter the OTP to Proceed {uattributes.colors.fg.yellow}{otp}: {uattributes.colors.fg.lightgrey}")
            if(choice == otp):
                return True
            else:
                print(f"\n{uattributes.colors.fg.lightgrey}OTP Incorrect!!")
                return False
        except:
            print(
                f"\n\n{uattributes.colors.fg.lightgrey}Password Creation Aborted!!")
            return False
    else:
        return True


def sessionOtp(optLen, byPassOtp):
    if(byPassOtp == False):
        try:
            otp = utilum.string.randomNumberStream(optLen)
            choice = input(
                f"\n{uattributes.colors.fg.red}Are you sure about creating a Session ??{uattributes.colors.fg.lightgrey}\nEnter the OTP to Proceed {uattributes.colors.fg.yellow}{otp}: {uattributes.colors.fg.lightgrey}")
            if(choice == otp):
                return True
            else:
                print(f"\n{uattributes.colors.fg.lightgrey}OTP Incorrect!!")
                return False
        except:
            print(
                f"\n\n{uattributes.colors.fg.lightgrey}Session creation Aborted!!")
            return False
    else:
        return True
