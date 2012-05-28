"Descrption: vim plugins for Find files in bundles
"Author:     xieyu3 at gmail dot com
"
"Commands:
"
"Options:
"
"Maps:
map <C-b> :py findInCurrentBuffer()<CR>
map <C-p> :py findFilePaths()<CR>
map <C-f> :py trieFinderFile()<CR>


if !exists("g:reposFile")
	let g:reposFile = "/Users/ic/.vim/bundle/finder/reposPaths"
endif

python<<EOF
import os
import sys
import vim
#include shared lib to sys.path
for path in vim.eval("&runtimepath").split(','):
	lib = "%s/shared"%path
	if lib not in sys.path and os.path.exists(lib):
		sys.path.insert(0, lib)

import CompareUtils
from Factory import SharedFactory
from Finder import ScanFinder
from Finder import TrieFinder
from Candidates import FileCandidate
import Acceptor

class FileCandidateManager:
	def __init__(self, reposFile):
		self.reposFile = reposFile
		self.rootPathList = self.parse(self.reposFile)
		self.cachedCandidateList = None

	def parse(self, reposFile):
		return [line.strip()  for line in open(reposFile).readlines() if line.strip()[0]!="#"]

	def createCandidateList(self):
		if self.rootPathList is None:
			return None
		candidateList = []
		for rootPath in self.rootPathList:
			print rootPath
			if not os.path.exists(rootPath):
				print "%s is not exists"%rootPath
			for root, dirs, files in os.walk(rootPath):
				for filePath in files:
					filePath = os.path.join(root, filePath)
					fileName = os.path.basename(filePath)
					item = FileCandidate(name = "%s\t %s"%(fileName, filePath), content = fileName.lower(), filePath = filePath)
					candidateList.append(item)
		return candidateList
	
	def getCachedCandidateList(self):
	#TODO: make it multithread ...
		if self.cachedCandidateList is None:
			self.cachedCandidateList = self.createCandidateList()

		return self.cachedCandidateList	

reposFile = vim.eval("g:reposFile")
fileCandidateManager = FileCandidateManager(reposFile)

def findFilePaths():
	candidates = fileCandidateManager.getCachedCandidateList()
	if candidates is None:
		print "scanning files, try latter"
	finder = ScanFinder(candidates, queryCritic = CompareUtils.fuzzyIgnoreCaseCompare, queryContainsCompare = CompareUtils.fuzzyCompare)
	acceptor = Acceptor.FileAcceptor()
	matcher = SharedFactory.getMatchController(title ="findCurrentBuffer", finder = finder, acceptor = acceptor)
	matcher.show()

def trieFinderFile():
	candidates = fileCandidateManager.getCachedCandidateList()
	if candidates is None:
		print "scanning files, try latter"
	finder = TrieFinder()
	finder.addCandidates(candidates)
	acceptor = Acceptor.FileAcceptor()
	matcher = SharedFactory.getMatchController(title ="findCurrentBuffer", finder = finder, acceptor = acceptor)
	matcher.show()
EOF

