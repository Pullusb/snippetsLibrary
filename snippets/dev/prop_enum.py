 ${1:bpy.types.Scene.}${2:Enum_variable_name} : ${3:bpy.props.}EnumProperty(
    name="${4}", description="${5}", default=${6:None}, options={'ANIMATABLE'}, update=None, get=None, set=None,
    items=(
        ('${0}CHOICE1', 'First choice', 'this is the first choice', 0),
        ('CHOICE1', 'First choice', 'this is the first choice', 0),   
        ))
    #(key, label, descr, id[, icon])