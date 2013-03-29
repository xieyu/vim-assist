import os
import vim
from SearchIterm import FileIterm
from Common import CommonUtil
from Common import SettingManager

class HistoryAssist:
    recentFiles = None
    storeFileName= "HistoryFiles"
    @staticmethod
    def getHistoryIterms(symbol):
        result = []
        if HistoryAssist.recentFiles is None:
            HistoryAssist.recentFiles = HistoryAssist.load()
        if HistoryAssist.recentFiles is []:
            print "recent history is none"

        for filePath in HistoryAssist.recentFiles:
            if filePath:
                fileName = os.path.basename(filePath)
                if CommonUtil.fileStrokeMatch(symbol, filePath):
                    result.append(FileIterm(fileName, filePath))
        result.reverse()
        return result

    @staticmethod
    def add():
        filePath = vim.current.buffer.name
        if not os.path.exists(filePath):
            return
        if HistoryAssist.recentFiles is None:
            HistoryAssist.recentFiles = HistoryAssist.load()
        for i, rfile in enumerate(HistoryAssist.recentFiles):
            if rfile == filePath:
                del HistoryAssist.recentFiles[i]
                break

        if filePath in HistoryAssist.recentFiles:
            return

        HistoryAssist.recentFiles.append(filePath)
        HistoryAssist.save(HistoryAssist.recentFiles)

    @staticmethod
    def clear():
        HistoryAssist.save([])

    @staticmethod
    def edit():
        storeFilePath = os.path.join(SettingManager.getStoreDir(), HistoryAssist.storeFileName)
        vim.command("sp %s"% storeFilePath)
        vim.command("autocmd BufWritePost <buffer> py HistoryAssist.reload()")

    @staticmethod
    def reload():
        HistoryAssist.recentFiles = HistoryAssist.load()

    @staticmethod
    def load():
        storeFilePath = os.path.join(SettingManager.getStoreDir(), HistoryAssist.storeFileName)
        result = []
        try:
            f = open(storeFilePath, 'r')
            for line in f.readlines():
                result.append(line.strip())
        except:
            pass
        return result

    @staticmethod
    def save(filesList):
        storeFilePath = os.path.join(SettingManager.getStoreDir(), HistoryAssist.storeFileName)
        f = open(storeFilePath, 'w+')
        for filePath in filesList:
            f.write("%s\n" % filePath)
        f.close();
        pass


