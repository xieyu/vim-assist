
map <C-s> :FindInLine<CR>
command FindInLine py findinLine()
python <<EOF
import os
import sys
import vim
#include shared lib to sys.path
for path in vim.eval("&runtimepath").split(','):
	lib = "%s/shared"%path
	if lib not in sys.path and os.path.exists(lib):
		sys.path.insert(0, lib)

scriptdir = os.path.dirname(vim.eval('expand("<sfile>")'))
if scriptdir not in sys.path:
    sys.path.insert(0, scriptdir)
from Factory import SharedFactory

from LineFinder import CurrentBufferLineFinder
lineFinder = CurrentBufferLineFinder()

def findinLine():
	lineFinder.find()
EOF
