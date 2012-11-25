import vim
import os
import subprocess

class WalleProjectManager(object):
    @staticmethod
    def getProjectSettings(filePath):
        "includePath=$andorid_home/pathA:pathB;classPath=pathA:pathB"
        projectFile = WalleProjectManager.getProjectFile(filePath)
        if (projectFile):
            return open(projectFile).readLines()
        return None

    @staticmethod
    def syntaxCheckForCurrentBuffer():
        filePath = vim.current.buffer.name
        if os.path.exists(filePath):
            settings = WalleProjectManager.getProjectSettings(filePath)
            errors = WalleCompiler.syntaxCheck(settings, filePath)
            WalleHighlightManager.removeAllHighlightInFile(filePath)
            if errors:
                for error in errors:
                    WalleHighlightManager.addHighlightInfo(WalleProjectManager.getSrcLocation(error.filePath), error.line_num, error.line_start, error.line_end, error.error_type, error.message)
                WalleHighlightManager.highlightCurrentBuf()

    @staticmethod
    def getSrcLocation(fileName):
        return fileName

    @staticmethod
    def build():
        pass

    @staticmethod
    def run():
        pass

    @staticmethod
    def debug():
        pass

    #privates:
    @staticmethod
    def getProjectFile(filePath):
        if not filePath:
            return
        parent = filePath
        while True:
            tmpdir = os.path.dirname(parent)
            if tmpdir == "" or tmpdir == "/" or tmpdir == parent:
                break;
            parent = tmpdir
            path = os.path.join(parent, ".project")
            if os.path.exists(path):
                return path
        return None

class WalleHighlightManager(object):
    highlights = {}
    class ErrorInfo(object):
        def __init__(self, lineStart, lineEnd, errorType, message):
            self.message = message
            self.lineStart = lineStart 
            self.lineEnd = lineEnd
            self.errorType = errorType

    @staticmethod
    def removeAllHighlightInFile(filePath):
        highlights = WalleHighlightManager.highlights
        if highlights.has_key(filePath):
            del highlights[filePath]

    @staticmethod
    def addHighlightInfo(abs_path, line_num, line_start, line_end, error_type, message=""):
        highlights = WalleHighlightManager.highlights
        if not highlights.has_key(abs_path):
            highlights[abs_path] = {}
        if not highlights[abs_path].has_key(line_num):
            highlights[abs_path][line_num] = []

        highlights[abs_path][line_num].append(WalleHighlightManager.ErrorInfo(line_start, line_end, error_type, message))

    @staticmethod
    def displayMsg():
        highlights = WalleHighlightManager.highlights
        filePath= vim.current.buffer.name
        (row,col) = vim.current.window.cursor
        message = ""
        if highlights.has_key(filePath) and highlights[filePath].has_key(row):
            errorInfos = highlights[filePath][row]
            errorInfo = errorInfos[0]
            min_distance = abs(errorInfo.lineStart - col)
            for t in errorInfos:
                if min_distance > abs(t.lineStart - col):
                    errorInfo = t
                    min_distance = abs(t.lineStart - col)
            message = errorInfo.message
        vim.command('call VimUtils#DisplayMsg("%s")' % message)

    @staticmethod
    def highlightCurrentBuf():
        highlights = WalleHighlightManager.highlights
        WalleHighlightManager.clearHighlightInVim()
        filePath= vim.current.buffer.name
        for lineNum, errorInfos in highlights[filePath].items():
            for errorInfo in errorInfos:
                group = WalleHighlightManager.getGroupName(errorInfo.errorType)
                start = errorInfo.lineStart
                syncmd = """syn match %s "\%%%dl\%%>%dv.[a-zA-Z_0-9]*\>" """ %(group, lineNum, start)
                vim.command(syncmd)
                WalleHighlightManager.highlightError(lineNum, errorInfo.lineStart, errorInfo.lineEnd, errorInfo.errorType)

    @staticmethod
    def getGroupName(highlightType):
        higlightMap ={"warning": "Walle_Warning", "error": "Walle_Error", "note":"Walle_Reference"}
        if higlightMap.has_key(highlightType.strip()):
            return higlightMap[highlightType.strip()]
        else:
            return higlightMap["warning"]

    @staticmethod
    def highlightError(lineNum, lineStart, lineEnd, errorType):
        lineNum, start, end = int(lineNum), int(lineStart), int(lineEnd)
        group = WalleHighlightManager.getGroupName(errorType)
        syncmd = """syn match %s "\%%%dl\%%>%dv.[a-zA-Z_0-9]*\>" """ %(group, lineNum, start)
        vim.command(syncmd)

    @staticmethod
    def clearHighlightInVim():
        vim.command("syntax clear Walle_Error")
        vim.command("syntax clear Walle_Warning")
        vim.command("syntax clear Walle_Reference")

class WalleCompiler:
    @staticmethod
    class ErrorInfo:
        def __init__(self, filePath, line_num, line_start, line_end, error_type, message):
            self.filePath = filePath
            self.message = message
            self.line_num = line_num
            self.line_start = line_start
            self.line_end = line_end
            self.error_type = error_type

        def __str__(self):
            return "(%s,%s)" % (self.error_type, self.error_message)

        def __repr__(self):
            return "(%s,%s)" % (self.error_type, self.error_message)

    @staticmethod
    def syntaxCheck(settings, filePath):
        if not os.path.exists(filePath):
            return None
        errors = None
        root, ext = os.path.splitext(filePath)
        checkers={".java":WalleCompiler.javaSynatxCheck, ".cpp":WalleCompiler.cppSynatxCheck, ".c":WalleCompiler.cppSynatxCheck, "py" : WalleCompiler.pythonSynatxCheck}
        if checkers.has_key(ext):
            syntaxCheck = checkers[ext] 
            errors = syntaxCheck(settings, filePath)
        return errors

    @staticmethod
    def javaSynatxCheck(options, filePath):
        pass

    @staticmethod
    def cppSynatxCheck(settings, filePath):
        cmd = ["clang", "-fsyntax-only"]
        options =[]
        try:
            includePath = settings["includePath"]
            for t in includePath.split(":"):
                options.append("-I %s" %t)
        except:
            options = []

        cmd = cmd + options + [filePath]
        errors = []
        try:
            subprocess.check_output(cmd, stderr = subprocess.STDOUT)
        except subprocess.CalledProcessError as error:
            for line in error.output.split("\n"):
                errorInfo = line.split(":")
                #file:line:col:error_type:message
                if len(errorInfo) == 5:
                    (fileName, line_num, col, error_type, message) = errorInfo
                    line_end = -1
                    errors.append(WalleCompiler.ErrorInfo(fileName, int(line_num), int(col), int(line_end), error_type, message))
        return errors
    @staticmethod
    def pythonSynatxCheck(options, filePath):
        pass

class EditAssist:
    pass
