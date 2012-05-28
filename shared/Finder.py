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
		self.suiteCandidates=[]
		self.trieTree = TrieTree()

	def addCandidates(self, candidateList):
		for candidate in candidateList:
			self.trieTree.add(candidate.getContent(), candidate)
	
	def setCandidates(self, candidatesList):
		self.trieTree = TrieTree()
		self.suiteCandidates = []
		self.addCandidates(candidatesList)

	def query(self, word):
		self.suiteCandidates = self.trieTree.query(word)
		return [iterm.getName() for iterm in self.suiteCandidates]

	def getSuiteCandidate(self, index):
		try:
			return self.suiteCandidates[index]
		except:
			return None

class TrieTree:
	def __init__(self):
		self.root = {}
		self.leafName = "__TRIE_TREE_LEAFE_NAME__"

	def query(self, prefixOfKey):
		node = self.root
		for w in prefixOfKey:
			if node.has_key(w):
				node = node[w]
			else:
				node = None
				break
		if node:
			return self.getValuesOfAllChild(node)

	def add(self, key, value):
		iterator = self.root
		for char in key:
			if not iterator.has_key(char):
				iterator[char] = {}
			iterator = iterator[char]
			iterator[self.leafName] = value

	def getValuesOfAllChild(self, node):
		values = []
		#leafNode
		if node.has_key(self.leafName):
			values.append(node[self.leafName])
		#internal node
		values.extend([self.getValuesOfAllChild(node[key]) for key in node.keys()])

		return values

class SuffixTree:
	class Node:
		pass

	def __init__(self):
		self.root = {}
		self.active_point = None
		self.reminder = 1
		pass

	def query(self, subStringOfKey):
		pass

	def add(self, key, value):
		for i in range(len(key)):
			self.addPrefix(key[0:i], value)
		pass
	
	#private
	def addPrefix(self, prefix, value):
		pass

class SuffixTreeFinder:
	pass

