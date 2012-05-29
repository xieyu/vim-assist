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
		self.refresh()

	def refresh(self):
		self.IsReady = False
		threading.Thread(target = self.doRefresh).start()

	def doRefresh(self):
		self.candidateManager.refresh()
		candidates = self.candidateManager.getCachedCandidates()
		self.finder.setCandidates(candidates)
		print "refresh is done"
		self.IsReady = True
	
	def find(self):
		if not self.IsReady:
			print "scaning files, not ready yet :(, why not have a coffee break now.."
			return
		matcher = SharedFactory.getMatchController(title ="Go-to-file", finder = self.finder, acceptor = self.acceptor)
		matcher.show()


class FileCandidateManager:
	def __init__(self, reposFile):
		self.reposFile = reposFile
		self.rootPathList = self.parse(self.reposFile)
		self.cachedCandidates = []

	def parse(self, reposFile):
		return [line.strip()  for line in open(reposFile).readlines() if line.strip()[0]!="#"]

	def refresh(self):
		if self.rootPathList is None:
			return None
		self.cachedCandidateList = []
		for rootPath in self.rootPathList:
			print rootPath
			if not os.path.exists(rootPath):
				print "%s is not exists"%rootPath
			for root, dirs, files in os.walk(rootPath):
				for filePath in files:
					filePath = os.path.join(root, filePath)
					fileName = os.path.basename(filePath)
					iterm = FileCandidate(name = "%s\t %s"%(fileName, filePath), content = fileName.lower(), filePath = filePath)
					self.cachedCandidates.append(iterm)
		return self.cachedCandidates
	
	def getCachedCandidates(self):
		return self.cachedCandidateList	

