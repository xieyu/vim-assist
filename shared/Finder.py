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

class TrieFinder:
	def __init__(self):
		self.root={}
		self.suiteCandidates=[]
		#to make it unique to avoid conflict with candidates
		self.leafName = "__TrieFinderCandidate__"

	def addCandidates(self, candidateList):
		for candidate in candidateList:
			iterator = self.root
			for char in candidate.getContent().lower():
				if not iterator.has_key(char):
					iterator[char]={}
				iterator = iterator[char]
			iterator[self.leafName] = candidate
		pass
	
	def setCandidates(self, candidatesList):
		self.root={}
		self.suiteCandidates = []
		self.addCandidates(candidatesList)

	def query(self, word):
		#self.suiteCandidates = self.prefixQuery(word)
		self.suiteCandidates = self.fuzzyQuery(word)
		return [iterm.getName() for iterm in self.suiteCandidates]

	def prefixQuery(self, word):
		node = self.root
		for w in word:
			if node.has_key(w):
				node = node[w]
			else:
				node = None
				break
		if node:
			return self.getAllChildCandidate(node)
		return []

	def fuzzyQuery(self, word):
		return self.doFuzzyQuery(self.root, word.lower())

	def doFuzzyQuery(self, node, word):
		result = []
		#if world is empty
		if not word:
			return result

		for i, w in enumerate(word):
			if node.has_key(w):
				node = node[w]
			else:
				#node is leafnode, so return [] if unmatch
				if node.has_key(self.leafName):
					return []
				#then ignore this unmatch, and research in all its child nodes 
				for key in node.keys():
					result.extend(self.doFuzzyQuery(node[key], word[i:-1]))
				return result

		if node:
			result.extend(self.getAllChildCandidate(node))
		return result

	def getAllChildCandidate(self, node):
		candidates = []
		if node.has_key(self.leafName):
			candidates.append(node[self.leafName])
			return candidates

		for key in node.keys():
			result = self.getAllChildCandidate(node[key])
			candidates.extend(result)

		return candidates


	def getSuiteCandidate(self, index):
		try:
			return self.suiteCandidates[index]
		except:
			return None

class SuffixTree:
	class Node:
		pass

	def __init__(self):
		self.root = {}
		self.active_point = None
		self.reminder = 1
		pass
	#private
	def addPrefix():
		pass
