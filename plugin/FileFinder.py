import os
import threading
import vim
from Factory import SharedFactory
from Finder import TrieFinder
from Candidates import Candidate
from Acceptor import Acceptor

class FileFinderDriver:
	def __init__(self, reposFile, recentFilesListPath):
		self.candidateManager = FileCandidateManager(reposFile, recentFilesListPath)

		self.finder = FileFinder()
		self.finder.setIgnoreCase()
		self.finder.setCandidateManager(self.candidateManager)

		self.acceptor = FileAcceptor()
		self.acceptor.setCandidateManager(self.candidateManager)

		self.lock = threading.Lock()
		self.refresh()

	def refresh(self):
		threading.Thread(target = self.doRefresh).start()

	def doRefresh(self):
		self.lock.acquire()
		self.candidateManager.refresh()
		candidates = self.candidateManager.getCachedCandidates()
		self.finder.setCandidates(candidates)
		print "file finder refresh is done :)"
		self.lock.release()
	
	def run(self):
		self.candidateManager.refreshRecentFilesList()
		matcher = SharedFactory.getPromptMatchController(title ="Go-to-file", finder = self.finder, acceptor = self.acceptor)
		matcher.run()


class FileCandidate(Candidate):
	def __init__(self, name, key, path):
		Candidate.__init__(self, name, key)
		self.path = path
		
	def getPath(self):
		return self.path

class FileCandidateManager:
	def __init__(self, reposFile, recentFilesListPath):
		self.reposFile = reposFile
		self.rootPathList = self.parse(self.reposFile)
		self.cachedCandidates = []
		self.recentCandidates = []
		self.recentFilesListPath = recentFilesListPath

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
					filePath = os.path.normcase(filePath)
					if  self.pathShouldIgnore(filePath):
						continue
					fileName = os.path.basename(filePath)
					iterm = FileCandidate(name = "%-40s\t%s"%(fileName, filePath), key = fileName, path = filePath)
					self.cachedCandidates.append(iterm)

	
	def pathShouldIgnore(self, filePath):
		return ".git" in filePath

	def getCachedCandidates(self):
		return self.cachedCandidates	

	def getBufferCandidates(self):
		buffers = filter(lambda buf: buf.name and os.path.exists(buf.name), vim.buffers)
		def createCandidate(buf):
			filePath = os.path.normcase(buf.name)
			fileName = os.path.basename(filePath)
			return FileCandidate(name = "%-40s\t%s"%(fileName, filePath), key = fileName, path = filePath)
		return map(createCandidate, buffers)


	def refreshRecentFilesList(self):
		try:
			lines = open(self.recentFilesListPath).readlines()
		except:
			return
		self.recentCandidates = []
		for line in lines:
			filePath = line.strip()
			if os.path.exists(filePath):
				fileName = os.path.basename(filePath)
				candidate = FileCandidate(name = "%-40s\t%s"%(fileName, filePath), key = fileName, path = filePath)
				self.recentCandidates.append(candidate)


	def getRecentlyCandidates(self):
		return self.recentCandidates

	def addToRecentCandidates(self, fileCandidate):
		if fileCandidate not in self.recentCandidates:
			self.recentCandidates.append(fileCandidate)
		if os.path.isfile(self.recentFilesListPath):
			os.remove(self.recentFilesListPath)
		file =open(self.recentFilesListPath, "w") 
		for candidate in self.recentCandidates:
			file.write(candidate.getPath())
			file.write('\n')
		file.close()

class FileFinder(TrieFinder):
	def __init__(self):
		TrieFinder.__init__(self)
		self.candidateManager = None
	def setCandidateManager(self, candidateManager):
		self.candidateManager = candidateManager

	def query(self, userInput):
		def unique(candidatesList):
			t = {}
			for i in candidatesList:
				t[i.getPath()] = i
			return [value for key,value in t.items()]
		return unique(self.queryRecent(userInput)) + TrieFinder.query(self, userInput)

	def queryRecent(self, userInput):
		candidates = []
		if self.candidateManager:
			candidates = self.candidateManager.getBufferCandidates() + self.candidateManager.getRecentlyCandidates()

		def match(candidate):
			return userInput is "" or userInput.lower() in os.path.basename(candidate.getPath()).lower()

		return filter(match, candidates)
		

class FileAcceptor(Acceptor):
	def __init__(self):
		self.candidateManager = None

	def setCandidateManager(self, candidatesManager):
		self.candidateManager = candidatesManager

	def accept(self, fileCandidate, options = None):
		if options is "None":
			if self.candidateManager:
				self.candidateManager.addToRecentCandidates(fileCandidate)
			return self.editFile(fileCandidate)

	def selectWindow(self):
		vim.command("wincmd w") #try next window

	def editFile(self, fileCandidate):
		self.selectWindow()
		vim.command("silent e %s"%fileCandidate.getPath())
		#close the window
		return False
