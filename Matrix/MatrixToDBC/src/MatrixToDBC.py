import os
from ReadMatrix import *
from Version import *
import threading
import time
global progressBar
progressBar = {}

def isMatrixFile(file):
    supportFormatlist = ["xlsx", "xlsm", "xltx", "xltm"]

    return any(format in file for format in supportFormatlist if not file.startswith("~$"))

def getMatrixFile(path):
    files = os.listdir(path)
    matrixFile = [file for file in files if isMatrixFile(file)]

    return matrixFile

def creatDBCFile(matrixFile):
    DBCFileName = "WM" + "_" + getVersion() + "_" + matrixFile.split(".")[0]

    if os.path.exists(DBCFileName + ".dbc"):
        os.remove(DBCFileName + ".dbc")
    if os.path.exists(DBCFileName + ".ini"):
        os.remove(DBCFileName + ".ini")

    return open(DBCFileName + ".dbc", "x", encoding = "gbk")

def setDBCBlank(DBCFile, times):
    for loop in range(times):
        DBCFile.write("\n")

def setDBCVersion(DBCFile):
    DBCFile.write("VERSION \"%s\"\n" %(getVersion()))
    setDBCBlank(DBCFile, 2)
    global progressBar
    progressBar["completenessPercent"] = 5

def setDBCNS(DBCFile, matrixFile):
    NS = getMatrixNS(matrixFile)
    DBCFile.write("NS_ : \n")
    DBCFile.write("%s" %(NS))
    setDBCBlank(DBCFile, 1)
    global progressBar
    progressBar["completenessPercent"] = 10

def setDBCBS(DBCFile, matrixFile):
    BS = getMatrixBS(matrixFile)
    DBCFile.write("BS_ : \n")
    DBCFile.write("%s" %(BS))
    setDBCBlank(DBCFile, 1)
    global progressBar
    progressBar["completenessPercent"] = 15

def setDBCBU(DBCFile, matrixFile):
    BUS = getMatrixBUS(matrixFile)
    DBCFile.write("BU_ : ")
    DBCFile.write("%s" %(BUS))
    setDBCBlank(DBCFile, 2)
    global progressBar
    progressBar["completenessPercent"] = 25

def setDBCBOS(DBCFile, matrixFile):
    BOS = getMatrixBOS(matrixFile)
    DBCFile.write("%s" %(BOS))
    setDBCBlank(DBCFile, 2)
    global progressBar
    progressBar["completenessPercent"] = 50

def setDBCCMS(DBCFile, matrixFile):
    CMS = getMatrixCMS(matrixFile)
    DBCFile.write("%s" %(CMS))
    global progressBar
    progressBar["completenessPercent"] = 65

def setDBCBAS(DBCFile, matrixFile):
    BAS = getMatrixBAS(matrixFile)
    DBCFile.write("%s" %(BAS))
    global progressBar
    progressBar["completenessPercent"] = 85

def setDBCVAL(DBCFile, matrixFile):
    VAL = getMatrixVAL(matrixFile)
    DBCFile.write("%s" %(VAL))
    setDBCBlank(DBCFile, 1)
    global progressBar
    progressBar["completenessPercent"] = 100

def setProgressBar():
    global progressBar
    scale = 50
    while(True):
        completenessPercent = progressBar["completenessPercent"]

        finished = "*" * int((completenessPercent / 100 * scale))
        unfinished = "." * int((1 - completenessPercent / 100) * scale)
        timing = time.perf_counter() - progressBar["startTime"]

        print("\r{:^3.0f}%[{}->{}]{:.2f}s".\
            format(completenessPercent, finished, unfinished, timing),end = "")

        if completenessPercent == 100:
            print("")
            break

def initProgressBar():
    global progressBar
    progressBar["startTime"] = time.perf_counter()
    progressBar["completenessPercent"] = 0

    thread = threading.Thread(target = setProgressBar, name = "WM_DBCFileGenProBar")
    thread.start()

def matrixToDBCFile(matrixFile):
    DBCFile = creatDBCFile(matrixFile)
    print("Start to convert matrix file: %s" %(matrixFile))

    initProgressBar()

    setDBCVersion(DBCFile)
    setDBCNS(DBCFile, matrixFile)
    setDBCBS(DBCFile, matrixFile)
    setDBCBU(DBCFile, matrixFile)
    setDBCBOS(DBCFile, matrixFile)
    setDBCCMS(DBCFile, matrixFile)
    setDBCBAS(DBCFile, matrixFile)
    setDBCVAL(DBCFile, matrixFile)

    DBCFile.close()
    print("Generate DBC file successfully, file name: %s\n" %(DBCFile.name))


def main():
    print("DBC file generator tool version: %s\n" %getToolVersion())
    matrixFiles = getMatrixFile('.')

    if matrixFiles:
        print("Matrix file(s) in current directory: %s\n" %", ".join(matrixFile for matrixFile in matrixFiles))
        for matrixFile in matrixFiles:
            matrixToDBCFile(matrixFile)

        print("Complete with success!")
    else:
        print("There is no matrix file in current directory.")

    print("(Press any key to exit.)")
    input()

main()
