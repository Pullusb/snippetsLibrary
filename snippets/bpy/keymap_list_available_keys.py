## explore keymap and list available key in specific categories
import bpy

keylist = [
'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
'ZERO','ONE','TWO','THREE','FOUR','FIVE','SIX','SEVEN','EIGHT','NINE',
'NUMPAD_1','NUMPAD_2','NUMPAD_3','NUMPAD_4','NUMPAD_5','NUMPAD_6','NUMPAD_7','NUMPAD_8','NUMPAD_9',
'NUMPAD_PERIOD','NUMPAD_SLASH','NUMPAD_ASTERIX','NUMPAD_0','NUMPAD_MINUS','NUMPAD_ENTER','NUMPAD_PLUS',
'F1','F2','F3','F4','F5','F6','F7','F8','F9','F10','F11','F12',
]

exclude = (
'bl_rna', 'identifier','name_property','rna_type','properties', 'compare', 'to_string',#basic
'is_user_defined', 'is_user_modified',
)

def explore_keyconfig_cat(catname, keymap_type='user', log=True):
    print(f'{catname} -- Keymap {keymap_type} --')
    wm = bpy.context.window_manager

    if keymap_type == 'user':
        keyconf = wm.keyconfigs.user.keymaps
    elif keymap_type == 'default':
        keyconf = wm.keyconfigs.default.keymaps
    elif keymap_type == 'addon':
        keyconf = wm.keyconfigs.addon.keymaps
    else:
        print("keymap_type not in ('default', 'user', 'addon')")
        return

    used_keys = []

    for cat, keymap in keyconf.items():
        if catname not in cat:
            continue
        if log:
            print(f'- {cat}')
        for k in keymap.keymap_items:

            mod_list = [m for m in ('ctrl','shift','alt') if getattr(k, m)]
            mods = ' + '.join(mod_list)
            val = f' ({k.value.lower()})' if k.value != 'PRESS' else ''
            if log:
                print(f"{k.name}: {mods + ' ' if mods else ''}{k.type}{val} - {k.idname}")

            ## check for used direct Key without modifier
            if k.key_modifier != 'NONE':
                # used_keys.append('mod:' +k.key_modifier)
                used_keys.append(k.key_modifier)
                continue

            if not mod_list and k.map_type == 'KEYBOARD': # and k.key_modifier == 'NONE' 
                used_keys.append(k.type)

        if log: 
            print()
        return used_keys
        return list(set(used_keys))


def check_available_direct_keys():
    '''Check direct keys available in GP draw mode'''

    used = []

    l = explore_keyconfig_cat('Grease Pencil Stroke Paint (Draw brush)', log=0)
    # print("l", l)#Dbg
    used += l

    ## Also consider general "paint mode" and Global keys
    l = explore_keyconfig_cat('Grease Pencil Stroke Paint Mode', log=0)
    # print("l", l)#Dbg
    used += l

    l = explore_keyconfig_cat('Grease Pencil', log=0)
    # print("l", l)#Dbg
    used += l


    ## Also consider Global keys accross all editors
    l = explore_keyconfig_cat('Window', log=0)
    # print("l", l)#Dbg
    used += l
    l = explore_keyconfig_cat('Screen', log=0)
    # print("l", l)#Dbg
    used += l

    ## In case of 3D view need also global shortcut
    l = explore_keyconfig_cat('3D View Generic', log=0)
    # print("l", l)#Dbg
    used += l

    # check every key that is not used
    available = [x for x in keylist if x not in used]

    return available

usable = check_available_direct_keys()
print(f'Available keys in draw mode:\n{usable}')

# explore_keyconfig_cat('Grease Pencil Stroke Paint Mode')