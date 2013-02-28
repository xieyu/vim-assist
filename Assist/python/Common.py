import string
import shelve
import vim
import os
import sys

class CommonUtil:
    @staticmethod
    def strokeMatch(key_stroke, filePath):
        index = 0
        s = filePath.lower()
        strokes = key_stroke.lower()
        for key in strokes:
            index = string.find(s, key, index)
            if index == -1:
                return False
        return True

    @staticmethod
    def fileStrokeMatch(key_stroke, filePath):
        if '/' in key_stroke:
            return CommonUtil.strokeMatch(key_stroke, filePath)
        else:
            return CommonUtil.strokeMatch(key_stroke, os.path.basename(filePath))
    @staticmethod
    def wordStrokeMatch(key_stroke, codeline):
        words = codeline.split(" ")
        for w in words:
            if CommonUtil.strokeMatch(key_stroke, w):
                return True
        return False

class SettingManager:
    walle_home = vim.eval("g:assistHome")
    configFile= os.path.join(walle_home, "config/shelvedb")
    @staticmethod
    def save(key, value):
        d = shelve.open(SettingManager.configFile)
        d[key] = value
        d.close()

    @staticmethod
    def get(key):
        d = shelve.open(SettingManager.configFile)
        value = d.has_key(key) and  d[key] or []
        d.close()
        return value

    @staticmethod
    def tmpfile(key):
        filePath = os.path.join(SettingManager.walle_home, "config/tmp_%s" % key)
        return filePath

def initVimAssist():
    assistHome = vim.eval("g:assistHome")
    sys.path.append(os.path.abspath(assistHome + "python"))

initVimAssist()
