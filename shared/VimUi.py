#a simple abstract layer of VIm intereface
#Author: xieyu3 at gmail dot com 
#License: BSD

import vim
import string

class Widget:
	def __init__(self, bufferName):
		self.bufferName = bufferName
		self.options = []
		self.content = []
		#TODO:get it for setting manager
		self.minHeight = 4
		self.maxHeight = 15
		self.height = 4
		self.cursor = (1,1)
		self.vimBuffer = None
		self.vimWindow = None

	def close(self):
		#have bugs here, need make sure that current buffer is self.
		initial = vim.current.window
		for i in range(len(vim.windows)):
			vim.command("wincmd w")
			if vim.current.window == self.vimWindow:
				break
		try:
			vim.command("noa bun!")
		except:
			vim.command("noa close!")

		for i in range(len(vim.windows)):
			vim.command("wincmd w")
			if vim.current.window == initial:
				break

	
	def show(self):
		vim.command("noa keepa bo 5new %s"%self.bufferName) 
		self.vimBuffer = vim.current.buffer
		self.vimWindow = vim.current.window
		self.synSettingWithVim()
		vim.command("redraw")

	def setContent(self, content):
		self.content = content
		self.updateContent()

	def getContent(self):
		return self.content

	def getHeight(self):
		return self.height

	def setOptions(self, options):
		self.options = options
		self.updateOptions()

	def addOptions(self, options):
		self.options.extend(options)
		self.updateOptions()


	def setHeight(self, height):
		self.height = height
		self.updateHeight()

	def setCursor(self, line, col):
		self.cursor = (line, col)
		self.updateCursor()

	def setHeightRange(self, minHeight, maxHeight):
		self.minHeight = minHeight
		self.maxHeight = maxHeight
		self.updateWindowHeight()

	#private:
	def updateOptions(self):
		#FIXME: does it matter of dup setings?
		if self.vimBuffer:
			for option in self.options:
				vim.command("setlocal %s"%option)

	def updateContent(self):
		if self.vimBuffer:
			self.unlock()
			self.vimBuffer[:] = self.content
			self.lock()
			self.updateWindowHeight()

	def updateHeight(self):
		if self.vimWindow:
			self.vimWindow.height = self.height

	def updateCursor(self):
		if self.vimWindow:
			self.vimWindow.cursor = self.cursor

	def synSettingWithVim(self):
		self.updateContent()
		self.updateOptions()
		self.updateHeight()
		self.updateCursor()

	def updateWindowHeight(self):
		if self.minHeight and self.maxHeight:
			if self.maxHeight < 0:
				maxheight = len(self.content)
			else:
				maxheight = min(self.maxHeight, len(self.content))
			self.setHeight(max(self.minHeight, maxheight))
	
	def lock(self):
		if self.options and "nomodifiable" in self.options:
			vim.command("setlocal nomodifiable")

	def unlock(self):
		vim.command("setlocal modifiable")

#Window that can register key map
class Window(Widget):
	def __init__(self, selfName, title=None):
		'''
		self.selfName is a hack for use memberFunction for vim keyMap, 
		it will call the instance's memeber fuction in following way
		:py selfName.memberFunction(), 
		So make sure that python can access the it in global scope
		'''
		Widget.__init__(self, title)
		self.selfName = selfName
		self.keyMaps = []

	def setSelfName(self, selfName):
		self.selfName = selfName

	def reNew(self, title):
		Widget.__init__(self, title)
		self.keyMaps = []


	def show(self):
		Widget.show(self)
		for (key, function, param) in self.keyMaps:
			self.doMap(key, function, param)

	def registerKeyMap(self, key, function, param=None):
		self.keyMaps.append((key, function, param))

	#private functions
	def registerMemberFunction(self, key, function, param=None):
		functionName = "%s.%s"%(self.selfName, function)
		self.registerKeyMap(key, functionName, param)

	def doMap(self, key, function, param=None):
		if param is None:
			vim.command("nnoremap <silent> <buffer> %s :py %s()<CR>"%(key, function))
		else: 
			vim.command('''nnoremap <silent> <buffer> %s :py %s("%s")<CR>'''%(key, function, param))


#window that with prompt line
class PromptWindow(Window):
	'''window with prompt line, which is used for get user input immediately, 
	it will call listener when user input changed
	'''
	def __init__(self, selfName, title=None, listener = None):
		Window.__init__(self, selfName, title)
		self.settingScope = "PromptWindow"
		self.prompt = Prompt(listener)
		#command: function
		self.commandMap ={"cancel":self.close,
				"bs": self.prompt.backspace,
				"del":self.prompt.delete,
				"delWord" :self.prompt.delWord,
				"right":self.prompt.cursorRight,
				"left":self.prompt.cursorLeft,
				"start" :self.prompt.cursorStart,
				"end" :self.prompt.cursorEnd
				}
		#command: keysmap
		self.keysMap = {
				"cancel":["<esc>", "<c-c>", "<c-g>"],
				"bs":["<BS>","<c-]>"],
				"del":["<del>"],
				"delWord": ["<c-w>"],
				"left": ["<c-h>", "<left>"],
				"right": ["<c-l>", "<right>"],
				"start":["<c-a>"],
				"end": ["<c-e>"],
			}

	def reNew(self, title, listener):
		Window.reNew(self, title)
		self.prompt.clear()
		self.prompt.setListener(listener)
		self.makeKeysMap()


	def getUserInput(self):
		return self.prompt.getContent()

	def setListener(self, listener):
		self.prompt.setListener(listener)

	#private
	def makeKeysMap(self):
		#normal keys
		punctuation ='<>`@#~!"$%&/()=+*-_.,;:?\\\'{}[] ' # and space excpet "|"
		for key in string.letters + string.digits + punctuation:
			self.registerMemberFunction("<Char-%d>"%ord(key),'handleNormalKey',key)

		for com in self.commandMap.keys():
			keys = self.keysMap[com]
			for key in keys:
				self.registerMemberFunction(key, 'doCommand', com)

	def close(self):
		Window.close(self)
		self.prompt.close()

	def handleNormalKey(self, key):
		self.prompt.add(key)

	def doCommand(self, com):
		self.commandMap[com]()

class Prompt:
	def __init__(self, listener):
		self.content=[]
		self.listener = listener
		self.col = 0
	
	def clear(self):
		self.content=[]
		self.col = 0
	
	def setListener(self, listener):
		self.listener = listener

	def add(self, key):
		self.content.append(key)
		self.moveCursor(1)
		self.redraw()
		self.notify()

	def clear(self):
		self.content=[]
		self.col = 0
		self.redraw()

	def backspace(self):
		if self.col > 0:
			self.content.pop(self.col-1)
			self.moveCursor(-1)
			self.notify()
			self.redraw()

	def delete(self):
		if self.col >=0 and self.col < len(self.content):
			self.content.pop(self.col)
			self.moveCursor(-1)
			self.redraw()
			self.notify()

	def cursorRight(self):
		self.moveCursor(1)
		self.redraw()

	def cursorStart(self):
		self.col=0
		self.notify()
		self.redraw()

	def cursorEnd(self):
		self.col=len(self.content)
		self.notify()
		self.redraw()

	def cursorLeft(self):
		self.moveCursor(-1)
		self.redraw()

	def delWord(self):
		try:
			left = self.content[0:self.col]
			try:
				right = self.content[self.col:-1]
				right = right[right.index(" ") : -1]
			except:
				right = []
			self.content = left + right
			self.redraw()
			self.notify()
		except:
			pass

	def close(self):
		self.clear()
		vim.command("redraw")
		vim.command("echo")

	#private
	def redraw(self):
		prompt = ">>"
		prompt_highlight = "Comment"
		cursor_highlight = "Cursor"
		normal_heiglight = "Normal"
		left, cursor, right = self.segContent()
		drawMaps=[(prompt, prompt_highlight), (left, normal_heiglight), (cursor, cursor_highlight),(right,normal_heiglight)]
		vim.command("redraw")
		for text, highlight in drawMaps:
			if text is not "":
				#note: echohl don't need escape with quote
				vim.command("echohl %s"%highlight)
				vim.command("echon '%s'"%text)
		vim.command("echohl None")


	def notify(self):
		self.listener(self.getContent())

	def getContent(self):
		return "".join(self.content)

	def moveCursor(self, step):
		self.col += step
		self.col = min(max(self.col, 0), len(self.content))
		self.notify()

	def segContent(self):
		empty=""
		whiteSpace=' '
		#cousor should be a whitespace char at end
		left, cursor, right = (empty, whiteSpace, empty)
		if self.content is []:
			return (left, cursor, right)

		left=empty.join(self.content[0:self.col])
		if self.col < len(self.content):
			cursor = str(self.content[self.col])
			right = empty.join(self.content[self.col + 1: len(self.content)])
		return (left, cursor, right)

