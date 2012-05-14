#a simple abstract layer of VIm intereface
#Author: xieyu3 at gmail dot com 
#License: BSD

import vim
import string
from SettingManager import settingManager

class VimWidget:
	def __init__(self, bufferName):
		self.bufferName = bufferName
		self.create(self.bufferName)
		self.minHeight = None
		self.maxHeight = None
		self.options = None

	def close(self):
		try:
			bufferId = int(vim.eval("bufnr('%s')"%self.bufferName))
			if bufferId != -1:
				vim.command("bdelete! %d"%bufferId)
		except:
			pass
	
	def create(self, bufferName):
		#close the old one, if it exists
		self.close() 
		#create a new buffer on bottom
		vim.command("bo sp %s"%bufferName) 
		self.bufferId = int(vim.eval("bufnr('%')"))
		self.windowId = int(vim.eval("winnr()"))
		for b in vim.buffers:
			if b.number == self.bufferId:
				self.buffer = b
		for w in vim.windows:
			if w.buffer.number == self.bufferId:
				self.window = w

	def setContent(self, content):
		self.unlock()
		self.buffer[:] = content
		self.lock()
		self.updateWindowHeight()

	def getContent(self):
		return self.buffer[:]

	def setOptions(self, options):
		self.options=options
		for option in self.options:
			vim.command("setlocal %s"%option)

	def setHeight(self, height):
		self.window.height = height

	def setHeightRange(self, minHeight, maxHeight):
		self.minHeight = minHeight
		self.maxHeight = maxHeight
		self.setHeight(max(self.minHeight, min(self.maxHeight, len(self.buffer))))

	def updateWindowHeight(self):
		if self.minHeight and self.maxHeight:
			self.setHeight(max(self.minHeight, min(self.maxHeight, len(self.buffer))))

	def show(self):
		vim.command("redraw")
	
	def lock(self):
		if self.options and "nomodifiable" in self.options:
			vim.command("setlocal nomodifiable")

	def unlock(self):
		vim.command("setlocal modifiable")

#Window that can register key map
class Window:
	def __init__(self, selfName, title=None):
		'''selfName is a hack for in vim, so we can call self member function, it should be the same with your var
		   for example: window = Window("window", title), *make sure python can access the name from glaobal scope*
		   it is used in self.doMapMemberFunction function.
		'''
		self.selfName = selfName
		self.title = title
		self.widget = None
		self.keyMaps = []
		self.content = []
		self.options = []
		self.minHeight = 5
		self.maxHeight = 15

	def reNew(self, title):
		#TODO:dup code, ugly here
		self.title = title
		self.widget = None
		self.keyMaps = []
		self.content = []
		self.options = []
		self.minHeight = 5
		self.maxHeight = 15

	def setSelfName(self, selfName):
		self.selfName = selfName

	def getSelfName(self, selfName):
		return self.selfName

	def setContent(self, content):
		self.content = content
		if self.widget:
			self.widget.setContent(self.content)

	def getContent(self):
		return self.content

	def setOptions(self, options):
		self.options = options
		if self.widget:
			self.widget.setOptions(options)

	def setHeightRange(self, minHeight, maxHeight):
		self.minHeight = minHeight
		self.maxHeight = maxHeight
		if self.widget:
			self.widget.setHeightRange(minHeight, maxHeight)

	def show(self):
		self.widget = VimWidget(self.title)
		self.makeKeysMap()
		self.synWithWidget()
		for (key, function, param) in self.keyMaps:
			self.doMap(key, function, param)

	def close(self):
		vim.command(":close")

	def registerKeyMap(self, key, function, param=None):
		self.keyMaps.append((key, function, param))

	#private functions
	def doMap(self, key, function, param=None):
		if param is None:
			#vim.command("noremap <silent> <buffer> %s :py %s()<CR>"%(key, function))
			vim.command("noremap  <buffer> %s :py %s()<CR>"%(key, function))
		else: 
			#vim.command('''noremap <silent> <buffer> %s :py %s("%s")<CR>'''%(key, function, param))
			vim.command('''noremap  <buffer> %s :py %s("%s")<CR>'''%(key, function, param))

	def registerMemberFunction(self, key, function, param=None):
		functionName = "%s.%s"%(self.selfName, function)
		self.registerKeyMap(key, functionName, param)

	def synWithWidget(self):
		if self.widget:
			self.widget.setContent(self.content)
			self.widget.setOptions(self.options)
			self.widget.setHeightRange(self.minHeight, self.maxHeight)

#window that with prompt line
class PromptWindow(Window):
	'''window with prompt line, which is used for get user input immediately, 
	it will call listener when user input changed
	'''
	def __init__(self, selfName, title=None, listener = None):
		Window.__init__(self, selfName, title)
		self.prompt = Prompt(listener)
		self.settingScope = "PromptWindow"

	def reNew(self, title, listener):
		Window.reNew(self, title)
		self.prompt = Prompt(listener)
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

		#note: we can not direct pass key to function in vim, so map it with values
		commands = ["cancel", "bs", "del", "left", "right", "home", "end", "kill"]
		for com in commands:
			key = settingManager.getScopeKeyMap(self.settingScope, com)
			if key:
				self.registerMemberFunction(key, 'doCommand', com)

	def close(self):
		Window.close(self)
		self.prompt.close()

	def handleNormalKey(self, key):
		self.prompt.add(key)

	def doCommand(self, com):
		handler={"cancel":self.close,
				"bs": self.prompt.backspace,
				"del":self.prompt.delete,
				"right":self.prompt.cursorRight,
				"left":self.prompt.cursorLeft,
				"kill" :self.prompt.killToEnd,
				"home" :self.prompt.cursorStart,
				"end" :self.prompt.cursorEnd
				}[com]
		handler()

class Prompt:
	def __init__(self, listener):
		self.content=[]
		self.listener = listener
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
			self.redraw()
			self.notify()

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
		self.redraw()

	def cursorEnd(self):
		self.col=len(self.content)
		self.redraw()

	def cursorLeft(self):
		self.moveCursor(-1)
		self.redraw()

	def killToEnd(self):
		self.content = self.content[0:self.col]
		self.redraw()
		self.notify()

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

	def close(self):
		self.clear()
		vim.command("redraw")
		vim.command("echo")

	def notify(self):
		self.listener(self.getContent())

	def getContent(self):
		return "".join(self.content)

	def moveCursor(self, step):
		self.col += step
		if self.col < 0:
			self.col = 0
		if self.col > len(self.content):
			self.col = len(self.content)
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
			right = "".join(self.content[self.col + 1: len(self.content)])
		return (left, cursor, right)

