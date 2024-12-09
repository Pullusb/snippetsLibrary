## Changelog

0.6.1 - 2024-12-09

- fixed: potential issue with addon folder name

0.6.0 - 2023-12-13

- fixed: api changes for Blender 4.0.0
- added: lots of snippets since last version

0.5.6 - 2022-10-01

- changed: default preview line display 10 > 25
- changed: preview function/classes above content preview

0.5.5 - 2021-12-05

- fix: blender 3.0.0 api changes # get native template

0.5.4

- feat: on linux shift+clic on the open folder button will also select the file in opened directory
- new snippets

0.5.1

- added tracker url
- new snippets

0.5.0

- Cleanning function : Clear memory button (snippets stay in blend files when load)
- clear operation when shift+click on reload button to save space
- Fix typos

0.4.6

- Fix possible encoding error (load files with option encoding='utf-8')

0.4.5

- Preview have now a better line spacing (tin2tin "column(align=True)" suggestion)

0.4.4

- Convert and send : adding path to the addon pref so the user converted snippets goes immediately in IDE folder (overwritting old conversion)
- added option to turn off folder opening upon conversion finish
  
0.4.3

- fix a bug with converter export for vscode (because [backslash escaping sequence in json is super weird](https://github.com/Microsoft/vscode/issues/33933))

0.4.2

- bugfix when entering nothing in save field (save with a generated random number and date)

0.4.1

- preview fix : '\t' Tab indentation character now display correctly in preview label (converted tab to space)

0.4.0 2019-09-13:

- Major code rewrite on snippets handling:
  - Data not read on-time but stored at reload
  - Reload takes longer but all other operations are faster.
  - Less disk access
  - allow better search
- New addon preferences : Scan buid-in templates (default True), Add blender templates to library
- Multi-source : adding support for multiple source folder. choosing additional sources in a new UIlist in addon preferences
- new UI option : show category in a second left-column
- New search :
  - Search in title and content are merged in the UI searchfield with an option to toggle content/title search.
  - Dynamic realtime search in content
  - Regex search is no longer available. But Wildcard '*' might be powerfull enough
  - removed sort-alphabetically : sorting alphabetically broken, fix in further version
  - Drawback : Prefill option disabled for now, can't find [how to access filter_name property](https://blender.stackexchange.com/questions/106282/access-to-filter-name-property-with-python)

- Unified python snippet format :
  - All the pre-shipped snippets are now .py format
  - Save only as py, option to choose between format has been removed
- Precise open : shift+click on the button open the current selected snippet folder (and select it on windows system)

0.3.3 :

- Underscore in names : snippets change to '_'
- Popup powerup : improvements for the save pop-up now auto format to a correct name and dynamic hint display (but sadly the dialog box redraw only when hitting enter after typing the name)
0.3.2 2019-09-09

- tiny fixes and new snippets

0.3.1 2019-09-08:

- Cleaner insert : Add error message when trying to insert without reloading, or with an empty library.
- Snippet format : Changed default format to be ".py" the only save format ('txt' choice deleted from the preferences, user can still set an extension manually at the moment of saving)
- library format : Changed all all library to .py format (added used script to the meta snippets)

0.3.0 2019-09-07:

- UI change : Now panel have his own 'Snippets' tab
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

0.2.3 2019-09-05:

- Converting a snippets without prefix now use containing folder name as trigger keyword. (instead of "bsnip")
  _thinking about making it the default in the future..._
- UI fix : The list as now a default minimum size that match the right icons space.
- UI fix : List item are no longer renamable with double click does nothing, this avoid bad UX and losing track of the snippets file
- UI new : Preview toggle button is now part of the right side buttons.
<!--The conversion use the prefix of the snippet's name as a tab-trigger keyword. It add an heading '`s`' This is meant to avoid having triggers with standard words
If some of your snippets don't have prefixes the name of the containing folder (with an '`s`' before) will be use as tab-trig.
example: for a snippet prefxes `bpy_`, in sublime text you would start tapping `sbpy` to see suggestions of all related snippets.
-->

0.2.2 2019-09-02:

- New feature : In user preferences, added buttons to convert all snippets to sublime-text/vscode/atom compatible format
- Added possibility to add tabstop syntax to the snippets (e.g: `${1}`or `${2:placeholder}`)
  this syntax is compatible with sublime-text/vscode/atom (for future use in those editor after conversion).
  The tabstop does not affect use in blender. there are hided in the preview and removed at insertion \o/. (maybe compatible in a future version)
- the preview now display the number of remaining hided line (e.g: `...+55 lines`)

0.2.1 2019-08-31:

- Search box now pre-fill with selection in the text (if highlight do not go over one line)
- UI changes

0.2.0 2019-08-31:

- New feature : Search in content (search in content and filename). act like reload with a filtering when populating the list
- New snippet standalone add mode (instead of inserting in current text, create a new text block)
- New option in user preferences : Choose max line number for preview (default 10)
- New option in user preferences : When auto-creating a new textblock choose wich text editor option to toggle on.
- Better tooltips

0.1.4 2019-08-30:

- the preview integrate a list of definitions ans classes of the file

0.1.3 2019-08-29:

- Added snippets preview area

0.1.1 2019-08-28:

- New UI
- new button to delete snippets from UI with confirmation pop-up
- adding a new snippet is now done from a pop-up
- fix bug when inserting without active text block
