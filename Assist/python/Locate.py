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
