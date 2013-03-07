#Assist for vim#
As a programmer, there always annoy things to do, such as find file to edit or search the sybmol where it is referenced and where is it defined. 
so I integrate some useful tools into vim, to make it more comfortable to use vim.

The world is under your finger, you can jump to anywhere freely, find what you need quicly, life is better with it, isn't it, haha.

###Require###
Require python and vim compled with python feature.

###Install###
recommand to use pathogen of vundle to install it

##Common intereface##
all tools in vim-assit  such as FileNavigation or historyFile search, will open a window to show the search result, In this window you can use following keymaps

* `<esc>`   close the search window
* `<enter>` open file under cursor and close the search window
* `<c-o>``  open file under cursor without close the search window, and jump to the window that open the file
* `<c-p>`   open file under cursor withtout close the search window, without jump to window that open the file
* `<c-j>`   select next one
* `<c-k>`   select pre one

##FileNavigation##
File navigation is used to quick search the files with stroke type, it's like command-T, or ctrl-p plugin, there are tow commands
``Fg`` and ``Fgdir``.

###Fndir###
command Fgdir will set the the FileNavigation search dir, the default is vim's current work dir. for example:
```
:Fndir ~/codes/demos/
```
by using it FileNavigation will search all the file under ``~/codes/demos``, instead of vim's current work dir

###Fnclear###
clear the searchPath set by Fndir

###Fn###
command Fg is used to search file with pattern, it accept zero or one args

for zero arg, it will list all the files under the searchPath in the searchWindow, then you can type some
stroke to do more filter the result.

if has args, it will list the file match the args instead of all the files under the searchPath

use example:
```
:Fn dom
```

##historyfile search##
Everyfile you edit, will be record. And then you can search it with key stroke, normally it just compare fileName with your input, but 
if there '/' in you input, it will compre the full path.

This assist provide these commands:
* SearchHistory  this command  will open the search window, then you can input something to search the file in history list
* EditHistory    this command  will open the a buffer, in which contains all the history file, you can edit it like normal file.

There also a keymap'<leader>r':
```
nmap <leader>r :SearchHistory<CR>
```
for `<leader>` you can see the detail by `:help leader`, normally I set `,` as `<leader>`:
by add follow in `.vimrc`
```
let mapleader=","
```

##Bookmark##
Bookmark is very useful when you have lot of code and tracing a bug.

###commands###
This assist provide commands:
* AddBookmark     this command will add the file and lineNum which the current cursor locate to bookmark.
* SearchBookMark  this command will open the search window, then you can search the bookmark
* EditBookMark,   Edit bookmark as normal file

a bookmark is in follow format:
```
filePath  lineNum  codeSnip
```

the bookmark exmaple:
```
~/codes/demos/foo.c  100  int main(int argc ,char* argv)
```

you can search with "foo", it will search the bookmark which fileName contains stroke 'foo', or you can 
search with "@main", it will search bookmark with codeSnip that contains stroke 'main'. and you can combine
use "foo@main", this will search bookmark which filename contain stroke 'foo', and codeSnip contain 'main'.

###keymaps###
There are a keymap `<leader>b` for SearchBookMark:
``
nmap <leader>b :SearchBookMark<CR>
``

##Gtags##
[gtags](http://www.gnu.org/software/global/) is very useful tool for search cpp, java, code.

###require###
This plugin require gtags installed. and generate gtags first. 

###generate gtags###
for example generate gtags for code under ``~/codes/demos``
```
$cd ~/codes/demos/
$gtags
```
###commands###
This Assist provide following commands
* GtagsSymbolRef    this command will search the place that reference the symbol.
* GtagsSymbolDefine this command will search the place where the symbol is defined.
* GtagsFile         this command will search file which in the pattern you just input.
* GtagsWorkdir      this command will set work dir for gtags

These commands require args. 
####usage####
* ``:GtagsSymbolRef symbol``
* ``:GtagsSymbolDefine symbol``
* ``:GtagsFile  filepattern``
* ``:GtagsWorkdir path/to/workdir/``

You can search file which contain 'canvas' by `:GtagsFile canvas`, 
then it will open a search window which list file that contains the 'canvas',
after that you can input some stroke to do more search in this filelist.

The way of use ``GtagsSymbolDefine`` and ``GtagsSymbolRef`` command is same as ``GtagsFile``, but except in
the search window you can search in the same way as Bookmark with format "filePath@codesnip",
see Bookmark section for detail

``:GtagsWorkdir ~/codes/demos/`` will make gtags search dir `~/codes/demos` for tags instead of cwd

###keymaps###
There also keymaps, which will search the word under current cursor, Attention there a space following 'GtagsFile'
```
nmap <leader>gs :GtagsSymbolRef <C-R>=expand("<cword>")<CR><CR>
nmap <leader>gd :GtagsSymbolDefine <C-R>=expand("<cword>")<CR><CR>
nmap <leader>gf :GtagsFile 
```

##Ctags##
ctags at here is used to quick jump to the define of symbol in current file.

###commands###
* CtagsSearchCurrentFile, this will list all the sybmol in the current file in the search window

###keymaps##
```
nmap <leader>c :CtagsSearchCurrentFile<CR>
```

##Ag##
ag [the_silver_searcher](https://github.com/ggreer/the_silver_searcher)can be used as replacement of grep or Ack, its speed is very impressive.

###require###
install ag
```
$sudo apt-get install the-silver-searcher
```
For other platform follow instraction at [here](https://github.com/ggreer/the_silver_searcher)

###Commands###
* ``:Ag [options] {pattern} [{directory}]``  see ``ag help `` for detail
* ``:Agdir path/to/dir``                     set ag work dir, default cwd
* ``:AgClearWokdir``                         set ag workdidr as cwd

###keymaps###
this keymap will search the word under cursor in AgWorkdir if you have set it or cwd
```
nmap <leader>ag :Ag  <C-R>=expand("<cword>")<CR><CR>
```
The search window opened by Ag assit can use the same with Bookmark, see bookmark section for details.

##Gitk##
gitk is used to see the log of current file, provide two command
###command###
* Gkblame       this command will call gitk show the commit which change current line last time
* Gklog         this command will call gitk show the change log of current file
* Gitk <args>   command with args, which is samed as gitk in shell 

###map###
have to map at here
```
nmap<leader>gp :Gklog<CR>
nmap<leader>gl :Gkblame<CR>
```


##TEST##
I use it dailly on linux platform and Mac os. not test it windows yet.


##TODO##
* Better RANK
* Search File quick
* Integrate Ctags
