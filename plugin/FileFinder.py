import os
import re
import threading
import vim
from Factory import SharedFactory
from Finder import Finder
from Candidates import Candidate
from Acceptor import Acceptor

class FileFinderDriver:
	def __init__(self, reposFile):
		self.candidateManager = FileCandidateManager(reposFile)
		self.finder = FileFinder()
		self.acceptor = FileAcceptor()
		self.lock = threading.Lock()
		#self.refresh()

	def refresh(self):
		self.IsReady = False
		threading.Thread(target = self.doRefresh).start()

	def doRefresh(self):
		self.lock.acquire()
		self.candidateManager.refresh()
		candidates = self.candidateManager.getCachedCandidates()
		self.finder.setCandidates(candidates)
		print "file finder refresh is done :)"
		self.IsReady = True
		self.lock.release()
	
	def run(self):
		matcher = SharedFactory.getMatchController(title ="Go-to-file", finder = self.finder, acceptor = self.acceptor)
		matcher.show()

class FileCandidate(Candidate):
	def __init__(self, name, key, filePath):
		Candidate.__init__(self, name, key)
		self.filePath = filePath
		pass
		
	def getPath(self):
		return self.filePath

class FileCandidateManager:
	def __init__(self, reposFile):
		self.reposFile = reposFile
		self.rootPathList = self.parse(self.reposFile)
		self.cachedCandidates = []

	def parse(self, reposFile):
		try:
			lines = open(reposFile).readlines()
		except:
			print "your repose is empty, try use command FinderEditRepos"
			return
		return [line.strip()  for line in lines if line.strip() and line.strip()[0]!="#"]

	def refresh(self):
		self.rootPathList = self.parse(self.reposFile)
		if self.rootPathList is None:
			return
		self.cachedCandidates = []
		for rootPath in self.rootPathList:
			if not os.path.exists(rootPath):
				print "%s is not exists"%rootPath
			for root, dirs, files in os.walk(rootPath):
				for filePath in files:
					filePath = os.path.join(root, filePath)
					if  self.pathShouldIgnore(filePath):
						continue
					fileName = os.path.basename(filePath)
					iterm = FileCandidate(name = "%s\t %s"%(fileName, filePath), key = fileName.lower(), filePath = filePath)
					self.cachedCandidates.append(iterm)
	
	def pathShouldIgnore(self, filePath):
		return ".git" in filePath

	def getCachedCandidates(self):
		return self.cachedCandidates	

class FileFinder(Finder):
	def __init__(self):
		Finder.__init__(self)
		self.candidates = []
		self.lastQuery = None
		self.pathMatchsCache = {}

	def addCandidates(self, fileCandidates):
		self.candidates.extend(fileCandidates)

	def setCandidates(self, fileCandidates):
		self.candidates = fileCandidates

	def query(self, userInput):
		searchItems = self.candidates
		if self.lastQuery and self.match(self.lastQuery, userInput):
			searchItems = self.suiteCandidates
		self.suiteCandidates = self.doQuery(userInput, searchItems)
		self.lastQuery = userInput
		return self.suiteCandidates

	def doQuery(self, userInput, fileCandidates):
		dirNamePattern, fileNamePattern = self.getPattern(userInput)
		result = []
		for fileCandidate in fileCandidates:
			path = fileCandidate.getPath()
			if fileNamePattern and self.match(fileNamePattern, os.path.basename(path)):
				result.append(fileCandidate)
		searchResult = sorted(result, key = lambda fileCandidate: self.editDistance(userInput, os.path.basename(fileCandidate.getPath())))

		result = []
		for fileCandidate in fileCandidates:
			path = fileCandidate.getPath()
			if dirNamePattern and self.match(dirNamePattern, os.path.dirname(path)):
				result.append(fileCandidate)
		searchResult.extend(sorted(result, key = lambda fileCandidate: self.editDistance(userInput, os.path.dirname(fileCandidate.getPath()))))
		#searchResult.extend(result)
		return searchResult

	def getPattern(self, pattern):
		pathPart = pattern.split("/")
		fileNamePart = pathPart.pop() 
		pathRegex = None
		fileRegex = None
		if pathPart:
			pathRegexRaw = "^(.*?)" + [self.makePattern(part) for part in pathPart].join("(.*?/.*?/") + "(.*?)$"
			pathRegex = re.compile(pathRegexRaw, re.IGNORECASE)

		fileRegexRaw = "^(.*?)" + self.makePattern(fileNamePart) + "(.*)$"
		fileRegex = re.compile(fileRegexRaw, re.IGNORECASE)

		return pathRegex,fileRegex


	def makePattern(self, pattern):
		if pattern is "":
			return ""
		regex = None
		for character in pattern:
			regex = regex and regex + "([^/]*?)"
			regex = regex + "(%s)"%(re.escape(character))
		return regex

	def matchPath(self, path, pathRegex, pathSegments):
		if self.pathMatchsCache.has_key(path):
			return self.pathMatchsCache[path]
		matchablePath = path
		if pathRegex:
			match = pathRegex.match(path)
			self.pathMatchsCache[path] = match and self.buildMatchResult(match, pathSegments) or {"score":1, "result":matchablePath, "missed":True}
		else:
			self.pathMatchsCache[path] ={"score":1, "result":matchablePath}

	def matchFile(self):
		pass

	def buildMatchResult(self):
		pass


	def match(self, pattern, item):
		pass


class FileAcceptor(Acceptor):
	def __init__(self):
		pass

	def accept(self, fileCandidate, options = None):
		if options is None:
			return self.editFile(fileCandidate)

	def selectWindow(self):
		vim.command("wincmd w") #try next window

	def editFile(self, fileCandidate):
		self.selectWindow()
		vim.command("silent e %s"%fileCandidate.getPath())
		#close the window
		return False
