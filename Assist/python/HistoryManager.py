import os
import vim
from SearchIterm import FileIterm
from Common import CommonUtil
from SettingManager import SettingManager

class HistoryManager(SearchBackend):
    recentFiles = None
    storeKey= "history.json"
    @staticmethod
    def add():
        filePath = vim.current.buffer.name
        if not os.path.exists(filePath):
            return
        if HistoryManager.recentFiles is None:
            HistoryManager.recentFiles = HistoryManager.load()
        for i, rfile in enumerate(HistoryManager.recentFiles):
            if rfile == filePath:
                del HistoryManager.recentFiles[i]
                break

        if filePath in HistoryManager.recentFiles:
            return

        HistoryManager.recentFiles.append(filePath)
        HistoryManager.save(HistoryManager.recentFiles)

    @staticmethod
    def edit():
        SettingManager.editSavedValue(HistoryManager.storeKey, "HistoryManager.reload()")

    @staticmethod
    def reload():
        HistoryManager.recentFiles = HistoryManager.load()

    @staticmethod
    def load():
        return [str(s) for s in SettingManager.load(HistoryManager.storeKey)]

    @staticmethod
    def save(filesList):
        return SettingManager.save(HistoryManager.storeKey, filesList)

    #implement interface of search backend
    @staticmethod
    def getHistoryIterms():
        result = []
        if HistoryManager.recentFiles is None:
            HistoryManager.recentFiles = HistoryManager.load()

        if HistoryManager.recentFiles is []:
            print "recent history is none"

        for filePath in HistoryManager.recentFiles:
            if filePath and os.path.exists(filePath):
                    result.append(FileIterm(filePath))
        result.reverse()
        return result
