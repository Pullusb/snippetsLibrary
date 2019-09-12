# step (int) – Step of increment/decrement in UI, in [1, 100], defaults to 3 (WARNING: actual value is /100).
# precision (int) – Maximum number of decimal digits to display, in [0, 6].
# options (set) – Enumerator in ['HIDDEN', 'SKIP_SAVE', 'ANIMATABLE', 'LIBRARY_EDITABLE', 'PROPORTIONAL','TEXTEDIT_UPDATE'].
# subtype (string) – Enumerator in ['PIXEL', 'UNSIGNED', 'PERCENTAGE', 'FACTOR', 'ANGLE', 'TIME', 'DISTANCE', 'NONE'].
# unit (string) – Enumerator in ['NONE', 'LENGTH', 'AREA', 'VOLUME', 'ROTATION', 'TIME', 'VELOCITY', 'ACCELERATION', 'MASS', 'CAMERA', 'POWER'].
${1:bpy.types.Scene.}${2:Float_variable_name} : ${3:bpy.props.}FloatProperty(name="${4}", description="${5}", default=${6:0.0}, min=${7:sys.float_info.min}, max=${8:sys.float_info.max}, soft_min=${9:sys.float_info.min}, soft_max=${10:sys.float_info.max}, step=${11:3}, precision=${12:2}, options={'ANIMATABLE'}, subtype='NONE', unit='NONE', update=None, get=None, set=None)${0}