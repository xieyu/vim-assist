
import subprocess
import re
import os
import shelve

from SearchIterm import CtagIterm
from Common import CommonUtil

class CtagsAssist:
    #public interface:
    @staticmethod
    def getCurrentFileTags():
        fileName = vim.current.buffer.name
        if fileName:
            output = CtagsAssist.ctags(fileName)
            return CtagsAssist.createTagCandidate(output)
        return []

    #private helper functions
    @staticmethod
    def createTagCandidate(output):
        result = []
        pattern = re.compile("(\S*)\s*(\S*)\s*(\d*)\s*(\S*)\s*(.*$)")
        for line in output.split("\n"):
            line = line.strip()
            if line:
                (symbol, symbolType, lineNumber, filePath, codeSnip) = pattern.search(line).groups()
                iterm = CtagIterm(name = symbol, path = filePath, lineNumber = lineNumber, codeSnip = codeSnip, symbolType = symbolType)
                result.append(iterm)
        return result

    @staticmethod
    def ctags(fileName):
        cmd = "ctags -x %s" % fileName
        process = subprocess.Popen(cmd, stdout = subprocess.PIPE, shell = True)
        output = process.stdout.read()
        del process
        return output

class CtagSearchBackend(ItermsFilter):
    def itermPassCheck(self, word, iterm):
        if word is "":
            return True
        if word[0] == '%':
            return CommonUtil.strokeMatch(word[1:], iterm.name)
        s = iterm.name.lower()
        return word in s

