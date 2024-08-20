# general
import sys
import os
import pathlib
import time

# local
import utils

# cmd: `datacrypt server` inside the desired directory
CWD = utils.CWD
PATH_HERE = pathlib.Path(__file__).parent.resolve()
PARENT_PATH_HERE = pathlib.Path(__file__).parent.parent.resolve()
PUBLIC_DIR_PATH = directory = os.path.join(PATH_HERE, "web/public")
STATIC_DIR_PATH = directory = os.path.join(PATH_HERE, "web/static")
TEMPLATES_DIR_PATH = directory = os.path.join(PATH_HERE, "web/templates")
FAVICON_PATH = os.path.join(PUBLIC_DIR_PATH, 'favicon.ico')
MANIFEST_PATH = os.path.join(PUBLIC_DIR_PATH, 'manifest.json')
sys.path.append(CWD)


# DI instance
DI = None


def mainlet():
    global DI
    if(DI == None):
        DI = utils.getInstance()
    else:
        pass


if __name__ == "__main__":
    mainlet()
    count = 0
    while(True):
        print()
        print("Count:", count,
              f" [Interval:{DI.config.customConfig.commitInterval}]")
        print("<git>--------------**--------------")
        DI.run('git', 'regular')
        count += 1
        print("</git>--------------**--------------")
        print()
        print()
        time.sleep(DI.config.customConfig.commitInterval)
