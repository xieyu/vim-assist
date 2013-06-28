
import subprocess
import re
import os
import shelve

from Candidate import CtagCandidate
from Common import CommonUtil

class Ctags:
    @staticmethod
    def instance():
        if not hasattr(Ctags, "_instance"):
            Ctags._instance = Ctags();
        return Ctags._instance

    def searchCurrentFile(self, symbol):
        candidates = self._getCurrentFileTags()
        SearchBackend.showSearchResult(candidates, self._candidateFilterCheck)

    def _getCurrentFileTags(self):
        fileName = vim.current.buffer.name
        if fileName:
            output = self._makeCtags(fileName)
            return self._createTagCandidate(output)
        return []

    def _createTagCandidate(self, output):
        result = []
        pattern = re.compile("(\S*)\s*(\S*)\s*(\d*)\s*(\S*)\s*(.*$)")
        for line in output.split("\n"):
            line = line.strip()
            if line:
                (symbol, symbolType, lineNumber, filePath, codeSnip) = pattern.search(line).groups()
                iterm = CtagCandidate(symbol = symbol, path = filePath, lineNumber = lineNumber, codeSnip = codeSnip, symbolType = symbolType)
                result.append(iterm)
        return result

    def _makeCtags(self, fileName):
        cmd = "ctags -x %s" % fileName
        process = subprocess.Popen(cmd, stdout = subprocess.PIPE, shell = True)
        output = process.stdout.read()
        del process
        return output

    def _candidateFilterCheck(self, word, candidate):
        return CommonUtil.wordMatch(word, candidate.symbol)

