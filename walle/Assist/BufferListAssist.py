import os
import vim
from Assist.Candidate import FileCandidate 
from Assist.Candidate import CandidateManager
from Assist.CommonUtil import CommonUtil

#TODO:FIXIT, remove this  ugly code
from Assist.VimUi import ControllerFactory

class BufferListAssist:
    walle_home = vim.eval("g:walle_home")
    configFile= os.path.join(walle_home, "config/recentFiles")

    @staticmethod
    def searchHot():
        BufferListAssist.filePaths = [buf.name for buf in vim.buffers if buf.name and os.path.exists(buf.name)]
        CandidateManager.searchHot(BufferListAssist.SearchHotCallbacker)


    class SearchHotCallbacker:
        @staticmethod
        def search(pattern):
            result = []
            for filePath in BufferListAssist.filePaths:
                if CommonUtil.strokeMatch(pattern, filePath):
                    fileName = os.path.basename(filePath)
                    result.append(FileCandidate(fileName, filePath))
            return result
