from importlib.resources import path
import os
import utilum
import copy


class Creds:
    def __init__(self, username, passwords):
        self.username = username
        self.passwords = passwords
        passwordsR = copy.deepcopy(passwords)
        passwordsR.reverse()
        self.passwordsReverse = passwordsR


def getCreds(self):
    credsBasePath = self.config.credsBasePath
    allFiles = utilum.file.listDirPath(credsBasePath)
    upath = os.path.join(credsBasePath, 'u.txt')
    username = utilum.file.readFile(upath)
    passwords = []

    for ifile in range(1, len(allFiles)):
        pf = os.path.join(credsBasePath, f'p{ifile}.txt')
        pwd = utilum.file.readFile(pf)
        passwords.append(pwd)

    return Creds(username, passwords)


def stringContainFromList(input_string, input_list):
    for il in input_list:
        if(il in input_string):
            return True
        else:
            continue
    return False


def listDirPathSlashFiltered(self, input_path):
    paths = []
    input_path_mod = input_path
    if(input_path_mod == "."):
        input_path_mod = ""
    for f in os.listdir(input_path):
        if(os.path.isdir(input_path_mod+f) == True):
            if(input_path_mod+f+"/" in self.config.allIgnoredFolders):
                continue
            paths.append(sanitizePath(self, input_path_mod+f+"/"))
        else:
            filePath = (input_path_mod+f)
            if(filePath in self.config.allIgnoredFiles or filePath[-7:] == ".enc259" or filePath[-9:] == ".name.txt"):
                continue
            paths.append(sanitizePath(self, filePath))
    return paths


def checkIfPathShouldBeIgnored(self, path):
    # print("checkIfPathShouldBeIgnored: ", path, path in self.config.allIgnoredFolders,
    #   stringContainFromList(path, self.config.allIgnoredFoldersRegExp))
    if(os.path.isfile(path) and (path in self.config.allIgnoredFiles or stringContainFromList(path, self.config.allIgnoredFilesRegExp))):
        return True
    elif(os.path.isdir(path) and (path in self.config.allIgnoredFolders or stringContainFromList(path, self.config.allIgnoredFoldersRegExp))):
        return True
    return False


def checkIfPathAndEpShouldBeIgnored(self, path):
    # Path and Encrypted Path
    if(checkIfPathShouldBeIgnored(self, path) or (path[-7:] == ".enc259" and path[-9:] != ".name.txt")):
        return True
    return False


def bfsTraversal(self, start_path):
    def deepBfs(paths, allFiles):
        for p in paths:
            if(os.path.isdir(p) == True):
                if(checkIfPathShouldBeIgnored(self, p)):
                    continue
                else:
                    files = listDirPathSlashFiltered(p)
                    allFiles = deepBfs(files, allFiles)
            else:
                if(checkIfPathShouldBeIgnored(self, p)):
                    continue
                else:
                    allFiles.append(p)
        return allFiles
    allFiles = []
    allFiles = deepBfs([start_path], allFiles)
    return allFiles


def sanitizePath(self, pathHere):
    if(pathHere == "."):
        return pathHere
    if(os.path.isdir(pathHere)):
        if(pathHere[-1] != "/"):
            return pathHere + "/"
        else:
            return pathHere
    elif(os.path.isfile(pathHere)):
        if(pathHere[-1] == "/"):
            return pathHere[:-1]
        else:
            return pathHere
    else:
        return pathHere

# checks for existence of corresponding encrypted file


def associatedPlaceHolderPath(self, path):
    path = path + ".name.txt"
    return path


def associatedEncryptedFile(self, filePath):
    if("/" in filePath):
        rev = filePath[::-1]
        ri = len(rev) - rev.index("/")
    else:
        ri = 0
    first = filePath[:ri]
    last = filePath[ri:]

    possibleEncryptedFilePath = os.path.join(
        self.config.storageBasePath, f"{first}.{last}.enc259")
    return possibleEncryptedFilePath


def checkCorrespondingEncryptedFile(self, filePath):
    possibleEncryptedFilePath = associatedEncryptedFile(self, filePath)

    if(utilum.file.isPathExist(possibleEncryptedFilePath)):
        return True
    else:
        return False


def shreddAssociatedEncryptedFile(self, filePath):
    if(checkCorrespondingEncryptedFile(self, filePath)):
        utilum.file.removeFile(associatedEncryptedFile(self, filePath))
    return None
