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
at the moment of save the snippet format can be changed from .txt (default) to .py format. The default format can be changed in the addon preference.
It's completely up to you. Preferably use '.py' when the code can run as a standalone script
<!-- Thought it's not mandatory, it is better to add a prefix (e.g: `obj_`) to the name. Try to keep it a very short word that represent a related category, think of it as a tag.
When it's very generic I just use `bpy_` to tell it's related to blender python.
This prefix serve not only to sort snippets (alphabetically) by category, but it's necessary when using the snippets conversion (covered later in this doc)
Also preferably use '-' rather than spaces in snippet's name.-->


**Delete** : This will delete the selected snippet file (pop up a confirmation windows). This action is irreversible since the snippets text file is deleted from disk.

**Open library folder** : open the library folder in your OS browser.

**Preview** : If activated, a preview of the selected snippet will appear below. Also display a list of def and class.
The number of line displayed can be changed in the addon preferences

### addon pref UI

**Use custom path** : Change the source folder of the snippets library.
For example, this prove's usefull when multiple user work on a same server to share the same library (if the addon is not already loaded from server).

**Max preview lines** : Choose max line number for preview (default 10)

**text editor properties** : Choose wich editor option to toggle on when a new textblock is automatically created 

**Conversion** : Enjoy your blender made snippets on your favorite IDE !
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
- add all scene properties in a property group

### Ideas considered :
- Maybe in the future consider putting all the built-in snippets as .py format and stop wondering if it should be txt or py...
- adding bookmark of search tag (editable) this can replace the prefix for a quick search (but will way more disck access )
- Precise open : Make the open folder operator open the folder of the selected snippets
- Edit selected: Add an edit button that open the snippet from disk so it can be edited quickly
- TabTrigger : use the tabstop syntax on snippets to jump the cursor after insertion in blender. (Very hard to implement...)
- quick insert : Double click to insert (just dont know how to do that with UIlist without an ugly modal on each clic)
- Convert and send : adding path to the addon pref so the user so converted snippets goes immetdiately in IDE folder (overwritting old conversion)
- multi-source : adding support for multiple source folder and source change in user preferences...
- online lib : (need multi-source) make some sort of repo where every user can pull-push snippets...(difficult)

---

## Changelog:

  v0.3.0 2019-09-07:
  - Library Clean : All shipped personnal snippets have been corrected to work in 2.8 (mentionned otherwise in the header for a few). Filenames are now with spaces and without prefix
  - Changed shipped snippets folder organisation.
  - UX change : The library use now plain filename without prefix. For IDE conversion it uses now the containing folder name as trigger.
  - New conversion feature : Convert auto-description, during conversion to external editors format, use the top comment (if any) of the snippets as description (else use the snippet name.)
  - Add overwrite alert : Confirmation/options popup when creating snippets with the same name as an already existing one
  - Clean text-get: Change the methods of getting selection so it doesn't mess with user clipboard.
  - Clean save : Saving a new snippet has now a lot of error/sanity check with help messages in case of obvious problems.
  - New addon pref : You can choose if you want snippets to be saved as .txt file or .py by default.
  This choice is also shown at the moment of saving (if an extension is manually added it will override the settings)
  _considering .py format for all snippets in the future..._

  v0.2.3 2019-09-05:
  - Converting a snippets without prefix now use containing folder name as trigger keyword. (instead of "bsnip")
  _thinking about making it the default in the future..._
  - UI fix : The list as now a default minimum size that match the right icons space.
  - UI fix : List item are no longer renamable with double click does nothing, this avoid bad UX and losing track of the snippets file
  - UI new : Preview toggle button is now part of the right side buttons.
  <!--The conversion use the prefix of the snippet's name as a tab-trigger keyword. It add an heading '`s`' This is meant to avoid having triggers with standard words
  If some of your snippets don't have prefixes the name of the containing folder (with an '`s`' before) will be use as tab-trig.
  example: for a snippet prefxes `bpy_`, in sublime text you would start tapping `sbpy` to see suggestions of all related snippets.
  -->

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
