if !has("python")
    echo "need python support!"
    finish
endif

"SETUP PATH
let s:pluginPath= escape(expand('<sfile>:p:h'), '\')
let g:assistHome= s:pluginPath."/../Assist/"

function! RunPyFile(filename)
	exec "pyfile ".g:assistHome."python/".a:filename
endfunction

call RunPyFile("Common.py")
"load python files
call RunPyFile("VimUi.py")
"call RunPyFile("GitAssist.py")
call RunPyFile("HistoryAssist.py")
"call RunPyFile("GtagsAssist.py")
"call RunPyFile("BufferListAssist.py")
function! SearchHistory()
	call RunPyFile("VimUi.py")
	call RunPyFile("HistoryAssist.py")
	python vimAssistSearchWindow = SearchWindow(HistoryAssist())
	python vimAssistSearchWindow.createShowBuffer("vimAssistSearchWindow")
endfunction


"Commands:"
"gtags command
command! -nargs=1 SearchSymbolRef      py GtagsAssist.searchSymbolRef(<q-args>)
command! -nargs=1 SearchSymbolDefine   py GtagsAssist.searchSymbolDefine(<q-args>)
command! -nargs=1 SetGtagsWorkdir      py GtagsAssist.setWorkdir(<q-args>)
command! -nargs=1 SearchFile		   py GtagsAssist.searchFile(<q-args>)

"gtags history
command! SearchGtagsHistory            py GtagsHistory.searchHot()
command! ClearGtagsHistory             py GtagsHistory.clear()
command! EditGtagsHisotry              py GtagsHistory.edit()

"recent files
command! SearchHistoryHot              py call SearchHistory()
command! EditHistory                   py HistoryAssist.edit()
"au BufRead,BufNewFile * 			   py HistoryAssist.add()

"search quick in bufferlist
command! SearchBufferListHot		   py BufferListAssist.searchHot()
command! Test                          py HotSearchTest()

"Gik
command! Gkblame                    py GitAssist.gitkCurrentLine()
command! Gklog                      py GitAssist.gitkLogCurrentBuffer()
command! -nargs=* Gitk              py GitAssist.gitkCmd(<q-args>)

"command! MakeFilePathTags              py WalleTagsManager.makeFilePathTags()

"command! ChangeBetweenHeaderAndCFile py SearchAssist.changeBetweenHeaderAndcFile(<q-args>)
"Maps:

nmap <leader>r :call SearchHistory()<CR>
nmap <leader>b :SearchBufferListHot<CR>
nmap <leader>l :SearchGtagsHistory<CR>


nmap <leader>gs :SearchSymbolRef <C-R>=expand("<cword>")<CR><CR>
nmap <leader>gd :SearchSymbolDefine <C-R>=expand("<cword>")<CR><CR>
nmap <leader>gf :SearchFile <C-R>=expand("<cword>")<CR><CR>
"nmap <leader>ga :ChangeBetweenHeaderAndCFile<CR>

nmap<leader>gp :Gklog<CR>
nmap<leader>gl :Gkblame<CR>
