import os
import threading
import vim
import json
from Finder import TrieFinder
import re
import subprocess

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

class RecentManager:
	def __init__(self, recentConfig):
		self.recentConfig = recentConfig

	def addToRecent(self, fileCandidate):
		recentCandidates = self.getRecent()
		recentCandidates.append(fileCandidate)
		recentCandidates.reverse()
		recentCandidates = CandidateUntils.unique(recentCandidates)

		if not os.path.exists(os.path.dirname(self.recentConfig)):
			os.mkdir(os.path.dirname(self.recentConfig))

		if os.path.isfile(self.recentConfig):
			os.remove(self.recentConfig)
		file =open(self.recentConfig, "w")
		for candidate in recentCandidates:
			file.write(candidate.getPath())
			file.write('\n')
		file.close()

	def getRecent(self):
		result = []
		try:
			lines = open(self.recentConfig).readlines()
			for line in lines:
				filePath = line.strip()
				if os.path.exists(filePath):
					fileName = os.path.basename(filePath)
					candidate = FileCandidate(name = fileName, path = filePath)
					result.append(candidate)
		except:
			result = []
		return result


class ReposManager:
	def __init__(self, reposConfig):
		try:
			reposConfig = json.load(open(reposConfig), 'utf-8')
			self.reposPath = reposConfig["reposPath"]
			self.reposIgnorePattern = reposConfig["ignorePattern"]
		except:
			self.reposPath = []
			self.ignorePattern = []
			print "error when load json config"

	def getReposPath(self):
		return self.reposPath

	def getIgnorePattern(self):
		return self.reposIgnorePattern

	def tranlate(self, pattern):
		table ={"*": ".*", '?':'.', "/": re.escape(os.sep)}
		s="".join([ c in table.keys() and table[c] or c for c in pattern])
		return re.compile(s)

class CandidateManager:
	def __init__(self, recentManager = None):
		self.recentManager = recentManager

	def getKeysMap(self):
		return {"<cr>":"close","<2-LeftMouse>":"keep","<c-o>":"keep", "<c-p>": "preview"}

	def acceptCandidate(self, candidate, way="close"):
		if way =="close":
			self.openCandidate(candidate)
			return False

		#todo: make a better name
		if way == "keep":
			self.openCandidate(candidate)
			return True

		if way =="preview":
			curwin = vim.eval("winnr()")
			self.openCandidate(candidate)
			#jump back to current window
			vim.command("%s wincmd w"%curwin)
			return True
		return True

	def openCandidate(self, candidate):
		if self.recentManager:
			self.recentManager.addToRecent(candidate)
		vim.command("wincmd w") #try next window
		vim.command("silent e %s"%candidate.getPath())

		if isinstance(candidate, TagCandidate):
			lineNumber = candidate.getLineNumber()
			vim.command("%d"%lineNumber)
			vim.command("normal z.")

class MRUCandidateManager(CandidateManager):
	def __init__(self, recentManager):
		CandidateManager.__init__(self, recentManager)
		self.recentmanager =recentManager
		self.recentCandidates = []
		self.bufferedCandidates = []

	def onStart(self):
		self.recentCandidates = self.recentManager.getRecent()
		self.bufferedCandidates = self.makeBufferCandidates()

	def searchCandidate(self, pattern):
		candidatesToSearch = self.recentCandidates + self.bufferedCandidates
		if pattern is "":
			result = self.recentCandidates
			return CandidateUntils.unique(result)
		elif pattern[0] == "@":
			candidatesToSearch = self.bufferedCandidates
			pattern =pattern[1:]
		elif pattern[0] == "#":
			candidatesToSearch = self.recentCandidates
			pattern =pattern[1:]

		substringResult =[candidate for candidate in candidatesToSearch if pattern.lower() in candidate.getKey().lower()]
		result= [candidate for candidate in candidatesToSearch if CandidateUntils.isSubset(pattern, candidate.getKey())]
		return CandidateUntils.unique(substringResult + result)

	def addPathtoRecent(self, path):
		if path and os.path.exists(path):
			filePath = os.path.abspath(path)
			fileName =os.path.basename(path)
			self.recentManager.addToRecent(FileCandidate(name=fileName, path=filePath))

	def makeBufferCandidates(self):
		buffers = filter(lambda buf: buf.name and os.path.exists(buf.name), vim.buffers)
		def createCandidate(buf):
			filePath = buf.name
			fileName = os.path.basename(filePath)
			return FileCandidate(name = fileName, path = filePath)
		return map(createCandidate, buffers)



class FileCandidateManager(MRUCandidateManager):
	def __init__(self, reposManager, recentManager):
		MRUCandidateManager.__init__(self, recentManager)
		self.reposManager  = reposManager
		self.finder = FileFinder()
		self.finder.setIgnoreCase()
		self.lock = threading.Lock()

	def searchCandidate(self, pattern):
		return MRUCandidateManager.searchCandidate(self, pattern) + self.finder.query(pattern)

	def refresh(self):
		threading.Thread(target = self.doRefresh).start()


	def doRefresh(self):
		self.lock.acquire()
		reposPath = self.reposManager.getReposPath()
		self.cachedCandidates = []
		for rootPath in reposPath:
			rootPath = rootPath.encode("utf-8", "ignore")
			if not os.path.exists(rootPath):
				print "%s is not exists"%rootPath
			for root, dirs, files in os.walk(rootPath):
				for filePath in files:
					filePath = os.path.join(root, filePath)
					filePath = os.path.normcase(filePath)
					if  self.pathShouldIgnore(filePath):
						continue
					fileName = os.path.basename(filePath)
					iterm = FileCandidate(name = fileName, path = filePath)
					self.cachedCandidates.append(iterm)
		self.finder.setCandidates(self.cachedCandidates)
		self.lock.release()


	def pathShouldIgnore(self, filePath):
		#if self.ignorePattern is None:
		#	self.ignorePattern = map(self.tranlate, self.reposConfig["ignorePattern"])
		#for pattern in self.ignorePattern:
		#	if pattern.match(filePath):
		#		return True
		return False



class FileFinder(TrieFinder):
	def __init__(self):
		TrieFinder.__init__(self)
		self.maxNumber = 30
		self.lastMixResults = []
		self.lastMixQuery = ""
		self.recentCandidates =[]

	def setMaxNumber(self, maxNumber):
		self.maxNumber = maxNumber


	def query(self, userInput):
		if userInput is "":
			return []
		return CandidateUntils.unique(self.queryMix(userInput))

	def queryMix(self, userInput):
		prefixCandidates = []

		index = len(userInput)
		while index > 0:
			prefixCandidates = TrieFinder.query(self, userInput[:index], 30)
			if prefixCandidates is not []:
				break
			index = index -1

		self.lastMixResults = self.scanFilter(userInput, CandidateUntils.unique(prefixCandidates + self.lastMixResults))

		return self.lastMixResults

	def scanFilter(self, userInput, candidates):
		def match(candidate):
			return CandidateUntils.isSubset(userInput, candidate.getKey())
		return filter(match, candidates)



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

class GTagsManager(CandidateManager):
	def __init__(self, recentManager):
		CandidateManager.__init__(self, recentManager)

	def globalCmd(self, cmd_args):
		cmd = ["global"] + cmd_args
		output = subprocess.check_output(cmd)
		return output

	def findFile(self, pattern, ignoreCase = True):
		result = []
		try:
			option = ignoreCase and "-Pai" or "-Pa"
			output = self.globalCmd([option, pattern])
			result = self.createCandidateFromBriefOutPut(output)
		except:
			print "pelase make sure you have file GTAGS in cwd or it's partents dir"
		return result

	def findSymbolDefine(self, symbol):
		output = self.globalCmd(["-ax", symbol])
		result = self.createCandidateFromDetailOutput(output)
		return result

	def findSymbolRef(self, symbol):
		output = self.globalCmd(["-arx", symbol])
		return  self.createCandidateFromDetailOutput(output)

	def findSymbol(self, symbol):
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

class QuickFind(CandidateManager):
	def __init__(self):
		CandidateManager.__init__(self)
		pass

	def findInCurrentBuffer(self, pattern):
		return self.findinBuffer(pattern, vim.current.buffer)

	def findInAllBuffers(self, pattern):
		result = []
		for buffer in vim.buffers:
			result.extend(self.findinBuffer(pattern, buffer))
		return result

	def findinBuffer(self, pattern, vimBuffer):
		result = []
		filePath = vimBuffer.name
		fileName = os.path.basename(filePath)
		for lineIndex, line in enumerate(vimBuffer):
			if re.search(pattern, line):
				result.append(TagCandidate(name=fileName, path=filePath, lineNumber = lineIndex+1, codeSnip = line.strip()))
		return result

	def acceptCandidate(self, candidate, way):
		if way == "autoPreview":
			curwin = vim.eval("winnr()")
			self.openCandidate(candidate)
			#jump back to current window
			vim.command("%s wincmd w"%curwin)
			return True
		return CandidateManager.acceptCandidate(self, candidate, way)

