##The story is that##
finder is a toolbox for searhing things with a quick result window, like the way of command-T
currently it has MRU managerment, quickSearch in buffers and GTags intergrations

##install and setting##
###install and config###
I suggest use *pathgon* to install this plugin, for linux or mac, just put it under dir like ``~/.vim/bundle/``
then set a global var ``g:walle_home`` in your ``.vimrc`` this way
```
let g:walle_home="/Users/ic/.vim/bundle/finder/walle/"
```
AH..., please make attenion that use absPath at here, and make sure the path end with "/", en, It's very ugly,
will fix later.

###commands and maps###
you can find the commands and maps that defined in ``plugin/walle.vim``, personalize it and enjoy it!!!.

###actions in display window###
####move select###
* ``Ctrl + j`` select next, 
* ``Ctrl + k`` select pre

####open####
* ``Ctrl + p`` preview the search result 
* ``Ctrl + o`` and ``double click`` will open serach result, and keep the display window
* ``Enter`` will open serach result, and close the display window


