import utilum
from . import uattributes


# 1) Hide
def folderUpdate(folderPath, password, encList, changeList):
    file_list_path = utilum.file.folderTraversal(folderPath)

    # folder encryption
    folder_list_path = utilum.file.folderTraversalFolders(folderPath)
    level1FolderList = []
    for flp in folder_list_path:
        flpDeep = utilum.file.folderTraversalFolders(flp)
        flpDeepFiles = utilum.file.folderTraversal(flp)
        if(len(flpDeep) == 1 and utilum.strings.stringContainFromList(".enc259", flpDeepFiles) == False):
            level1FolderList.append(flp)
            encList.append(flp)

    for ilfl, lfl in enumerate(level1FolderList):
        utilum.system.shell(f'''tar -czvf "{lfl}.tar.gz" "{lfl}"''')
        utilum.system.shell(
            f'''openssl aes-256-cbc -a -salt -in "{lfl}.tar.gz" -out "{lfl}.tar.gz.enc259" -pbkdf2 -k {password} > .no-print.txt''')
        utilum.system.shell('''rm .no-print.txt''')
        utilum.system.shell(f'''rm "{lfl}.tar.gz"''')
        utilum.system.shell(f'''rm -rf "{lfl}"''')

    # file encryption
    file_list_path = utilum.file.folderTraversal(folderPath)
    for iflp, flp in enumerate(file_list_path):
        if(flp[-7:] != ".enc259"):
            encList.append(flp)

            utilum.system.shell(
                f'''openssl aes-256-cbc -a -salt -in "{flp}" -out "{flp}.enc259" -pbkdf2 -k {password} > .no-print.txt''')
            utilum.system.shell('''rm .no-print.txt''')
            utilum.system.shell(f'''rm "{flp}"''')

    return encList, changeList


# 2) Show
def folderShow(folderPath, password, encList, changeList):

    file_list_path = utilum.file.folderTraversal(folderPath)

    for iflp, flp in enumerate(file_list_path):
        if(flp[-7:] == ".enc259"):
            print(
                f"{uattributes.bcolors.OKGREEN} Showing, ({iflp+1}/{len(file_list_path)}): {flp}")
            changeList.append(flp)
            flpClean = flp[:-7]
            utilum.system.shell(
                f'''openssl aes-256-cbc -d -a -in "{flp}" -out "{flpClean}" -pbkdf2 -k {password}''')
            if(flpClean[-7:] == ".tar.gz"):
                utilum.system.shell(f'''tar -xf "{flpClean}"''')
                utilum.system.shell(f'''rm "{flpClean}"''')

    return encList, changeList
