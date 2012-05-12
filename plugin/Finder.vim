"Descrption: vim plugins for Find files in bundles with regular expression
"Author:     xieyu3 at gmail dot com
"
"Usage:      in .vimrc, set g:paths and g:pathSep, like this way:
"            let g:paths="path1:path2:path3"
"            let g:pathSep=":"
" 			 in windows, you can set pathSep to ';' or whatever you like
"
"		     press <ctrl-f> to active the query, if find something,it  will show a
"		     output window that list the Found file path. 
"
"		     In output window, move to the line that you want open, press <Eneter> 
"		     to hide the output window and show that File in last window. 
"
"		     press <Space> 's behavior is same with <Enter> But keep the
"		     output window.


"Settings:
let g:paths="/Users/ic/codes/:/Users/ic/demos:/Users/ic/.vim"
let g:pathsSep=":"

"Maps:
map <C-f> :py findWord()<CR>

python<<EOF
import vim
import os
import sys
import re

scriptdir = os.path.dirname(vim.eval('expand("<sfile>")'))
if scriptdir not in sys.path:
    sys.path.insert(0, scriptdir)

import MyFinder
import VimUi


#vim.command("noremap <silent> <C-f> :py findWord()<CR>")

#a global window that is shared, reNew it before use it
promptWindow = VimUi.PromptWindow("promptWindow")

def findWord():
	candidates = VimUi.Utils.getCurrentBufferContent()
	def fuzzyCompare(pattern, line):
		return pattern in line
	finder = wordFinder(candidates, fuzzyCompare)
	matchWindow =MatchWindow("match",promptWindow, finder)

class MatchWindow:
	def __init__(self, title, window, finder):
		self.window = window
		self.window.reNew(title, self.userInputListener)
		self.finder = finder
		self.window.show()

	def userInputListener(self, userInput):
		result = self.finder.query(userInput)
		self.window.setContent(result)

class wordFinder:
	def __init__(self, candidates, compare):
		self.candidates = candidates
		self.compare = compare

	def query(self, pattern):
		return filter(lambda x : self.compare(pattern, x), self.candidates)
EOF
	
