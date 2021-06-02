## open folder in OS browser and select if path is a file

def openFolder(folderpath):
    """
    open the folder at the path given
    with cmd relative to user's OS
    on window and linux, select pointed file
    """
    import subprocess
    from sys import platform
    from shutil import which
    from os.path import isfile, dirname, normpath

    myOS = platform
    if myOS.startswith(('linux','freebsd')):
        cmd = 'xdg-open'

    elif myOS.startswith('win'):
        cmd = 'explorer'
        if not folderpath:
            return('/')
    else:
        cmd = 'open'

    if not folderpath:
        return('//')

    if isfile(folderpath): # When pointing to a file
        select = False
        if myOS.startswith('win'):
            # Keep same path but add "/select" the file (windows cmd option)
            cmd = 'explorer /select,'
            select = True

        elif myOS.startswith(('linux','freebsd')):
            if which('nemo'):
                cmd = 'nemo --no-desktop'
                select = True
            elif which('nautilus'):
                cmd = 'nautilus --no-desktop'
                select = True

        if not select:
            # Use directory of the file
            folderpath = dirname(folderpath)

    folderpath = normpath(folderpath)
    fullcmd = cmd.split() + [folderpath]
    # print('Opening command :', fullcmd)
    subprocess.Popen(fullcmd)
    return ' '.join(fullcmd)