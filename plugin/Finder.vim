"Descrption: vim plugins for Find files in bundles
"Author:     xieyu3 at gmail dot com
"
"Commands:
"
"Options:
"
"Maps:
map <C-b> :py findInCurrentBuffer()<CR>
map <C-f> :py findFilePaths()<CR>

python<<EOF
import os
import sys
import vim
scriptdir = os.path.dirname(vim.eval('expand("<sfile>")'))
if scriptdir not in sys.path:
    sys.path.insert(0, scriptdir)

import CompareUtils
from Factory import SharedFactory
from Factory import CandidatesFactory
from Finder import ScanFinder
import Acceptor

def findInCurrentBuffer():
	candidates = CandidatesFactory.createForCurBuffer()
	finder = ScanFinder(candidates, queryCritic = CompareUtils.fuzzyCompare, queryContainsCompare = CompareUtils.fuzzyCompare)
	acceptor = Acceptor.LineAcceptor()
	matcher = SharedFactory.getMatchController(title ="findCurrentBuffer", finder = finder, acceptor = acceptor)
	matcher.show()

def findFilePaths():
	candidates = CandidatesFactory.createForReposPath()
	finder = ScanFinder(candidates, queryCritic = CompareUtils.fuzzyCompare, queryContainsCompare = CompareUtils.fuzzyCompare)
	acceptor = Acceptor.FileAcceptor()
	matcher = SharedFactory.getMatchController(title ="findCurrentBuffer", finder = finder, acceptor = acceptor)
	matcher.show()

