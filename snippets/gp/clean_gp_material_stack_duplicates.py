## Clean duplicates in GP material stack (Taken from gp toolbox / gp render)

def different_gp_mat(mata, matb):
    '''return None if no difference (False), string describing color difference (True)'''
    a = mata.grease_pencil
    b = matb.grease_pencil
    if a.color[:] != b.color[:]:
        return f'{mata.name} and {matb.name} stroke color is different'
    if a.fill_color[:] != b.fill_color[:]:
        return f'{mata.name} and {matb.name} fill_color color is different'
    if a.show_stroke != b.show_stroke:
        return f'{mata.name} and {matb.name} stroke has different state'
    if a.show_fill != b.show_fill:
        return f'{mata.name} and {matb.name} fill has different state'

## Clean dups
def clean_mats_duplication(ob, skip_different_materials=True):
    '''Clean object material stack of duplication
    if a material is named "mat.001" and a "mat" exists, replace with the one with original name

    :skip_different_materials: Don't replace a "mat.???" if orignal "mat" has different color
    '''

    import re
    diff_ct = 0
    todel = []
    if ob.type != 'GPENCIL':
        return
    if not hasattr(ob, 'material_slots'):
        return
    for i, ms in enumerate(ob.material_slots):
        mat = ms.material
        if not mat:
            continue
        match = re.search(r'(.*)\.\d{3}$', mat.name)
        if not match:
            continue
        basemat = bpy.data.materials.get(match.group(1))
        if not basemat:
            continue
        diff = different_gp_mat(mat, basemat)
        if diff:
            print(f'! {ob.name} : {diff}')
            diff_ct += 1
            if skip_different_materials:
                continue

        if mat not in todel:
            todel.append(mat)

        # Replace and unset fake user (will be garbage collected on next file load)
        ms.material = basemat
        print(f'{ob.name} : slot {i} >> replaced {mat.name}')
        mat.use_fake_user = False

    ## Delete material (only when looping on all object at once first, else may delete another objects mat!)
    # for m in reversed(todel):
    #     bpy.data.materials.remove(m)

    if diff_ct:
        print(f'{diff_ct} mat skipped >> same name but different color settings!')
        # return ('INFO', f'{diff_ct} mat skipped >> same name but different color settings!')
