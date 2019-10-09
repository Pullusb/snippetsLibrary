# default (sequence) – sequence of floats the length of size.
# min (float) - max (float)
# options (set) – Enumerator in ['HIDDEN', 'SKIP_SAVE', 'ANIMATABLE', 'LIBRARY_EDITABLE', 'PROPORTIONAL','TEXTEDIT_UPDATE'].
# step (int) – Step of increment/decrement in UI, in [1, 100], defaults to 3 (WARNING: actual value is /100).
# precision (int) – Maximum number of decimal digits to display, in [0, 6].
# subtype (string) – Enumerator in ['COLOR', 'TRANSLATION', 'DIRECTION', 'VELOCITY', 'ACCELERATION', 'MATRIX', 'EULER', 'QUATERNION', 'AXISANGLE', 'XYZ', 'COLOR_GAMMA', 'LAYER', 'LAYER_MEMBER', 'POWER', 'NONE'].
# unit (string) – Enumerator in ['NONE', 'LENGTH', 'AREA', 'VOLUME', 'ROTATION', 'TIME', 'VELOCITY', 'ACCELERATION', 'MASS', 'CAMERA', 'POWER'].
# size (int) – Vector dimensions in [1, 32].
bpy.types.Scene.${1:FloatVector_variable_name} = ${2:bpy.props.}FloatVectorProperty(name="${3}", description="${4}", default=(${5:0.0}, ${6:0.0}, ${7:0.0}), min=sys.float_info.min, max=sys.float_info.max, soft_min=sys.float_info.min, soft_max=sys.float_info.max, step=3, precision=2, subtype='NONE', unit='NONE', size=3, options={'ANIMATABLE'}${8:, update=None, get=None, set=None})${0}