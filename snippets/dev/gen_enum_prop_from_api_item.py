## Create enumProperty code from api item

import bpy

def create_enum_layout_code_from_item(rna_item, prop_str):
    rna_type = type(rna_item)
    prop = rna_type.bl_rna.properties[prop_str]
    enum = [(e.identifier, e.name, e.description) for e in prop.enum_items]
    enum_str = ",\n\t".join(str(e) for e in enum)

    layout_str = f'''
{prop.identifier} : bpy.props.EnumProperty(
    name='{prop.name}',
    default='{prop.default}',
    description='{prop.description}',
    items=(
        {enum_str},
        ),
    )
    '''
    return layout_str


# usage ex:
res = create_enum_layout_code_from_item(bpy.context.scene.render.image_settings, 'file_format')
print(res)