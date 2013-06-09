import vim
import os
import sys
def initVimAssist():
    assistHome = vim.eval("g:assistHome")
    sys.path.append(os.path.abspath(assistHome + "python"))

initVimAssist()

