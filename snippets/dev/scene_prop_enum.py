bpy.types.Scene.${1:Enum_variable_name} = ${2:bpy.props.}EnumProperty(
    name="${3}", description="${4}", default=${5:None}, options={'ANIMATABLE'},${6: update=None, get=None, set=None,}
    items=(
        ('${0}CHOICE1', 'First choice', 'this is the first choice', 0),
        ('CHOICE1', 'First choice', 'this is the first choice', 0),   
        ))
    #(key, label, descr, id[, icon])