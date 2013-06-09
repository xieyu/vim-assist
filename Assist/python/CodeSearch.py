import subprocess
import re
import os

import SearchBackend
#import it to avoid not found VimUi error, don't know how to fix it now.
import VimUi
from Candidate import TagCandidate

class CodeSearch:
    @staticmethod
    def instance():
        if not hasattr(CodeSearch, "_instance"):
            CodeSearch._instance = CodeSearch()
        return CodeSearch._instance

    def search(self, symbol):
        symbol = symbol.strip() or vim.eval('expand("<cword>")')
        prefix = "-n"
        if hasattr(self, "searchDir"):
            prefix = "-n -f %s" %(self.searchDir)
        cmdArg = "%s %s" % (prefix, symbol)
        output = self.makeSearch(cmdArg)
        candidates = self._createTagCandidate(output)
        SearchBackend.showSearchResult(candidates)

    def setSearchDir(self, dir):
        path = os.path.abspath(dir)
        self.searchDir = path

    def makeSearch(self, cmdArgs):
        csearch = os.path.expanduser(vim.eval("g:assist_csearch"))
        cmd = " ".join((csearch, cmdArgs))
        process = subprocess.Popen(cmd, stdout = subprocess.PIPE, shell=True)
        output, error = process.communicate()
        del process
        return output

    def makeIndex(self, dir):
        absPath = os.path.abspath(dir)
        cindex = os.path.expanduser(vim.eval("g:assist_cindex"))
        cmd = " ".join((cindex, absPath))
        subprocess.Popen(cmd, shell=True)

    def _createTagCandidate(self, output):
        result = []
        pattern = re.compile("([^ \t:]*):(\d*):(.*$)")
        for line in output.split("\n"):
            line = line.strip()
            if line:
                (filePath, row, codeSnip) = pattern.search(line).groups()
                candidate = TagCandidate(path = filePath, lineNumber = str(int(row) + 1), codeSnip = codeSnip.strip())
                result.append(candidate)
        return result
