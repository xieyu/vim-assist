import os
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

	def getPattern(self, userInput):
		r = userInput.split("/")
		filePattern = r[-1]
		if len(r) == 1:
			dirPatterns = []
		else:
			dirPatterns = r[:len(r)-1]
		return dirPatterns, filePattern

	def editDistance(self, strA, strB):
		def isModify(i, j):
			return strA[i] == strB[j] and 0 or 1;

		def edit(i, j):
			if i == 0 and j == 0:
				return isModify(i, j)
			elif i == 0 or j == 0:
				if j > 0:
					return isModify(i,j) and edit(i, j-1)+1 or j
				else:
					return isModify(i,j) and edit(i-1, j)+1 or i
			else:
				return min([edit(i-1, j)+1, edit(i,j-1)+1, edit(i-1, j-1), isModify(i,j)])
		return edit(len(strA) -1, len(strB)-1)

	def match(self, pattern, item):
		patternLower = pattern.lower()
		itemLower = item.lower()
		return patternLower in itemLower


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
