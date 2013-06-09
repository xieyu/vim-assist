import vim
import json
import os

class StoreManager:
    walle_home = vim.eval("g:assistHome")
    @classmethod
    def getStoreDir(cls):
        path = os.path.join(cls.walle_home, "store/")
        if not os.path.exists(path):
            os.mkdir(path)
        return path

    @classmethod
    def getFullPath(cls, storekey):
        return os.path.join(cls.getStoreDir(), storekey)

    @classmethod
    def load(cls, storekey):
        path = cls.getFullPath(storekey)
        value = []
        try:
            f = open(path, 'r')
            value = json.loads(f.read())
        except:
            pass
        return value 

    @classmethod
    def save(cls, storekey, value):
        path = cls.getFullPath(storekey)
        f = open(path, 'w+')
        f.write(json.dumps(value, indent = 2))
        f.close();

    @classmethod
    def editSavedValue(cls, storekey, doneCallback = None):
        path = cls.getFullPath(storekey)
        vim.command("sp %s"% path)
        if doneCallback:
            vim.command("autocmd BufWritePost <buffer> py %s" % doneCallback)
