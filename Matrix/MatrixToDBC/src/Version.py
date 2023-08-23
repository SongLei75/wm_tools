import datetime

def getOEM():
    return "Weltmeister"

def getProjectName():
    return "CentralComputePlatform"

def getDBCGenerateDate():
    return datetime.date.today()

def getDBCGenerateYear():
    return getDBCGenerateDate().year % 100

def getDBCGenerateMonth():
    return getDBCGenerateDate().month

def getDBCGenerateDay():
    return getDBCGenerateDate().day

def getToolVersion():
    return "100"

def getVersion():
    return str(datetime.date.today())

def getDetailVersion():
    content = ""
    company = "WM"
    author = "Lei.song"
    time = str(datetime.datetime.now().__format__('%Y-%m-%d %H:%M:%S'))

    content += "Author: %s-%s\n" %(company, author)
    content += "Tool version: %s\n" %getToolVersion()
    content += "DBC generate date: %s" %time

    return content

