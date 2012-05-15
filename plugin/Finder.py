
class Query:
	def __init__(self, pattern, critic, queryContainsCompare = None):
		self.pattern = pattern
		self.critic = critic
		self.queryContainsCompare = queryContainsCompare

	def getPattern(self):
		return self.pattern

	def setPattern(self, pattern):
		self.pattern = pattern

	def contains(self, anotherQuery):
		"use for Optimize search"
		if self.queryContainsCompare:
			return self.queryContainsCompare(self.pattern, anotherQuery.pattern)
		return False

	def isHappyWith(self, content):		
		return self.critic(content, self.pattern)

class ScanFinder:
	def __init__(self, candidates, queryCritic, queryContainsCompare = None):
		self.candidates = candidates
		self.suitCandidates= []
		self.queryCritic= queryCritic
		self.queryContainsCompare = queryContainsCompare
		self.lastQuery = None

	def query(self, userInput):
		query = Query(userInput, self.queryCritic, self.queryContainsCompare)
		searchIterms = self.candidates
		if self.lastQuery and query.contains(self.lastQuery):
			searchIterms = self.suiteCandidates
		self.suiteCandidates = filter(lambda iterm : query.isHappyWith(iterm.getContent()), searchIterms)
		self.lastQuery = query
		return [iterm.getName() for iterm in self.suiteCandidates]

	def getSuiteCandidate(self, index):
		try:
			return self.suiteCandidates[index]
		except:
			return None

	def getSuiteCandidateNum(self):
		return len(self.suiteCandidates)

class CandidatesFactory:
	@staticmethod
	def createForCurBuffer():
		#TODO:we need get current buffer's name
		contents = VimUtils.getCurBufferContent()
		filePath = VimUtils.getCurBufferName()
		#construct candidate for every line, we also need filename
		lineNum = 0
		candidates = []
		for line in contents:
			lineNum += 1
			name = "%d:%s"%(lineNum, line.strip())
			item = Candidate(name = name, content = line, pos = (lineNum, 0),filePath = filePath)
			
			candidates.append(item)
		return candidates

	@staticmethod
	def createForReposPath():
		reposMg = ReposManager(settingManager.getReposConfigureFilePath())
		candidates = []
		try:
			reposPaths = reposMg.getReposPaths()
			for repos in reposPaths:
				for root, dirs, files in os.walk(repos):
					for filePath in files:
						filePath = os.path.join(root, filePath)
						item = Candidate(name = filePath, content = filePath, filePath = filePath)
						candidates.append(item)
			return candidates
		except:
			return []

class FinderFactory:
	def createCurBufferScanFinder():
		pass
	def createFileFinder():
		pass
	def getReposFileFinder():
		pass
	def getReposWordFinder():
		pass
