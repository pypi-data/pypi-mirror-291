from . import uattributes
from . import db


def statusEnc(self, noPrint=False, printArenaList=[], relaxed=False):
    dataDict = {}
    # print("relaxed: ", relaxed)
    records = db.fetchEncData(self, None, relaxed)
    recordsClean = []

    for row in records:
        path = row["path"]
        dataDict[path] = row

        printablePath = path
        recordsClean.append(
            {'path': printablePath, 'arena': row["arena"], 'type': row['type']})
        if(noPrint == False):
            if(len(printArenaList) == 0 or row["arena"] in printArenaList):
                print(
                    f'{uattributes.statusColor[row["arena"]]}[{row["arena"]}]: {uattributes.colors.fg.lightgrey}{printablePath}')
    return dataDict, recordsClean
