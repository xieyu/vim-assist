import os
import threading

from Factory import SharedFactory
from Finder import TrieFinder
from Candidates import FileCandidate
import Acceptor

class FileFinder:
	def __init__(self, reposFile):
		self.candidateManager = FileCandidateManager(reposFile)
		self.finder = TrieFinder()
		self.acceptor = Acceptor.FileAcceptor()
		self.lock = threading.Lock()
		self.refresh()

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
	
	def find(self):
		matcher = SharedFactory.getMatchController(title ="Go-to-file", finder = self.finder, acceptor = self.acceptor)
		matcher.show()


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
			return None
		self.cachedCandidates = []
		for rootPath in self.rootPathList:
			if not os.path.exists(rootPath):
				print "%s is not exists"%rootPath
			for root, dirs, files in os.walk(rootPath):
				for filePath in files:
					filePath = os.path.join(root, filePath)
					fileName = os.path.basename(filePath)
					iterm = FileCandidate(name = "%s\t %s"%(fileName, filePath), key = fileName.lower(), filePath = filePath)
					self.cachedCandidates.append(iterm)
	
	def getCachedCandidates(self):
		return self.cachedCandidates	

