## Enable Snippets Library addon (useful stored as a registered text to enable when opening a specific file)

import addon_utils

for a in addon_utils.modules():
    if hasattr(a, 'bl_info') and a.bl_info.get('name'):
        if a.bl_info['name'] == 'Snippets Library':
            if not addon_utils.check('snippetsLibrary')[1]:
                print('Enabling Snippets Library addon')
                addon_utils.enable('snippetsLibrary')

            break
