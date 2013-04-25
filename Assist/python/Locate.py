import subprocess
import re
import os
import hashlib
import vim

#from Common import CommonUtil
#from SearchBackend import SearchBackend

class LocateFile(SearchBackend):
    @staticmethod
    def startSearch(pattern):
        backend = LocateFile()
        window = SearchWindow(backend)
        window.show()

    def __init__(self):
        #self.pattern  = pattern
        self.searchIterms = []

    def search(self, word):
        ret = []
        countLimit = 30
        for iterm in self.searchIterms:
            if CommonUtil.fileMatch(word, iterm.getPath()):
                countLimit = countLimit - 1
                if countLimit < 0:
                    break
                ret.append(iterm)
        return ret

    def prepare(self):
        buffers = self.getBufferIterms()
        history = HistoryManager.getHistoryIterms()
        self.searchIterms = CommonUtil.unique(buffers  + history)

    def getInitDisplayIterms(self):
        return self.searchIterms

    def getBufferIterms(self):
        ret = []
        for buffer in vim.buffers:
            if buffer.name:
                ret.append(FileIterm(buffer.name))
        return ret

        
class LocateDirManager:
    storeKey = "locateDirs.json"
    @staticmethod
    def addLocateDir(workdir):
        p = os.path.expandvars(os.path.expanduser(workdir))
        if os.path.exists(p):
            paths = Locate.getLocateDirs()
            if p not in paths:
                paths.append(p)
                LocateDirManager.save(LocateDirManager.workdir, paths)

    @staticmethod
    def setWorkdir(path):
        path = os.path.expandvars(os.path.expanduser(path))
        if os.path.exists(path):
            LocateDirManager.addLocateDir(path)
            LocateDirManager.workdir = path
            LocateDirManager.save(LocateDirManager.workdir, paths)

    @staticmethod
    def edit():
        SettingManager.editSavedValue(Locate.storeKey)

    @staticmethod
    def getLocateDirs():
        return [str(b) for b in SettingManager.load(Locate.storekey)["paths"]]

    @staticmethod
    def getWorkdir():
        return LocateDirManager.workdir

    @staticmethod
    def save(workdir, paths):
        SettingManager.save(Locate.storeKey, {"workdir": workdir, "paths" :paths})

#class LocateFileIndex:
#    workdir = None
#    fileIterms = []
#    needReloadIndex = False
#    @staticmethod
#    def getFileIterms(pattern):
#        if LocateFile.needReloadIndex:
#            filePaths = SettingManager.load(LocateFile.getStoreKey(LocateFile.workdir))
#            LocateFile.fileIterms =[FileIterm(str(filePath)) for filePath in filePaths]
#            LocateFile.needReloadIndex = False
#
#        if pattern:
#            return [fileIterm for fileIterm in LocateFile.fileIterms if
#                    CommonUtil.fileMatch(pattern, fileIterm.getPath())]
#        else:
#            return LocateFile.fileIterms
#
#    @staticmethod
#    def updateIndex():
#        for path in Locate.getLocateDirs():
#            LocateDirManager.updateIndexForPath(path)
#
#    @staticmethod
#    def updateIndexForPath(path):
#        #TODO:make it multi process
#        result = []
#        storeKey = LocateFile.getStoreKey(path)
#        for root, dirs, files in os.walk(path):
#            for filePath in files:
#                filePath = os.path.join(root, filePath)
#                result.append(filePath)
#        SettingManager.save(storeKey, result)
#
#    @staticmethod
#    def setWorkdir(workdir):
#        if os.path.exists(workdir):
#            LocateFile.updateIndexForPath(workdir)
#            LocateFile.workdir = workdir
#            LocateFile.needReloadIndex = True
#        else:
#            print "%s is not exists"
#
#    @staticmethod
#    def getStoreKey(path):
#        return "file_index_%s_%s" %(os.path.basename(path), hashlib.md5(path).hexdigest())
#
#
#
#class LocateSymbol:
#    @staticmethod
#    def getTagIterms(symbol):
#        pass
