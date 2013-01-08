if !has("python")
    echo "need python support!"
    finish
endif

let s:plugin_path = escape(expand('<sfile>:p:h'), '\')
let g:walle_home = s:plugin_path."/../walle/"

function! RunPyFile(filename)
	exec "pyfile ".g:walle_home."Assist/".a:filename
endfunction

function! SetupPath()
python<<EOF
import sys
import os
import vim

walle_home = vim.eval("g:walle_home")
sys.path.append(os.path.abspath(walle_home))
EOF
endfunction

call SetupPath()
call RunPyFile("VimUi.py")
call RunPyFile("GitAssist.py")
call RunPyFile("HistoryAssist.py")
call RunPyFile("GtagsAssist.py")
call RunPyFile("BufferListAssist.py")


"Commands:"
command! -nargs=1 SearchSymbolRef      py GtagsAssist.searchSymbolRef(<q-args>)
command! -nargs=1 SearchSymbolDefine   py GtagsAssist.searchSymbolDefine(<q-args>)

command! -nargs=1 SearchFile		   py GtagsAssist.searchFile(<q-args>)

command! SearchBufferListHot		   py BufferListAssist.searchHot()
command! SearchHistoryHot              py HistoryAssist.searchHot()
"command! ChangeBetweenHeaderAndCFile py SearchAssist.changeBetweenHeaderAndcFile(<q-args>)


command! GitkcurrentLine               py GitAssit.gitkCurrentLine()
command! GitkLogp                      py GitAssit.gitkLogCurrentBuffer()

"command! MakeFilePathTags              py WalleTagsManager.makeFilePathTags()

au BufRead,BufNewFile * 			   py HistoryAssist.addToHistory()
"Maps:

nmap <leader>r :SearchHistoryHot<CR>
nmap <leader>b :SearchBufferListHot<CR>

nmap <leader>gs :SearchSymbolRef <C-R>=expand("<cword>")<CR><CR>
nmap <leader>gd :SearchSymbolDefine <C-R>=expand("<cword>")<CR><CR>
nmap <leader>gf :SearchFile <C-R>=expand("<cword>")<CR><CR>
"nmap <leader>ga :ChangeBetweenHeaderAndCFile<CR>

nmap<leader>gp :GitkLogp<CR>
nmap<leader>gl :GitkcurrentLine<CR>

