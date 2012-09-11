import os
import threading
import vim
import json
from Finder import TrieFinder
from ctags import CTags, TagEntry
import ctags
import re

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

	def getDisplayName(self):
		return "%-40s\t%s"%(self.name, self.path)

class RecentManager:
	def __init__(self, recentConfig):
		self.recentConfig = recentConfig

	def addToRecent(self, fileCandidate):
		if fileCandidate not in self.recentCandidates:
			self.recentCandidates.append(fileCandidate)

		if os.path.isfile(self.recentConfig):
			os.remove(self.recentConfig)
		file =open(self.recentConfig, "w")
		for candidate in self.recentCandidates:
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
					candidate = FileCandidate(name = fileName, key = fileName, path = filePath)
					result.append(candidate)
		except:
			result = []
		return result

class ReposManager:
	def __init__(self, reposConfig):
		try:
			reposConfig = json.load(open(reposConfigFile), 'utf-8')
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


class FileCandidateManager:
	def __init__(self, reposManager, recentManager):
		self.recentManager = recentManager
		self.reposManager  = reposManager
		self.finder = FileFinder()
		self.finder.setIgnoreCase()
		self.lock = threading.Lock()

	def searchCandidate(self, pattern):
		return self.finder.query(pattern)

	def getKeysMap(self):
		return {"<cr>":"None","<2-LeftMouse>":"None"}

	def acceptCandidate(self, candidate, way):
		if way is "None":
			self.recent.addToRecent(candidate)
			vim.command("wincmd w") #try next window
			vim.command("silent e %s"%candidate.getPath())
		#close the window
		return False

	def onStart(self):
		recents = self.recentManager.getRecent()
		self.finder.setRecentCandidate(self.getBufferCandidates() + recents)

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
					iterm = FileCandidate(name = "%-40s\t%s"%(fileName, filePath), key = fileName, path = filePath)
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

	def getBufferCandidates(self):
		buffers = filter(lambda buf: buf.name and os.path.exists(buf.name), vim.buffers)
		def createCandidate(buf):
			filePath = os.path.normcase(buf.name)
			fileName = os.path.basename(filePath)
			return FileCandidate(name = "%-40s\t%s"%(fileName, filePath), key = fileName, path = filePath)

		return map(createCandidate, buffers)






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


class TagCandidate(FileCandidate):
	def __init__(self, name, key, filePath, lineNumber):
		FileCandidate.__init__(self, name, key, filePath)
		self.lineNumber = lineNumber

	def getlineNumber(self):
		return int(self.lineNumber)

	def getDisplayName(self):
		return "%-40s\t%s: %s"%(self.name, self.path, self.lineNumber)


class TagManager:
	def getActiveTag():
		pass

	def generateTag(Path):
		pass

class TagCandidateManager:
	def __init__(self, rencentManager):
		self.recent = rencentManager

	def setTagFile(self, tagFile):
		self.tagFilePath = tagFile
		self.tagFile=CTags(tagFile)

	def getAllEntryInKind(self, kind):
		entry = TagEntry()
		result = []
		while self.tagFile.next(entry):
			if entry['kind'] == kind:
				result.append(entry['name'])
		return result

	def getKeysMap(self):
		return {"<cr>":"None","<2-LeftMouse>":"None"}

	def findTagByFullName(self, name):
		entry = TagEntry()
		result = []
		if self.tagFile.find(entry, name, ctags.TAG_FULLMATCH):
			print entry['name']
			result.append(TagCandidate(entry['name'], entry['name'], entry['file'], entry['lineNumber']))
		while self.tagFile.findNext(entry):
			result.append(TagCandidate(entry['name'], entry['name'],entry['file'], entry['lineNumber']))
		return result

	def acceptCandidate(self, candidate, way):
		if way is "None":
			self.recent.addToRecent(candidate)
			vim.command("wincmd w") #try next window
			vim.command("silent e %s"%candidate.getPath())
		#close the window
