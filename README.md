# Renpy save renamer
Expanded load/save screens that let players rename their saves.  
Also, while browsing their saves, players can jump ten pages at a time.

In order to use the script, edit the original file screens.rpy and replace respectively:  
```use file_slots(_("Save"))```  
with:  
```use renamer_file_slots(_("Save"))```  
and:  
```use file_slots(_("Load"))```  
with:  
```use renamer_file_slots(_("Load"))```  

The icons in the images folder are from [Feathericons](http://google.comhttps://github.com/feathericons/feather), a beautiful collection made by [colebemis](https://twitter.com/colebemis) and licensed under the [MIT License](https://raw.githubusercontent.com/feathericons/feather/master/LICENSE).