import os.path

def createFolder(name):
    if not os.path.exists(name):
        os.makedirs(name)
    return name

homeFolder    = os.path.expanduser("~")

rootFolder    = createFolder(os.path.join(homeFolder, ".raireplay"))
dataFolder    = createFolder(os.path.join(rootFolder, "data"))

replayFolder  = createFolder(os.path.join(dataFolder, "replay"))
itemFolder    = createFolder(os.path.join(dataFolder, "items"))
pageFolder    = createFolder(os.path.join(dataFolder, "pages"))
demandFolder  = createFolder(os.path.join(dataFolder, "demand"))
juniorFolder  = createFolder(os.path.join(dataFolder, "junior"))
searchFolder  = createFolder(os.path.join(dataFolder, "search"))
tgFolder      = createFolder(os.path.join(dataFolder, "tg"))
mediasetFolder = createFolder(os.path.join(dataFolder, "mediaset"))
pluzzFolder   = createFolder(os.path.join(dataFolder, "pluzz"))
tf1Folder     = createFolder(os.path.join(dataFolder, "tf1"))
m6Folder      = createFolder(os.path.join(dataFolder, "m6"))

programFolder = createFolder(os.path.join(rootFolder, "programs"))
