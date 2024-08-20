import os
import sqlite3
import copier
import paramsHandling
from codeme import status


def folders():
    return "folder_datacrypt"


def files():
    return "files_datacrypt"


class Config:
    def __init__(self, basePath, customConfig):
        if(customConfig):
            self.customConfig = customConfig

        if(customConfig and customConfig.git and customConfig.git['branch']):
            self.gitBranch = customConfig.git['branch']
        else:
            self.gitBranch = 'main'

        # 1) Base Folder
        self.basePath = basePath
        basePathForJoining = self.basePath
        if(self.basePath == "."):
            basePathForJoining = ""
        self.encBasePath = os.path.join(basePathForJoining, '.enc259/')

        # 2) Storage
        self.storageBasePath = os.path.join(self.encBasePath, "storage/")
        self.storageGitKeepPath = os.path.join(
            self.storageBasePath, '.gitkeep')
        self.databasePath = os.path.join(self.encBasePath, "database.db")
        self.credsPath = os.path.join(self.encBasePath, 'creds.json')

        # Z) Others
        self.enc259IgnoredFiles = [
            self.databasePath,
            os.path.join(basePathForJoining, "config.py"),
            os.path.join(basePathForJoining, "Readme.md"),
            os.path.join(basePathForJoining, "runLocal.sh"),
        ]
        self.enc259IgnoredFolders = [
            self.encBasePath,
            os.path.join(basePathForJoining, ".git/"),
        ]
        self.customIgnoredFolders = [
            os.path.join(basePathForJoining, "GitHub_manager/"),
        ]
        self.customIgnoredFiles = [
            os.path.join(basePathForJoining, "main.py"),
            os.path.join(basePathForJoining, "zRunAllGit.sh"),
            os.path.join(basePathForJoining, "run.py"),
            os.path.join(basePathForJoining, "__init__.py"),
            os.path.join(basePathForJoining, ".gitignore")
        ]

        self.allIgnoredFiles = self.enc259IgnoredFiles + \
            self.customIgnoredFiles + customConfig.ignoredFiles
        self.allIgnoredFolders = self.enc259IgnoredFolders + \
            self.customIgnoredFolders + customConfig.ignoredFolders

        self.ignoredFilesRegExp = []
        self.allIgnoredFilesRegExp = self.ignoredFilesRegExp + \
            customConfig.ignoredFilesRegExp

        self.ignoredFoldersRegExp = [".git", '.enc259']
        self.allIgnoredFoldersRegExp = self.ignoredFoldersRegExp + \
            customConfig.ignoredFoldersRegExp

        self.credsBasePath = customConfig.credsBasePath

    def setCredentials(self, creds):
        self.creds = creds


class Connection:
    def __init__(self, databasePath):
        self.databasePath = databasePath
        self.connection = sqlite3.connect(
            self.databasePath, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row


class Instance:
    def __init__(self, basePath=".", customConfig={}):

        # Basic Params
        self.basePath = basePath

        # Modules1: config
        self.config = Config(basePath, customConfig)

        # Initializations type-1
        copier.run(self)

        # Modules2: connections
        self.connections = Connection(self.config.databasePath)

        # Initializations type-2
        copier.run2(self)

        # Hashdict initialization
        self.hashDict, _ = status.statusEnc(self, True, [])

        self.token = {}

    def printBasePath(self):
        print(self.basePath)

    def run(self, param1=None, param2=None, param3=None, param4=None, param5=None):
        return paramsHandling.run(self, param1, param2, param3, param4, param5)

    def authenticate(self, origin):
        return paramsHandling.authenticate(self, origin)
