#Assist for vim#
As a programmer, there always annoy things to do, such as find file to edit or search the sybmol where it is referenced and where is it defined. 
so I integrate some usual tools into vim, to make it more comfortable to use vim.

##Search Assist##
###Gtags###
TODO:has done, need write introduce of it

###history file search###
TODO:has done, need write introduce of it

###buffer list search###
TODO:has done, need write introduce of it

###quick search file###
NEXT: need write code to implment it

###code search###
PLAN: need write code
use codesearch tools as backend, integrate it into vim
https://code.google.com/p/codesearch/

if you put the text into register k, example `` "kyw ``  put a word in register k, then it will 
search k in current dir with all file type.(code type..)

intereface:
* SetCsDir a, b, c
* SetFt cpp, java
if you set dir and file type, the effect will keep on until you next call this method.

then the search scope will be in dir a, b, c, with type, cpp.



##Build Assist##
PLAN:can make, deubug, run, etc..

##shell Assists##
LONG PLAN:execute cmd from vim

##Edit Assist##
LONG PLAN:



##Other##
###git assit##
DONE

call gitk show log..
