import subprocess
import re
import os

from SearchIterm import TagIterm
from Common import CommonUtil

class FileNvAssist:
    workdir=None
    @staticmethod
    def getFileIterms(stroke):
        stroke = stroke.strip()
        print stroke
        pwd = FileNvAssist.workdir
        if pwd is None:
            pwd = vim.eval("getcwd()")
        result = []
        for root, dirs, files in os.walk(pwd):
            for filePath in files:
                if CommonUtil.fileStrokeMatch(stroke, filePath):
                    fileName = os.path.basename(filePath)
                    filePath = os.path.join(root, filePath)
                    result.append(FileIterm(fileName, filePath))
        return result

    @staticmethod
    def clearWorkdir():
        FileNvAssist.workdir = None

    @staticmethod
    def setWorkdir(workdir):
        workdir = os.path.expandvars(os.path.expanduser(workdir))
        if os.path.exists(workdir):
            FileNvAssist.workdir = workdir
        else:
            print "%s is note exists"
