import vim

"""
Acceptor is used for handle user's accept selection, It is used in MatchController, and should 
define follow intereface

"@interface
class Acceptor():
	def __init__(self):
		pass
	def accept(self, candidate, options = None):
		#if you want keep the MatchController window open:
		return True
"
you can register key map with option:
MatchController.addKeyMapForCommand("acceptSelect", keys, option):

@Attention: keys should be a list, and option should be a string.

in matchController the default key map that will triger accept is <cr>, and default option is None, 
"""
class Acceptor:
	def __init__(self):
		pass
	def getKeysMap(self):
		return {"<cr>":"None","<2-LeftMouse>":"None"}
	def accept(self, candidate, param):
		pass


class WorldAcceptor(Acceptor):
	def __init__(self):
		pass
	def accept(self, lineCandidate, options = None):
		pass
	def editFile(self, WordCandidate):
		pass

		


