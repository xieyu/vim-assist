import os
import threading
import vim
from Factory import SharedFactory
from Finder import TrieFinder
from Candidates import Candidate
from Acceptor import Acceptor

class FileFinderDriver:
	def __init__(self, reposFile):
		self.candidateManager = FileCandidateManager(reposFile)
		self.finder = FileFinder()
		self.finder.setIgnoreCase()
		self.acceptor = FileAcceptor()
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
		matcher = SharedFactory.getPromptMatchController(title ="Go-to-file", finder = self.finder, acceptor = self.acceptor)
		matcher.run()


class FileCandidate(Candidate):
	def __init__(self, name, key, path):
		Candidate.__init__(self, name, key)
		self.path = path
		pass
		
	def getPath(self):
		return self.path

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
					iterm = FileCandidate(name = "%s\t %s"%(fileName, filePath), key = fileName, path = filePath)
					self.cachedCandidates.append(iterm)
	
	def pathShouldIgnore(self, filePath):
		return ".git" in filePath

	def getCachedCandidates(self):
		return self.cachedCandidates	

	@staticmethod
	def getBufferCandidates():
		buffers = filter(lambda buf: buf.name and os.path.exists(buf.name), vim.buffers)
		def createCandidate(buf):
			filePath = buf.name
			fileName = os.path.basename(filePath)
			return FileCandidate(name = "%s\t %s"%(fileName, filePath), key = fileName, path = filePath)
		return map(createCandidate, buffers)

	@staticmethod
	def getRecentlyCandidates():
		return []

	@staticmethod
	def addToRecentCandidates(fileCandidate):
		pass

class FileFinder(TrieFinder):
	def query(self, userInput):
		return self.queryRecent(userInput) + TrieFinder.query(self, userInput)

	def queryRecent(self, userInput):
		candidates = FileCandidateManager.getBufferCandidates() + FileCandidateManager.getRecentlyCandidates()
		def match(candidate):
			return userInput is "" or userInput.lower() in os.path.basename(candidate.getPath()).lower()
		return filter(match, candidates)
		

class FileAcceptor(Acceptor):
	def __init__(self):
		pass

	def accept(self, fileCandidate, options = None):
		if options is "None":
			FileCandidateManager.addToRecentCandidates(fileCandidate)
			return self.editFile(fileCandidate)

	def selectWindow(self):
		vim.command("wincmd w") #try next window

	def editFile(self, fileCandidate):
		self.selectWindow()
		vim.command("silent e %s"%fileCandidate.getPath())
		#close the window
		return False
