#a simple abstract layer of VIm intereface
#Author: xieyu3 at gmail dot com 
#License: BSD

import vim
import sys
import os

class UI:
	def __init__(self, title):
		self.title = title
		self.widget = None
		self.contents= []
		self.minHeight = 5
		self.maxHeight = 8

	def createWidget(self):
		self.widget = VimWidget(self.title)
		self.widget.setHeight(max(self.minHeight, min(self.maxHeight, len(self.contents))))

	def show(self):
		if self.widget is None:
			self.createWidget()
		self.widget.setContents(self.contents)
		self.widget.show()
	#set min and max lines of the ui's height
	def setHeightRange(minHeight, maxHeight):
		self.minHeight = minHeight
		self.maxHeight = maxHeight

	def setContents(self, contents):
		self.contents = contents

class VimWidget:
	def __init__(self, bufferName):
		self.bufferName = bufferName
		self.create(self.bufferName)

	def close(self, bufferName):
		bufferId = int(vim.eval("bufnr('%s')"%bufferName))
		print bufferId
		print bufferName
		if bufferId != -1:
			vim.command("bdelete! %d"%bufferId)
	
	def create(self, bufferName):
		#close the old one, if it exists
		#TODO:avoid kill the buffer that opened by User
		self.close(self.bufferName) 
		vim.command("bo sp %s"%bufferName) #create a new buffer on bottom
		self.bufferId = int(vim.eval("bufnr('%')"))
		self.windowId = int(vim.eval("winnr()"))
		for b in vim.buffers:
			if b.number == self.bufferId:
				self.buffer = b
		for w in vim.windows:
			if w.buffer.number == self.bufferId:
				self.window = w

	def getBuffer(self):
		return self.buffer

	def setHeight(self, height):
		self.window.height = height

	def setContents(self, contents):
		self.buffer[:] = contents

	def setBufProp(self, varname,value):
		vim.eval('setbufvar(%d,"%s","%s")'%self.bufferId, str(varname), str(value))

	def getBufProp(self, varname):
		return vim.eval('getbufvar(%d,"%s")'%self.bufferId, str(varname))

	def setWindowProp(self, varname,value):
		vim.eval('setwinvar(%d,"%s","%s")'%(self.bufferId, str(varname), str(value)))

	def getWindowProp(self, varname):
		return vim.eval('getwinvar(%d,"%s")'%self.bufferId, str(varname))

	def show(self):
		vim.command("redraw")
	

def bufferExists(bufferName):
	return int(vim.eval("bufexists('%s')"%bufferName))

def openInWindow(windowId, hideCurrent):
	filePath = vim.current.line
	if(os.path.exists(filePath)):
		if hideCurrent:
			vim.command("hide") #hide current window
		vim.command("%d wincmd w"%windowId) #move focus to windowId
		#TODO:handle when buffer is already loaded
		vim.command("e %s"%filePath)

