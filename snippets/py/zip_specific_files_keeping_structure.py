def zip_with_structure(zip, filelist, root=None, compressed=True):
    '''
    Zip passed filelist into a zip with root path as toplevel tree
    If root is not passed, the shortest path in filelist becomes the root

    :zip: output fullpath of the created zip
    :filelist: list of filepaht as string or Path object (converted anyway)
    :root: top level of the created hierarchy (not included), file that are not inside root are discarded
    :compressed: Decide if zip is compressed or not
    '''

    import zipfile as zp

    filelist = [Path(f) for f in filelist] # ensure pathlib
    if not filelist:
        return
    if not root:
        # autodetect the path thats is closest to root
        root = sorted(filelist, key=lambda f: f.as_posix().count('/'))[0].parent
        print('root: ', root)
    else:
        root = Path(root)

    compress_type = zp.ZIP_DEFLATED if compressed else zp.ZIP_STORED
    with zp.ZipFile(zip, 'w',compress_type) as zipObj:        
        for f in filelist:
            if not f.exists():
                print(f'Not exists: {f.name}')
                continue
            if str(root) not in str(f):
                print(f'{f} is out of root {root}')
                continue

            ## 
            arcname = f.as_posix().replace(root.as_posix(), '').lstrip('/')
            print(f'adding: {arcname}')
            zipObj.write(f, arcname)
            # zipObj.write(f)

    return zip