
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
