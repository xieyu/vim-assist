import string
import vim
import os
import sys
import json

class SettingManager:
    walle_home = vim.eval("g:assistHome")
    @staticmethod
    def getStoreDir():
        path = os.path.join(SettingManager.walle_home, "store/")
        if not os.path.exists(path):
            os.mkdir(path)
        return path

    @staticmethod
    def getFullPath(storekey):
        return os.path.join(SettingManager.getStoreDir(), storekey)

    @staticmethod
    def getScriptDir():
        path = os.path.join(SettingManager.walle_home, "python/")
        return path

    @staticmethod
    def load(storekey):
        path = SettingManager.getFullPath(storekey)
        value = []
        try:
            f = open(path, 'r')
            value = json.loads(f.read())
        except:
            pass
        return value 

    @staticmethod
    def save(storekey, value):
        path = SettingManager.getFullPath(storekey)
        f = open(path, 'w+')
        f.write(json.dumps(value, indent = 2))
        f.close();

    @staticmethod
    def editSavedValue(storekey, doneCallback = None):
        path = SettingManager.getFullPath(storekey)
        vim.command("sp %s"% path)
        if doneCallback:
            vim.command("autocmd BufWritePost <buffer> py %s" % doneCallback)
