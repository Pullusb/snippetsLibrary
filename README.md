# snippetsLibrary
Blender addon - personnal snippets library in text editor

**[Download latest](https://github.com/Pullusb/snippetsLibrary/archive/master.zip)**

Looking for the blender 2.7 version ? [go to this repo](https://github.com/Pullusb/snippetsLibrary279)

### [Demo Youtube](https://youtu.be/Rs4y7DeHkp8)

Want to support me? Get something from [my gumroad](https://pullusb.gumroad.com/), [blender market](https://blendermarket.com/creators/pullup), or see [other means](http://www.samuelbernou.fr/donate)

---  

## Description

Allow you use and manage a library of your own code snippets.  
Works well in combination with [devTools](https://github.com/Pullusb/devTools) to make your scripting life easier.  

A new _Snippets_ tab will be in the text editor's toolbar (accessible with `ctrl + T`).  
Snippets will be saved and stored as invidual plain text files in a folder named 'snippets'.  
This folder is located by default alongside the addon files (unless you enter a custom path in addon preferences).  
Blender build-in snippets are also scanned (you can disable it in addon pref).  
The addon is shipped with my personal pack of usefull code snippets (all free to use)  
once installed just click the reload button in the addon UI to diplay them)


## Features

Here description of the button list in order they appear.

### UI


**Insert paste** : Insert in current text at cursor location (do 'Insert new' if no active text)

**Insert new** : Place the snippet in a new text (named after the snippet)

**Reload** : Load/Reload the list of snippet's from library. It load only '.txt' or '.py' files  
Shift + click on Reload clear the list off the blend file (save space when your done)

<!-- **Search** : Searching in content and title of the library (This will reload filtering only matching element). Hit the Reload button to get back to full list.
if you have some text selected in the editor the searchfield will be pre-filled with it (if selection is not multiline). -->

**Arrows up/down** : Just change current snippet.

**Add** : Create a new snippet in library from current text selection (pop up a windows).  
Snippets are saved as standalone '.py' file in the library folder.  
Once saved you can open the library (click the icon folder) and arrange your newly created snippets into a suiting category folder (creating folder and subfolder is OK).  
Thus it's not necessary, the containing folder name will be important if you use the `conversion` feature (see below).  
<!-- at the moment of save the snippet format can be changed from .txt (default) to .py format. The default format can be changed in the addon preference.
It's completely up to you. Preferably use '.py' when the code can run as a standalone script
Thought it's not mandatory, it is better to add a prefix (e.g: `obj_`) to the name. Try to keep it a very short word that represent a related category, think of it as a tag.
When it's very generic I just use `bpy_` to tell it's related to blender python.
This prefix serve not only to sort snippets (alphabetically) by category, but it's necessary when using the snippets conversion (covered later in this doc)
Also preferably use '-' rather than spaces in snippet's name.-->


**Delete** : This will delete the selected snippet file (pop up a confirmation windows). This action is irreversible since the snippets text file is deleted from disk.

**Open library folder** : Open the library folder in your OS browser. shift+click on the button will open at current selected snippet folder.


**Search  field** : options : search between content and title, substractive search, show prefix, reverse order
_filter by name is currently broken so the feature has been removed_

**Preview** : If activated, a preview of the selected snippet will appear below. Also display a list of def and class.
The number of line displayed can be changed in the addon preferences

### addon pref UI

**Use custom path** : Change the source folder of the snippets library.
For example, this prove's usefull when multiple user work on a same server to share the same library (if the addon is not already loaded from server).

**Secondary path** : Manage other folderpath to scan as part of the library. Also choose to add blender build-in snippets in the lib (Those are already accessible with template menu in text editor)

**Max preview lines** : Choose max line number for preview (default 10)

**text editor properties** : Choose wich editor option to toggle on when a new textblock is automatically created 

**Conversion** : Enjoy your blender made snippets in your favorite IDE !
This buttons allow you to convert all your library to the format of external editors Sublime text, VScode or atom.
The trigger word to call it will be the name of the snippet's containing folder with an heading '`s`' added. (This is meant to avoid having triggers with standard words)  
example: if the snippets was in the folder `bpy`, in sublime text you would start tapping `sbpy` to see suggestions of all related snippets.
Note for Atom users: Since multiple snippets can share the same prefix, the conversion use [this hack to make it work](https://github.com/medienbaecker/kirby-snippets/issues/1#issue-172641340).

Note : You can enter tabstop syntax in your snippets. This will not affect your use of it in blender.  
It can be usefull after conversion on external editors (see Conversion above)
![tabstop](https://github.com/Pullusb/images_repo/raw/master/Bl_snippetLib_Tabstop.png)


Thanks to [tin2tin](https://github.com/tin2tin) for the feedbacks  

---


## Todo:
  - Think a way of auto cleaning... complex (maybe have a preference to auto-clean on save. But can be a super pain for the user)
- title case for the name (but need cases insensitive search, at least on titles before)
- Try to re-implement previous search option with the new design :
  - Case insensitive search (more usefull)
  - Regex search
  - sort-alphabetically
- [Prefill with selection](https://blender.stackexchange.com/questions/106282/access-to-filter-name-property-with-python)
- cleaner scene properties : Put all scene properties in a property group

### Ideas considered :
- adding bookmark of search tag (editable) this can replace the prefix for a quick search
or just an enum/list of the current folders to choose what to scan
- Edit selected: Add an edit button that open the snippet from disk so it can be edited quickly
- Find a way to resolve eventual conflict (different file with same name) -> example, pop up a windows with infos display and button to do action on name who have ultiple entry.
- Maybe avoid scan doubles.
- TabTrigger : use the tabstop syntax on snippets to jump the cursor after insertion in blender. (Very hard to implement...)
- quick insert : Double click to insert (with UIlist only an ugly modal on each clic or and operator in list but operator force center the text...)
- online lib : Make some sort of repo where every user can pull-push snippets...(super difficult)
