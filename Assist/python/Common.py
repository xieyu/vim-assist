import string
import shelve
import vim
import os
import sys
import fnmatch

class CommonUtil:
    @staticmethod
    def translatePattern(key_stroke):
        pat = key_stroke
        try:
            if pat[0] == "^":
                pat = pat[1:]
            else:
                pat = "*" + pat
            if pat[-1] == '$':
                pat = pat[:len(pat) - 1]
            else:
                pat = pat + "*"
        except:
            pat = "*"
        return pat

    @staticmethod
    def fileMatch(keystroke, filePath):
        fileName = os.path.basename(filePath)
        pat = CommonUtil.translatePattern(keystroke.lower())
        fileName = fileName.lower()
        return fnmatch.fnmatch(fileName, pat)

    @staticmethod
    def wordMatch(keystroke, content):
        pat = CommonUtil.translatePattern(keystroke.lower())
        return fnmatch.fnmatch(content.lower(), pat)

    @staticmethod
    def unique(fileIterms):
        ret = []
        for i in fileIterms:
            if i not in ret:
                ret.append(i)
        return ret

        
