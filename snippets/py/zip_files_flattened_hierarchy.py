def zip_files_flattened(zip, filelist, compressed=True):
    '''
    Zip passed filelist into a zip with flattened hierarchy

    :zip: output fullpath of the created zip
    :filelist: list of filepath as string or Path object (converted anyway)
    :compressed: Decide if zip is compressed or not
    '''

    import zipfile as zp

    filelist = [Path(f) for f in filelist] # ensure pathlib
    if not filelist:
        return

    added = {}
    compress_type = zp.ZIP_DEFLATED if compressed else zp.ZIP_STORED
    with zp.ZipFile(zip, 'w',compress_type) as zipObj:        
        for f in filelist:
            if not f.exists():
                print(f'Not exists: {f.name}')
                continue
            arcname = f.name

            # skip if name already added and have exactly same size
            ## need a for loop in keys to be foolproof
            size = added.get(arcname)
            if size and size == f.stat().st_size:
                print(f'Already added with same size: {f.name}')
                continue

            if size:
                # if already there but size is different create a copy
                i = 2
                while arcname in added.keys():
                    # maybe add the source directory in name to identify ?
                    arcname = f'{f.stem}_{i}{f.suffix}'
                    i+=1
                    ## add a copy

            print(f'adding: {arcname}')
            zipObj.write(f, arcname)
            added[f.name] = f.stat().st_size
    return zip