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

call RunPyFile("Init.py")
call RunPyFile("Common.py")
call RunPyFile("VimUi.py")
call RunPyFile("StoreManager.py")
call RunPyFile("CodeSearch.py")
call RunPyFile("BufferSearch.py")
call RunPyFile("Locate.py")
call RunPyFile("Gitk.py")


"Commands:
"buffer search
command! -nargs=? Bs                     py BufferSearch.instance().search(<q-args>)
command! -nargs=? Bsa                    py BufferSearch.instance().searchAll(<q-args>)

"code search
command! -nargs=? Cs                     py CodeSearch.instance().search(<q-args>)
command! -nargs=1 -complete=dir Cscd     py CodeSearch.instance().setSearchDir(<q-args>)
command! -nargs=1 -complete=dir Cindex   py CodeSearch.instance().makeIndex(<q-args>)

"Locate file
command! -nargs=? L                      py Locate.instance().search(<q-args>)
command! -nargs=? -complete=dir Lcd      py Locate.instance().setSearchDir(<q-args>)
command! Lswitch                         py Locate.instance().switchHeadAndImpl()

"Gitk
command! Gkblame                         py Gitk.gitkCurrentLine()
command! Gklog                           py Gitk.gitkLogCurrentBuffer()
command! -nargs=* Gitk                   py Gitk.gitkCmd(<q-args>)
