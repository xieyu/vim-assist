import subprocess
import re
import os
import vim
import VimUi
import SearchBackend

from StoreManager import StoreManager
from Candidate import FileCandidate
from Candidate import Candidate
from Common import CommonUtil

class Locate:
    @staticmethod
    def instance():
        if not hasattr(Locate, "_instance"):
            Locate._instance = Locate()
        return Locate._instance

    def __init__(self):
        self.storeKey = "LcdHistory"
        self.editHistoryKey = "editHistory"

    def search(self, symbol):
        candidates = getattr(self, "cachedCandidates", self.makeIndex())
        matchedCandidates = []
        for candidate in candidates:
                if CommonUtil.fileMatch(symbol, candidate.path):
                    matchedCandidates.append(candidate)

        if len(matchedCandidates) == 1:
            matchedCandidates[0].onAction("close")
        else:
            SearchBackend.showSearchResult(matchedCandidates)

    def searchBuffer(self, symbol):
        candidates = [FileCandidate(buffer.name) for buffer in vim.buffers if buffer.name and symbol in buffer.name]
        if len(candidates) == 1:
            candidates[0].onAction("close")
        SearchBackend.showSearchResult(candidates)

    def switchHeadAndImpl(self):
        '''
        switch between [.h|.hpp] with [.cpp|.m|.c|.cc]
        '''
        try:
            filename = os.path.basename(vim.current.buffer.name)
        except:
            return
        s = []
        extentions = [".cpp", ".c", ".cc", ".m"]
        if re.search("\.(h|hpp)$", filename):
            for ext in extentions:
                s.append(re.sub("\.(h|hpp)$", ext, filename))
        elif re.search("\.(c|cpp|cc|m)$", filename):
            s.append(re.sub("\.(c|cpp|cc)$", ".h", filename))
            s.append(re.sub("\.(c|cpp|cc)$", ".hpp", filename))

        candidates = getattr(self, "cachedCandidates", self.makeIndex())
        matchedCandidates = []
        for candidate in candidates:
            for pattern in s:
                if CommonUtil.fileMatch(pattern + "$", candidate.path):
                    matchedCandidates.append(candidate)
                    break
        if len(matchedCandidates) == 1:
            matchedCandidates[0].onAction("close")
        else:
            SearchBackend.showSearchResult(matchedCandidates)

    def makeIndex(self):
        path = getattr(self, "searchDir", os.getcwd())
        candidates = []
        for root, dirs, files in os.walk(path):
            for file in files:
                filePath = os.path.join(root, file)
                if not self.isIgnorePath(filePath):
                    candidate = FileCandidate(filePath)
                    candidates.append(candidate)
        self.cachedCandidates = candidates
        return self.cachedCandidates

    def isIgnorePath(self, path):
        def isReIgnore(ignorePatterns, items):
            ignorePattern = [re.compile(rawPattern) for rawPattern in ignorePatterns]
            for pattern in ignorePattern:
                for item in items:
                    if pattern.search(item):
                        return True
            return False

        ignoreDirs = ["^.git$"]
        if isReIgnore(ignoreDirs, path.split(os.sep)):
            return True

        ignoreFilePatterns =[".pyc$", ".o$"]
        if isReIgnore(ignoreFilePatterns, [os.path.basename(path)]):
            return True

        return False


    def setSearchDir(self, dirPath):
        if dirPath is "":
            self.showCdHistory()
        elif not os.path.exists(os.path.abspath(dirPath)):
            self.showFilterCdHistory(dirPath)
        else:
            dirPath = os.path.abspath(dirPath)
            self.addToCdHistory(dirPath)
            self.doSetSearchDir(dirPath)

    def doSetSearchDir(self, dir):
        path = os.path.abspath(dir)
        self.searchDir = path
        self.makeIndex()

    def showEditHistory(self):
        editHistory = StoreManager.load(self.editHistoryKey)
        editHistory.reverse()
        if editHistory:
            candidates = [FileCandidate(str(path)) for path in editHistory]
            SearchBackend.showSearchResult(candidates)
        else:
            print "empty history"

    def addToEditHistory(self):
        filePath = vim.current.buffer.name
        if not os.path.exists(filePath):
            return

        history = StoreManager.load(self.editHistoryKey)
        for i, historyFileName in enumerate(history):
            if historyFileName == filePath:
                del history[i]
                break

        history.append(filePath)
        StoreManager.save(self.editHistoryKey , history)

    def editHistory(self):
        StoreManager.editSavedValue(self.editHistoryKey);


    def showCdHistory(self):
        history = StoreManager.load(self.storeKey)
        candidates = [LocateCdCandidate(str(path)) for path in history]
        SearchBackend.showSearchResult(candidates, filterCheck=locatefilterCheck)

    def showFilterCdHistory(self, symbol):
        history = StoreManager.load(self.storeKey)
        candidates = [LocateCdCandidate(str(path)) for path in history if symbol in path]
        SearchBackend.showSearchResult(candidates, filterCheck=locatefilterCheck)

    def addToCdHistory(self, dirPath):
        history = StoreManager.load(self.storeKey)
        if dirPath not in history:
            history.append(dirPath)
        StoreManager.save(self.storeKey, history)

    def editCdHistory(self):
        StoreManager.editSavedValue(self.storeKey)


class LocateCdCandidate(Candidate):
    def __init__(self, dirPath):
        self.dirPath = dirPath

    def displayText(self):
        return self.dirPath

    def onAction(self, action):
        Locate.instance().doSetSearchDir(self.dirPath)

        if action =="close":
            return True

        if action == "preview":
            return False

def locatefilterCheck(word, candidate):
    return word in candidate.dirPath
