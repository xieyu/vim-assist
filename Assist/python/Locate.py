import subprocess
import re
import os
import vim
import VimUi
import SearchBackend

from Candidate import FileCandidate 
from Common import CommonUtil

class Locate:
    @staticmethod
    def instance():
        if not hasattr(Locate, "_instance"):
            Locate._instance = Locate()
        return Locate._instance

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

    def setSearchDir(self, dir):
        path = os.path.abspath(dir)
        self.searchDir = path
        self.makeIndex()

    def makeIndex(self):
        path = getattr(self, "searchDir", os.getcwd())
        candidates = []
        for root, dirs, files in os.walk(path):
            for file in files:
                filePath = os.path.join(root, file)
                candidate = FileCandidate(filePath)
                candidates.append(candidate)
        self.cachedCandidates = candidates
        return self.cachedCandidates
