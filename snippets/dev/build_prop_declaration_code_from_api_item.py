## Build properties declaration code : generate properties code from api items
## Some properies are still not completely supported (Vector prop for example)
## v1.2

import bpy

exclude = ('rna_type', 'srna', 'type', 'tags', 'icon', 'translation_context',\
'name', 'description', 'identifier',\
'default_array', 'default_flag', 'array_dimensions', 'array_length')

def get_enum_code_from_rna_prop(prop):
    '''Get an enum api item's rna_type.properties to build enum code'''
    enum = [(e.identifier, e.name, e.description) for e in prop.enum_items]
    enum_str = ",\n\t".join(str(e) for e in enum)

    prop_str = f'''
{prop.identifier} : bpy.props.EnumProperty(
    name='{prop.name}',
    default='{prop.default}',
    description='{prop.description}',
    items=(
        {enum_str},
        ),
    )
    '''
    return prop_str

def get_prop_code(prop, exclude_default=True):
    '''Get api item's rna_type.properties to build code'''

    if prop.rna_type.identifier == 'EnumProperty':
        return get_enum_code_from_rna_prop(prop)

    all_prop_attrs = ''
    for subattr in prop.rna_type.properties:
        if not subattr.rna_type.identifier.endswith('Property'):
            continue
        if subattr.rna_type.identifier == 'PointerProperty':
            continue
        if subattr.identifier.startswith('is_'): # don't handle options enum for now
            continue
        if subattr.identifier.strip() in exclude:
            continue

        val = str(getattr(prop, subattr.identifier))
        
        if subattr.type == 'STRING' and val == 'NONE':
            continue

        ## ignore values (problem: not sure of what are the true default values)
        ## does not gie real default : subattr.rna_type.properties['default'].default

        if exclude_default:
            # note: val is str at this point
            if subattr.type == 'INT':
                print('subattr.identifier: ', subattr.identifier)
                if subattr.identifier == 'step' and val == '1': continue
                # if subattr.identifier in ('hard_min', 'soft_min') and val == 0: continue
                # if subattr.identifier in ('hard_max','soft_max') and val == 1048574: continue 
            if subattr.type == 'FLOAT':
                # if subattr.identifier in ('hard_min', 'soft_min') and val == 0.0: continue
                if subattr.identifier in ('hard_max','soft_max') and val == '3.4028234663852886e+38': continue
                if subattr.identifier == 'step' and val == '3': continue

        ## quote strings
        val = f"'{val}'" if subattr.type == 'STRING' else val

        all_prop_attrs += f'    {subattr.identifier}={val},\n'

    prop_string = f'''
{prop.identifier} : bpy.types.{prop.rna_type.identifier}(
    name='{prop.name}',
    description='{prop.description}',
{all_prop_attrs})
'''
    return prop_string


def build_single_prop_code(holder, prop):
    '''get propery group holder in API and prop name as string
    ex: (bpy.context.scene.render.ffmpeg, "audio_bitrate")
    '''
    return get_prop_code(holder.rna_type.properties[prop])


def build_all_prop_from_api_point(prop):
    p_string = ''
    for attr in prop.rna_type.properties:
        if attr.identifier in ('srna', 'rna_type'):
            continue
        p_string += get_prop_code(attr)
    return p_string

rd = bpy.context.scene.render

## all property at an api item
strings = build_all_prop_from_api_point(rd.ffmpeg)

## a single prop
# strings = build_single_prop_code(rd.ffmpeg, 'audio_bitrate')
# equivalent to: strings = get_prop_code(rd.ffmpeg.rna_type.properties['audio_bitrate'])

print(strings) # print in console
# bpy.context.window_manager.clipboard = strings # add to clipboard
