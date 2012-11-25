import os
import vim
import re
import subprocess
import sqlite3
from python.VimUi import ControllerFactory

class FileCandidate:
    def __init__(self, name, path):
        self.name = name
        self.path = path

    def getPath(self):
        return self.path

    def getName(self):
        return self.name

    def getKey(self):
        return os.path.normpath(self.path)

    def getDisplayName(self):
        return "%-40s\t%s"%(self.name, self.path)

class TagCandidate(FileCandidate):
    def __init__(self, name, path, lineNumber, codeSnip):
        FileCandidate.__init__(self, name, path)
        self.lineNumber = lineNumber
        self.codeSnip = codeSnip

    def getLineNumber(self):
        return int(self.lineNumber)

    def getKey(self):
        return self.path+self.lineNumber

    def getDisplayName(self):
        return "%-30s\t%-10s\t%-50s"%(os.path.basename(self.path), self.lineNumber, self.codeSnip)

class CommandCandidate:
    def __init__(self, cmd, needArgs, isVimCommnd):
        self.cmdName = cmd
        self.needArgs = needArgs
        self.isVimCommnd = isVimCommnd

    def getDisplayName(self):
        return self.cmdName




class CandidateUntils:
    @staticmethod
    def unique(candidates):
        seen = {}
        ret = []
        for candidate in candidates:
            if not seen.has_key(candidate.getKey()):
                ret.append(candidate)
                seen[candidate.getKey()] = True
        return ret

    @staticmethod
    def isSubset(needle, haystack):
        m, n = (0,0)
        while n < len(needle) and m <len(haystack):
            if needle[n] == haystack[m] or needle[n].upper() == haystack[m]:
                n = n + 1
            m = m + 1
        return n == len(needle)

class Searcher:
    def prepare(self):
        pass
    def search(self, pattern):
        return []

class SearchInBuffer:
    def prepare(self):
        self.filePath = vim.current.buffer.name
        try:
            self.searchLines = open(self.filePath).readlines()
        except:
            self.searchLines = []

    def searchInBuffer(self, kindPattern, searchPattern):
        kindPattern = re.compile(kindPattern)
        searchPattern = re.compile(searchPattern, re.IGNORECASE)
        result = []
        try:
            for lineNum, line in enumerate(self.searchLines):
                match = kindPattern.search(line)
                if match:
                    functionName = match.groups(0)[0]
                    if searchPattern.match(functionName):
                        result.append(TagCandidate(self.filePath, self.filePath, lineNum + 1, line.strip()))
            return result
        except:
            return []

class SearchClassInBuffer(SearchInBuffer):
    def search(self, pattern):
        kindPattern = "class\s*([_a-zA-Z][a-zA-Z0-9<>]*\s*)"
        return self.searchInBuffer(kindPattern, pattern)

class SearchFunctionInBuffer(SearchInBuffer):
    def search(self, pattern):
        functionPattern = "([_a-zA-Z][a-zA-Z0-9<>:]*\s*[(])"
        return self.searchInBuffer(functionPattern, pattern)

class SearchSymbolInBuffer(SearchInBuffer):
    def search(self, pattern):
        result = []
        pattern = re.compile(pattern, re.IGNORECASE)
        for lineNum, line in enumerate(self.searchLines):
            if pattern.search(line.strip()):
                result.append(TagCandidate(self.filePath, self.filePath, lineNum + 1, line.strip()))
        return result

class SearchRecentFiles(Searcher):
    walle_home = vim.eval("g:walle_home")
    recentConfigFile = os.path.join(walle_home, "config/recentFiles")
    def prepare(self):
        try:
            self.recentFileCollection = [line.strip() for line in open(SearchRecentFiles.recentConfigFile).readlines()]
            self.recentFileCollection.reverse()
        except:
            self.recentFileCollection = []

    def search(self, pattern):
        pattern = re.compile(pattern, re.IGNORECASE)
        result = []
        for filePath in self.recentFileCollection:
            filePath = filePath.strip()
            if pattern.search(filePath):
                fileName = os.path.basename(filePath)
                result.append(FileCandidate(fileName, filePath))
        return result

    @staticmethod
    def addToRecent():
        filePath = vim.current.buffer.name
        if filePath and os.path.exists(filePath):
            configFile = SearchRecentFiles.recentConfigFile
            recentFiles = [line.strip() for line in open(configFile).readlines()]
            if filePath in recentFiles:
                return
            recentFiles.append(filePath)

            if not os.path.exists(os.path.dirname(configFile)):
                os.mkdir(os.path.dirname(configFile))

            if os.path.isfile(configFile):
                os.remove(configFile)

            file =open(configFile, "w")
            for filePath in recentFiles:
                if os.path.exists(filePath):
                    file.write(filePath)
                    file.write('\n')
            file.close()

class SearchFileNameFromBufferList(Searcher):
    def prepare(self):
        self.filePaths = [buf.name for buf in vim.buffers if buf.name and os.path.exists(buf.name)]

    def search(self, pattern):
        pattern = re.compile(pattern, re.IGNORECASE)
        result = []
        for filePath in self.filePaths:
            fileName = os.path.basename(filePath)
            if pattern.match(fileName):
                result.append(FileCandidate(fileName, filePath))
        return result

class SearchFileNameFromDatabase(Searcher):
    def prepare(self):
        pass

    def search(self, pattern):
        db = WalleTagsManager.getDatabasePath()
        pattern = pattern.strip()
        if pattern is "":
            return []

        def regexp(expr, item):
            pattern = re.compile(expr, re.IGNORECASE)
            if "/" not in expr:
                return pattern.match(item) is not None
            else:
                return pattern.search(item) is not None

        connection = sqlite3.connect(db)
        connection.create_function("REGEXP", 2, regexp)
        cursor= connection.cursor()
        if '/' in pattern:
            cursor.execute("select fileName, filePath from FilePaths where filePath REGEXP'%s'limit 30"%pattern)
        else:
            cursor.execute("select fileName, filePath from FilePaths where fileName REGEXP'%s'limit 30"%pattern)

        def toString(s):
            return isinstance(s, unicode) and s.encode("utf8") or s

        return [FileCandidate(toString(fileName), toString(filePath)) for fileName, filePath in cursor.fetchall()]

class SearchSymbolFromGtags(Searcher):
    def globalCmd(self, cmd_args):
        cmd = ["global"] + cmd_args
        output = subprocess.check_output(cmd)
        return output

    def search(self, symbol):
        symbol = symbol.strip()
        output = self.globalCmd(["-arxs", symbol])
        return  self.createCandidateFromDetailOutput(output)

    def createCandidateFromDetailOutput(self, output):
        result = []
        pattern = re.compile("(\S*)\s*(\d*)\s*(\S*)\s*(.*$)")
        for line in output.split("\n"):
            line = line.strip()
            if line:
                (symbol, lineNumber, filePath, codeSnip) = pattern.search(line).groups()
                iterm = TagCandidate(name = symbol, path = filePath, lineNumber = lineNumber, codeSnip = codeSnip)
                result.append(iterm)
        return result

    def createCandidateFromBriefOutPut(self, output):
        result = []
        for filePath in output.split("\n"):
            filePath = filePath.strip()
            if filePath:
                fileName = os.path.basename(filePath)
                iterm = FileCandidate(name = fileName, path = filePath)
                result.append(iterm)
        return result

class SearchAssist:
    walle_home = vim.eval("g:walle_home")
    recentConfigFile = os.path.join(walle_home, "config/recentFiles")
    increamentSearchCommand = {
            "c" : SearchClassInBuffer(),
            "f" : SearchFunctionInBuffer(),
            "s" : SearchSymbolInBuffer(),
            "b" : SearchFileNameFromBufferList(),
            "r" : SearchRecentFiles(),
            }
    searchCommand = {
            "b" : SearchFileNameFromDatabase(),
            "s" : SearchSymbolFromGtags()
            }
    @staticmethod
    def increamentSearch():
        SearchAssist.lastWinnr = vim.eval("winnr()")
        for key, searcher in SearchAssist.increamentSearchCommand.items():
            searcher.prepare()
        matcher = ControllerFactory.getPromptMatchController(title ="command", candidateManager = SearchAssist)
        matcher.run()

    @staticmethod
    def quickSearch():
        pattern = vim.eval('input("%s ")'%">>")
        key = pattern[0]
        for key, searcher in SearchAssist.searchCommand.items():
            searcher.prepare()
        if SearchAssist.searchCommand.has_key(key):
            handler = SearchAssist.searchCommand.get(key)
            result = handler.search(pattern[1:])
            displayer = ControllerFactory.getDisplayController("search-result", SearchAssist)
            if  len(result) == 0:
                print "can not find with pattern %s"%pattern
            elif(len(result)==1):
                SearchAssist.acceptCandidate(result[0], "close")
                vim.command("redraw")
            else:
                displayer.show(result)

    @staticmethod
    def searchCandidate(pattern):
        if len(pattern) < 1:
            return []

        key = pattern[0]
        if SearchAssist.increamentSearchCommand.has_key(key):
            handler = SearchAssist.increamentSearchCommand.get(key)
            return handler.search(pattern[1:])
        else:
            return []

    @staticmethod
    def getKeysMap():
        return {"<cr>":"close","<2-LeftMouse>":"keep","<c-o>":"keep", "<c-p>": "preview"}

    @staticmethod
    def acceptCandidate(candidate, way):
        curwin = vim.eval("winnr()")
        if isinstance(candidate, FileCandidate):
            wId = vim.eval("VimUtils#firstUsableWindow()")
            vim.command("%s wincmd w"%wId) #try next window
            vim.command("silent e %s"%candidate.getPath())

        if isinstance(candidate, TagCandidate):
            lineNumber = candidate.getLineNumber()
            vim.command("%d"%lineNumber)
            vim.command("normal z.")

        if way != "autoPreview" and isinstance(candidate, CommandCandidate):
            vim.command("%s wincmd w"%SearchAssist.lastWinnr)
            if candidate.isVimCommnd:
                if not candidate.needArgs:
                    vim.command(candidate.cmdName)
                else:
                    args = vim.eval('input("%s ")'%candidate.cmdName)
                    vim.command("%s %s"%(candidate.cmdName, args.strip()))

        if way =="preview" or way == "autoPreview":
            vim.command("%s wincmd w"%curwin)
        return way != "close"



class SearchUntils:
    projectFileName = ".walleProject"
    @staticmethod
    def addToRecent():
        SearchRecentFiles.addToRecent()
    @staticmethod
    def findSymbol(arg):
        searcher = SearchSymbolFromGtags()
        result = searcher.search(arg)
        displayer = ControllerFactory.getDisplayController("search-result", SearchAssist)
        if  len(result) == 0:
            print "can not find %s"%arg
        elif(len(result)==1):
            SearchAssist.acceptCandidate(result[0], "close")
            vim.command("redraw")
        else:
            displayer.show(result)



class WalleTagsManager:
    projectFileName = ".walleProject"
    @staticmethod
    def getProjectRootPath():
        parent = vim.eval("getcwd()")
        while parent and True:
            path = os.path.join(parent, WalleTagsManager.projectFileName)
            if os.path.exists(path):
                return parent
            tmpdir = os.path.dirname(parent)
            if tmpdir == "" or tmpdir == "/" or tmpdir == parent:
                break;
            parent = tmpdir
        return None

    @staticmethod
    def getDatabasePath():
        rootPath = WalleTagsManager.getProjectRootPath()
        databasePath = os.path.join(rootPath, ".walleTags")
        return databasePath

    @staticmethod
    def getIgnoreDirs():
        return [".git"]

    @staticmethod
    def getIgnoreFilePatterns():
        return []

    @staticmethod
    def makeFilePathTags():
        #TODO:make a new thread to do this
        rootPath = WalleTagsManager.getProjectRootPath()
        ignoredirs = WalleTagsManager.getIgnoreFilePatterns()
        dbPath = WalleTagsManager.getDatabasePath()
        if not dbPath:
            return

        connection = sqlite3.connect(dbPath)
        try:
            connection.execute('drop table FilePaths')
        except:
            pass

        connection.execute('create table if not exists FilePaths(fileName varchar(60), filePath text, fileType varchar(10))')
        connection.commit()

        for rootdir, dirs, files in os.walk(rootPath):
            if os.path.basename(rootdir) not in ignoredirs:
                for dirName in dirs:
                    absPath = os.path.join(rootdir, dirName)
                    fileName = os.path.basename(dirName)
                    connection.execute('insert into FilePaths(fileName, filePath, fileType) values("%s", "%s", "%s")'%(fileName, absPath, 'dir'))
                for filePath in files:
                    base, ext = os.path.splitext(filePath)
                    fileName = os.path.basename(filePath)
                    absPath = os.path.join(rootdir, filePath)
                    connection.execute('insert into FilePaths(fileName, filePath, fileType) values("%s", "%s", "%s")'%(fileName, absPath, ext))
        connection.commit()
