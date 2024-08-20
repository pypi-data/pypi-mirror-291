import hashlib
from dirhash import dirhash


def sha512(stream):
    result = hashlib.sha512(stream.encode())
    return str(result.hexdigest())


# hashing for file
def hexxod(fileName):
    # BUF_SIZE is totally arbitrary, change for your app!
    BUF_SIZE = 65536  # lets read stuff in 64kb chunks!

    md5 = hashlib.md5()
    sha1 = hashlib.sha1()

    with open(fileName, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            md5.update(data)
            sha1.update(data)

    return format(md5.hexdigest()), format(sha1.hexdigest())


# hashing for folder
def hexxodFolder(folderPath):
    try:
        dir_md5 = dirhash(folderPath, "md5")
        return dir_md5
    except:
        return -1


# '''Sample Runnings'''
# "scripts/temp1.txt"
# md, sh = hexxod("scripts/temp1.txt")
# print(md)
# print(sh)

# md1, sh1 = hexxod("scripts/t1.tar.xz")
# md2, sh2 = hexxod("scripts/t2.tar.xz")
# md3 = hexxodFolder("scripts/t3/")
# md4 = hexxodFolder("scripts/t4/")

# print(md1)
# print(md2)
# print(md3)
# print(md4)

# md1, sh1 = hexxod("scripts/adsense.txt")
# md2, sh2 = hexxod("scripts/o1.txt")
# print(md1)
# print(md2)
