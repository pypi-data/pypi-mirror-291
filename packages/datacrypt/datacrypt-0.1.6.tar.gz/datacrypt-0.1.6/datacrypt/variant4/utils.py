import utilum

def folderEncrypt(folderPath, password):
    folderPathClean = folderPath
    if(folderPathClean[-1] == "/"): folderPathClean = folderPathClean[:-1]
    utilum.system.shell(f"cd {folderPathClean} && zip -P {password} -r 'src.zip' 'src'")
    return

def folderDecrypt(folderPath, password):
    folderPathClean = folderPath
    if(folderPathClean[-1] == "/"): folderPathClean = folderPathClean[:-1]
    utilum.system.shell(f"cd {folderPathClean} && unzip -P {password} 'src.zip'")
    return
