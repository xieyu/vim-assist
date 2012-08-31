import os
import threading
import vim
import json
import re
from shared.Controller import ControllerFactory
from shared.Finder import TrieFinder


class FileFinderDriver:
	def __init__(self):
		self.candidateManager = FileCandidateManager(self.getReposPath(), self.getRecentPath())
		self.refresh()

	def refresh(self):
		self.candidateManager.refresh()

	def run(self):
		self.candidateManager.onStart()
		matcher = ControllerFactory.getPromptMatchController(title ="Go-to-file", candidateManager = self.candidateManager)
		matcher.run()

	def editReposConfig(self):
		vim.command("sp %s"%self.getReposPath())

	def editRecentConfig(self):
		vim.command("sp %s"%self.getRecentPath())


	def getReposPath(self):
		walle_home = vim.eval("g:walle_home")
		return os.path.abspath(os.path.join(walle_home, "config/reposConfig"))

	def getRecentPath(self):
		walle_home = vim.eval("g:walle_home")
		return os.path.abspath(os.path.join(walle_home, "config/recentEditFiles"))



class FileCandidate:
	def __init__(self, name, key, path):
		self.name = name
		self.key = key
		self.path = path

	def getPath(self):
		return self.path

	def getName(self):
		return self.name

	def getKey(self):
		return self.key

class FileCandidateManager:
	def __init__(self, reposConfig, recentConfig):
		self.recentConfig = recentConfig
		self.reposConfig = self.parse(reposConfig)
		self.ignorePattern = None
		self.finder = FileFinder()
		self.finder.setIgnoreCase()
		self.lock = threading.Lock()

	def searchCandidate(self, pattern):
		return self.finder.query(pattern)

	def getKeysMap(self):
		return {"<cr>":"None","<2-LeftMouse>":"None"}

	def acceptCandidate(self, candidate, way):
		if way is "None":
			self.addToRecentCandidates(candidate)
			vim.command("wincmd w") #try next window
			vim.command("silent e %s"%candidate.getPath())
		#close the window
		return False

	def onStart(self):
		self.recentCandidates = []
		try:
			lines = open(self.recentConfig).readlines()
			for line in lines:
				filePath = line.strip()
				if os.path.exists(filePath):
					fileName = os.path.basename(filePath)
					candidate = FileCandidate(name = "%-40s\t%s"%(fileName, filePath), key = fileName, path = filePath)
					self.recentCandidates.append(candidate)
		except:
			self.recentCandidates = []
		self.finder.setRecentCandidate(self.getBufferCandidates() + self.recentCandidates)

	def refresh(self):
		threading.Thread(target = self.doRefresh).start()

	def parse(self, reposConfigFile):
		try:
			reposConfig = json.load(open(reposConfigFile), 'utf-8')
			return reposConfig
		except:
			print "error when load json config"
			return None

	def doRefresh(self):
		self.lock.acquire()
		reposPath = self.reposConfig["reposPath"]
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
					iterm = FileCandidate(name = "%-40s\t%s"%(fileName, filePath), key = fileName, path = filePath)
					self.cachedCandidates.append(iterm)
		self.finder.setCandidates(self.cachedCandidates)
		self.lock.release()


	def pathShouldIgnore(self, filePath):
		if self.ignorePattern is None:
			self.ignorePattern = map(self.tranlate, self.reposConfig["ignorePattern"])
		#for pattern in self.ignorePattern:
		#	if pattern.match(filePath):
		#		return True
		return False

	def getBufferCandidates(self):
		buffers = filter(lambda buf: buf.name and os.path.exists(buf.name), vim.buffers)
		def createCandidate(buf):
			filePath = os.path.normcase(buf.name)
			fileName = os.path.basename(filePath)
			return FileCandidate(name = "%-40s\t%s"%(fileName, filePath), key = fileName, path = filePath)
		return map(createCandidate, buffers)

	def tranlate(self, pattern):
		table ={"*": ".*", '?':'.', "/": re.escape(os.sep)}
		s="".join([ c in table.keys() and table[c] or c for c in pattern])
		return re.compile(s)



	def addToRecentCandidates(self, fileCandidate):
		if fileCandidate not in self.recentCandidates:
			self.recentCandidates.append(fileCandidate)

		if os.path.isfile(self.recentConfig):
			os.remove(self.recentConfig)
		file =open(self.recentConfig, "w")
		for candidate in self.recentCandidates:
			file.write(candidate.getPath())
			file.write('\n')
		file.close()


class FileFinder(TrieFinder):
	def __init__(self):
		TrieFinder.__init__(self)
		self.maxNumber = 30
		self.lastMixResults = []
		self.lastMixQuery = ""
		self.recentCandidates =[]

	def setMaxNumber(self, maxNumber):
		self.maxNumber = maxNumber

	def setRecentCandidate(self, recentCandidates):
		self.recentCandidates = recentCandidates

	def query(self, userInput):
		if userInput is "":
			self.lastMixResults = []
			self.lastQuery = ""
			return self.unique(self.queryRecent(userInput))

		return self.unique(self.queryRecent(userInput) + self.queryMix(userInput))

	def queryRecent(self, userInput):
		return self.scanFilter(userInput, self.recentCandidates)

	def queryMix(self, userInput):
		prefixCandidates = []

		index = len(userInput)
		while index > 0:
			prefixCandidates = TrieFinder.query(self, userInput[:index], 30)
			if prefixCandidates is not []:
				break
			index = index -1

		self.lastMixResults = self.scanFilter(userInput, self.unique(prefixCandidates + self.lastMixResults))

		return self.lastMixResults

	def scanFilter(self, userInput, candidates):
		def match(candidate):
			return self.is_subset(userInput, candidate.getKey())
		return filter(match, candidates)

	def unique(self, candidates):
		seen = {}
		ret = []
		for candidate in candidates:
			if not seen.has_key(candidate.getKey()):
				ret.append(candidate)
				seen[candidate.getKey()] = True
		return ret

	def is_subset(self, needle, haystack):
		m, n = (0,0)
		while n < len(needle) and m <len(haystack):
			if needle[n] == haystack[m] or needle[n].upper() == haystack[m]:
				n = n + 1
			m = m + 1
		return n == len(needle)


file_locate_driver = FileFinderDriver()
