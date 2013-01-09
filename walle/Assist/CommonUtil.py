import string
import shelve
import vim
import os
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

class SettingManager:
    walle_home = vim.eval("g:walle_home")
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

def myAssert(condition, message=""):
    if condition:
        print message, "pass"
    else:
        print message, "fail"

if __name__=="__main__":
    myAssert(CommonUtil.fileStrokeMatch("hwd", "hello world"))
    myAssert(CommonUtil.fileStrokeMatch("oWd", "hello world"))
