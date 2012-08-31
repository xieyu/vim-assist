import copy
class Finder:
	def __init__(self):
		pass

	def query(self, key):
		assert not "Not implement"


class ScanFinder(Finder):
	def __init__(self, match):
		Finder.__init__(self)
		self.candidates = []
		self.match = match
		self.lastQuery = None
		self.containMatch = None

	def setCandidates(self, candidates):
		self.candidates = candidates

	def addCandidates(self, candidates):
		self.candidates.extend(candidates)

	def query(self, key):
		return filter(lambda item : self.match(key, item), self.candidates)

class TrieFinder(Finder):
	def __init__(self):
		Finder.__init__(self)
		self.trieTree = TrieTree()
		self.ignoreCase = False

	def setIgnoreCase(self):
		self.ignoreCase = True

	def addCandidates(self, candidates):
		for candidate in candidates:
			key = self.ignoreCase and candidate.getKey().lower() or candidate.getKey()
			self.trieTree.add(key, candidate)
	
	def setCandidates(self, candidates):
		self.trieTree = TrieTree()
		self.addCandidates(candidates)

	def query(self, word, maxNumber):
		if not word:
			return []
		word = self.ignoreCase and word.lower() or word
		return self.trieTree.query(word, maxNumber)

class TrieTree:
	def __init__(self):
		self.root = {}
		self.leafName = "__TRIE_TREE_LEAFE_NAME__"

	def query(self, prefixOfKey, maxNumber):
		node = self.root
		for w in prefixOfKey:
			if node.has_key(w):
				node = node[w]
			else:
				return []
		if node:
			return self.getValuesOfAllChild(node, maxNumber)

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
	
	def getValuesOfAllChild(self, node, maxNumber):
		values = []
		if maxNumber < 0 :
			return values

		#leafNode
		if node.has_key(self.leafName):
			maxNumber = maxNumber - len(self.leafName)
			values.extend(node[self.leafName])

		#internal node
		for key in node.keys():
			if maxNumber < 0:
				break
			if key != self.leafName:
				childs = self.getValuesOfAllChild(node[key], copy.copy(maxNumber))
				maxNumber = maxNumber - len(childs)
				values.extend(childs)

		return values
