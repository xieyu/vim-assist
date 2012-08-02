class Finder:
	def __init__(self):
		self.suiteCandidates = []

	def setCandidates():
		assert not "Not implement"

	def addCandidates(candidates):
		assert not "Not implement"

	def query(self, word):
		assert not "Not implement"

	def getSuiteCandidate(self, index):
		try:
			return self.suiteCandidates[index]
		except:
			return None

	def getSuiteCandidateNum(self):
		return len(self.suiteCandidates)


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

	def isHappyWith(self, Key):		
		return self.critic(Key, self.pattern)

class ScanFinder(Finder):
	def __init__(self, queryCritic, queryContainsCompare = None):
		Finder.__init__(self)
		self.candidates = []
		self.queryCritic= queryCritic
		self.queryContainsCompare = queryContainsCompare
		self.lastQuery = None

	def setCandidates(self, candidates):
		self.candidates = candidates

	def query(self, userInput):
		query = Query(userInput, self.queryCritic, self.queryContainsCompare)
		searchIterms = self.candidates
		if self.lastQuery and query.contains(self.lastQuery):
			searchIterms = self.suiteCandidates
		self.suiteCandidates = filter(lambda iterm : query.isHappyWith(iterm.getKey()), searchIterms)
		self.lastQuery = query
		return map(lambda iterm: iterm.getName(), self.suiteCandidates)

class TrieFinder(Finder):
	def __init__(self):
		Finder.__init__(self)
		self.trieTree = TrieTree()

	def addCandidates(self, candidateList):
		for candidate in candidateList:
			self.trieTree.add(candidate.getKey(), candidate)
	
	def setCandidates(self, candidatesList):
		self.trieTree = TrieTree()
		self.suiteCandidates = []
		self.addCandidates(candidatesList)

	def query(self, word):
		if not word:
			return []
		self.suiteCandidates = self.trieTree.query(word.lower())
		return [iterm.getName() for iterm in self.suiteCandidates]

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
				return []
		if prefixOfKey == "acceptor.py":
			print node
		if node:
			return self.getValuesOfAllChild(node)

	def add(self, key, value):
		iterator = self.root
		for char in key:
			if not iterator.has_key(char):
				iterator[char] = {}
			iterator = iterator[char]
		if iterator.has_key(self.leafName):
			iterator[self.leafName].append(value)
		else:
			iterator[self.leafName] = [value]
	
	def getValuesOfAllChild(self, node):
		values = []
		#leafNode
		if node.has_key(self.leafName):
			values.extend(node[self.leafName])

		#internal node
		for key in node.keys():
			if key != self.leafName:
				values.extend(self.getValuesOfAllChild(node[key]))

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

