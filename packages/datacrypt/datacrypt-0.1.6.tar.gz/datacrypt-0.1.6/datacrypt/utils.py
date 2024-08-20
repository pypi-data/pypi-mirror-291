import sys
import instance
import os
CWD = os.getcwd()
sys.path.append(CWD)

if('datacrypt/datacrypt' in CWD):
    # assigning gibberish for safety, aka to avoid self-repo initialization
    CWD = '/HhX8vI72QKe8sit9Fz2L'


def getInstance():
    from config import config as configLocal

    basePath = "."
    if(configLocal and hasattr(configLocal, basePath)):
        basePath = configLocal.basePath

    DI = instance.Instance(basePath, configLocal)
    return DI
