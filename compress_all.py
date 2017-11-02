import os
from subprocess import call

CMD = "7z a secure.7z * -pTEST"
PASSWD = "TEST"

fileNames = os.listdir('.')
fileNames = filter(lambda x: not x.startswith('.'), fileNames)

for fName in fileNames:
    archiveName = fName.split('.')[0] + ".archive"
    print "Compressing {} as {}...".format(fName, archiveName)
    call(["7z", "a", archiveName, fName, "-p" + PASSWD])

