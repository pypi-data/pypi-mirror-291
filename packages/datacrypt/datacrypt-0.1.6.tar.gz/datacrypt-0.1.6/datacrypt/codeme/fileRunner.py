import utilum
import os


# 1) Encrypt
def fileEncrypt(self, filePath, passwords):

    if("/" in filePath):
        rev = filePath[::-1]
        ri = len(rev) - rev.index("/")
    else:
        ri = 0
    first = filePath[:ri]
    last = filePath[ri:]

    encryptedFile = os.path.join(
        self.config.storageBasePath, f"{first}.{last}.enc259")
    utilum.file.createPath(encryptedFile)

    ####
    utilum.system.shell(
        f'''openssl aes-256-cbc -a -salt -in "{filePath}" -out "{encryptedFile}-1" -pbkdf2 -k "{passwords[-1]}" > .no-print.txt''')

    for irpwd, rpwd in enumerate(passwords[1:-1]):
        utilum.system.shell(
            f'''openssl aes-256-cbc -a -salt -in "{encryptedFile}-{irpwd+1}" -out "{encryptedFile}-{irpwd+2}" -pbkdf2 -k "{rpwd}" > .no-print.txt''')
        utilum.system.shell(f'''rm "{encryptedFile}-{irpwd+1}"''')

    utilum.system.shell(
        f'''openssl aes-256-cbc -a -salt -in "{encryptedFile}-{len(passwords)-1}" -out "{encryptedFile}" -pbkdf2 -k "{passwords[-1]}" > .no-print.txt''')
    utilum.system.shell(f'''rm "{encryptedFile}-{len(passwords)-1}"''')
    ####

    utilum.system.shell('''rm .no-print.txt''')

    nameFile = f"{filePath}.name.txt"
    utilum.system.shell(f'''touch "{nameFile}"''')
    utilum.system.shell(f'''rm "{filePath}"''')
    return None


# 2) Show --------------------------------
def fileShow(self, filePath, passwords):

    if("/" in filePath):
        rev = filePath[::-1]
        ri = len(rev) - rev.index("/")
    else:
        ri = 0
    first = filePath[:ri]
    last = filePath[ri:]

    encryptedFile = os.path.join(
        self.config.storageBasePath, f"{first}.{last}.enc259")

    ####
    utilum.system.shell(
        f'''openssl aes-256-cbc -d -a -in "{encryptedFile}" -out "{filePath}-1" -pbkdf2 -k "{passwords[0]}"''')

    for irpwd, rpwd in enumerate(passwords[1:-1]):
        utilum.system.shell(
            f'''openssl aes-256-cbc -d -a -in "{filePath}-{irpwd+1}" -out "{filePath}-{irpwd+2}" -pbkdf2 -k "{rpwd}"''')
        utilum.system.shell(f'''rm "{filePath}-{irpwd+1}"''')

    utilum.system.shell(
        f'''openssl aes-256-cbc -d -a -in "{filePath}-{len(passwords)-1}" -out "{filePath}" -pbkdf2 -k "{passwords[0]}"''')
    utilum.system.shell(f'''rm "{filePath}-{len(passwords)-1}"''')
    ####

    if(utilum.file.isPathExist(f'''{filePath}.name.txt''')):
        utilum.system.shell(f'''rm "{filePath}.name.txt"''')
    return None


def shreddFile(self, filePath):
    nameFile = f'''{filePath}.name.txt'''
    utilum.system.shell(f'''touch "{nameFile}"''')
    utilum.system.shell(f'''rm "{filePath}"''')
