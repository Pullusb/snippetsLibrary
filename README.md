# snippetsLibrary
Blender addon - personnal snippets library in text editor

**[Download latest](https://github.com/Pullusb/snippetsLibrary/archive/master.zip)**

Looking for the blender 2.7 version ? [go to this repo](https://github.com/Pullusb/snippetsLibrary279)

### [Demo Youtube](https://youtu.be/Rs4y7DeHkp8)

---  

## Description

Allow you use and manage a library of your own code snippets.
Works in combination with [devTools](https://github.com/Pullusb/devTools) to make your scripting life easier

A new Panel is added in Dev tab category of the text editor's toolbar
Snippets will be saved and stored as invidual plain text files in a folder named 'snippets'.
This folder (created automatically at first use) is located alongside the addon files (unless you enter a custom path).
The addon is shipped with my personal pack of usefull code snippets (once installed just click the reload button in the addon UI to diplay them)


## Features

Here description of the button list in order they appear.

### UI


**Insert paste** : Insert in current text at cursor location (do 'Insert new' if no active text)

**Insert new** : Place the snippet in a new text (named after the snippet)

**Reload** : Load/Reload the list of snippet's from library. It load only '.txt' or '.py' files

**Search** : Searching in content and title of the library (This will reload filtering only matching element). Hit the Reload button to get back to full list.
if you have some text selected in the editor the searchfield will be pre-filled with it (if selection is not multiline).

**Arrows up/down** : Just change current snippet.

**Add** : Create a new snippet to the library from current text selection (pop up a windows)
Thought it's not mandatory, it is better to add a prefix (e.g: `obj_`) to the name. Try to keep it a very short word that represent a related category, think of it as a tag.
When it's very generic I just use `bpy_` to tell it's related to blender python.
This prefix serve not only to sort snippets (alphabetically) by category, but it's necessary when using the snippets conversion (covered later in this doc)
Also preferably use '-' rather than spaces in snippet's name.

**Delete** : This will delete the selected snippet file (pop up a confirmation windows). This action is irreversible since the snippets text file is deleted from disk.

**Open library folder** : open the library folder in your OS browser.

**Preview** : If activated, a preview of the selected snippet will appear below. Also display a list of def and class.
The number of line displayed can be changed in the addon preferences

### addon pref UI

**Use custom path** : Change the source folder of the snippets library.
For example, this prove's usefull when multiple user work on a same server to share the same library (if the addon is not already loaded from server).

**Max preview lines** : Choose max line number for preview (default 10)

**text editor properties** : Choose wich editor option to toggle on when a new textblock is automatically created 

**Conversion** (this feature is not thoroughly tested) : Enjoy your blender made snippets on your favorite IDE !
This buttons allow you to convert all your library to the format of external editors Sublime text, VScode or atom.
The conversion use the prefix (with an '`s`' before) of the snippet's name as a tab-trigger keyword. This is meant to avoid having triggers with standard words
example: for a snippet prefxes `bpy_`, in sublime text you would start tapping `sbpy` to see suggestions of all related snippets.
Note for Atom users: Since multiple snippets can share the same prefix the conversion use [this hack to make it work](https://github.com/medienbaecker/kirby-snippets/issues/1#issue-172641340).


Note : You can enter tabstop syntax in your snippets. This will not affect your use of it in blender.
It can be usefull after conversion on external editors (see Conversion above)
![tabstop](https://github.com/Pullusb/images_repo/raw/master/Bl_snippetLib_Tabstop.png)


Thanks to [tin2tin](https://github.com/tin2tin) for the feedbacks

---

## Changelog:
  v0.2.2 2019-09-02:
  - New feature : In user preferences, added buttons to convert all snippets to sublime-text/vscode/atom compatible format
  - Added possibility to add tabstop syntax to the snippets (e.g: `${1}`or `${2:placeholder}`)
  this syntax is compatible with sublime-text/vscode/atom (for future use in those editor after conversion).
  The tabstop does not affect use in blender. there are hided in the preview and removed at insertion \o/. (maybe compatible in a future version)
  - the preview now display the number of remaining hided line (e.g: `...+55 lines`)

  v0.2.1 2019-08-31:
  - Search box now pre-fill with selection in the text (if highlight do not go over one line)
  - UI changes

  v0.2.0 2019-08-31:
  - New feature : Search in content (search in content and filename). act like reload with a filtering when populating the list
  - New snippet standalone add mode (instead of inserting in current text, create a new text block)
  - New option in user preferences : Choose max line number for preview (default 10)
  - New option in user preferences : When auto-creating a new textblock choose wich text editor option to toggle on.
  - Better tooltips

  v0.1.4 2019-08-30:
  - the preview integrate a list of definitions ans classes of the file

  v0.1.3 2019-08-29:
  - Added snippets preview area

  v0.1.1 2019-08-28:
  - New UI
  - new button to delete snippets from UI with confirmation pop-up
  - adding a new snippet is now done from a pop-up
  - fix bug when inserting without active text block
