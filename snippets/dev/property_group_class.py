class MYID_PGT_settings(bpy.types.PropertyGroup) :
    Bool_variable_name : bpy.props.BoolProperty(
        name="", description="", default=False, options={'ANIMATABLE'}, subtype='NONE', update=None, get=None, set=None)

    BoolVector_variable_name : bpy.props.BoolVectorProperty(
        name="", description="", default=(False, False, False), options={'ANIMATABLE'}, subtype='NONE', size=3, update=None, get=None, set=None)

    Collection_variable_name : bpy.props.CollectionProperty(
        type=None, name="", description="", options={'ANIMATABLE'})

    Enum_variable_name : bpy.props.EnumProperty(
        items=(
            ('FIRST', 'first element label', 'First element hover description', 0),#include icon name in fourth position
            ('SECOND', 'Second element label', 'second element hover description', 1),
            ),
        name="", description="", default=None, options={'ANIMATABLE'}, update=None, get=None, set=None)

    Float_variable_name : bpy.props.FloatProperty(
        name="", description="", default=0.0, min=sys.float_info.min, max=sys.float_info.max, soft_min=sys.float_info.min, soft_max=sys.float_info.max, step=3, precision=2, options={'ANIMATABLE'}, subtype='NONE', unit='NONE', update=None, get=None, set=None)

    FloatVector_variable_name : bpy.props.FloatVectorProperty(
        name="", description="", default=(0.0, 0.0, 0.0), min=sys.float_info.min, max=sys.float_info.max, soft_min=sys.float_info.min, soft_max=sys.float_info.max, step=3, precision=2, options={'ANIMATABLE'}, subtype='NONE', unit='NONE', size=3, update=None, get=None, set=None)

    Int_variable_name : bpy.props.IntProperty(
        name="", description="", default=0, min=-2**31, max=2**31-1, soft_min=-2**31, soft_max=2**31-1, step=1, options={'ANIMATABLE'}, subtype='NONE', update=None, get=None, set=None)

    IntVector_variable_name : bpy.props.IntVectorProperty(
        name="", description="", default=(0, 0, 0), min=-2**31, max=2**31-1, soft_min=-2**31, soft_max=2**31-1, step=1, options={'ANIMATABLE'}, subtype='NONE', size=3, update=None, get=None, set=None)

    String_variable_name : bpy.props.StringProperty(
        name="", description="", default="", maxlen=0, options={'ANIMATABLE'}, subtype='NONE', update=None, get=None, set=None)

    # place at the end of register()
    bpy.types.Scene.mytoolprops = bpy.props.PointerProperty(type = GP_PG_ToolsSettings)
    # place at the end of unregister()
    del bpy.types.Scene.mytoolprops

    # access in code with bpy.context.scene.mytoolprops.myvariable