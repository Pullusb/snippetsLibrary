# step (int) – Step of increment/decrement in UI, in [1, 100], defaults to 3 (WARNING: actual value is /100).
# precision (int) – Maximum number of decimal digits to display, in [0, 6].
# options (set) – Enumerator in ['HIDDEN', 'SKIP_SAVE', 'ANIMATABLE', 'LIBRARY_EDITABLE', 'PROPORTIONAL','TEXTEDIT_UPDATE'].
# subtype (string) – Enumerator in ['PIXEL', 'UNSIGNED', 'PERCENTAGE', 'FACTOR', 'ANGLE', 'TIME', 'DISTANCE', 'NONE'].
# unit (string) – Enumerator in ['NONE', 'LENGTH', 'AREA', 'VOLUME', 'ROTATION', 'TIME', 'VELOCITY', 'ACCELERATION', 'MASS', 'CAMERA', 'POWER'].
bpy.types.Scene.${1:Float_variable_name} = ${2:bpy.props.}FloatProperty(name="${3}", description="${4}", default=${5:0.0}, min=${6:sys.float_info.min}, max=${7:sys.float_info.max}, soft_min=${8:sys.float_info.min}, soft_max=${9:sys.float_info.max}, step=${10:3}, precision=${11:2}, subtype='NONE', unit='NONE', options={'ANIMATABLE'}${12:, update=None, get=None, set=None})${0}