"Descrption: vim plugins for Find files in bundles
"Author:     xieyu3 at gmail dot com
"
"Commands:
"
"Options:
"
"Maps:
map <C-f> :py findInCurrentBuffer()<CR>

python<<EOF
import os
import sys
import vim
scriptdir = os.path.dirname(vim.eval('expand("<sfile>")'))
if scriptdir not in sys.path:
    sys.path.insert(0, scriptdir)

import VimUi
import CompareUtils
from Candidates import Candidate
from Candidates import CandidatesFactory
from Finder import ScanFinder
import Controller

finder_promptWindow = VimUi.PromptWindow("finder_promptWindow")
finder_matchController = Controller.MatchController("finder_matchController")

def findInCurrentBuffer():
	candidates = CandidatesFactory.createForCurBuffer()
	findAndShow(candidates,  queryCritic = CompareUtils.fuzzyCompare, queryContainsCompare = CompareUtils.fuzzyCompare)

def findAndShow(candidates, queryCritic = CompareUtils.containCompare, queryContainsCompare = None):
	"""
	queryCritic is used for select candidate, and queryCompare is used for Optimaze query.
	if lastQuery is containted by this one, so we only need to search in search results.
	"""
	finder = ScanFinder(candidates, queryCritic, queryContainsCompare)
	finder_matchController.reNew("match", finder, finder_promptWindow)
	finder_matchController.show()
EOF
	
