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

class SettingManager:
    walle_home = vim.eval("g:assistHome")
    @staticmethod
    def getStoreDir():
        path = os.path.join(SettingManager.walle_home, "config/")
        if not os.path.exists(path):
            os.mkdir(path)
        return path

    @staticmethod
    def getBrowser():
        s = "g:browser"
        browser = "opera"
        #if vim.eval('exists("%s")' % s):
        #    browser = vim.eval('%s' % s)
        #else:
        #    browser = "opera"
        return browser


def initVimAssist():
    assistHome = vim.eval("g:assistHome")
    sys.path.append(os.path.abspath(assistHome + "python"))

initVimAssist()
