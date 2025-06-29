## implementation for easy stroke/point attribute access "get_attribute_for_write", "get_stroke_offsets", "stroke_to_point_index_mask".
## Script by Falk David : https://projects.blender.org/blender/blender/pulls/130287#issuecomment-1614715

import bpy
import numpy as np
import random
from contextlib import AbstractContextManager

#############################################################################

_attribute_value_string = {
  'FLOAT': "value",
  'INT': "value",
  'FLOAT_VECTOR': "vector",
  'FLOAT_COLOR': "color",
  'BYTE_COLOR': "color",
  'STRING': "value",
  'BOOLEAN': "value",
  'FLOAT2': "vector",
  'INT8': "value",
  'INT32_2D': "value",
  'QUATERNION': "value",
  'FLOAT4X4': "value",
}

_attribute_value_dtype = {
  'FLOAT': np.float32,
  'INT': np.dtype('int'),
  'FLOAT_VECTOR': np.float32,
  'FLOAT_COLOR': np.float32,
  'BYTE_COLOR': np.int8,
  'STRING': np.dtype('str'),
  'BOOLEAN': np.dtype('bool'),
  'FLOAT2': np.float32,
  'INT8': np.int8,
  'INT32_2D': np.dtype('int'),
  'QUATERNION': np.float32,
  'FLOAT4X4': np.float32,
}

_attribute_value_shape = {
  'FLOAT': (),
  'INT': (),
  'FLOAT_VECTOR': (3,),
  'FLOAT_COLOR': (4,),
  'BYTE_COLOR': (4,),
  'STRING': (),
  'BOOLEAN': (),
  'FLOAT2':(2,),
  'INT8': (),
  'INT32_2D': (2,),
  'QUATERNION': (4,),
  'FLOAT4X4': (4,4),
}

def get_attribute(attributes, name):
  attr = attributes[name]
  shape = (len(attr.data), *_attribute_value_shape[attr.data_type])

  data = np.empty(shape, dtype=_attribute_value_dtype[attr.data_type])
  attr.data.foreach_get(_attribute_value_string[attr.data_type], np.ravel(data))
  return data

class AttributeContextWriter(AbstractContextManager):
  __slots__ = ()

  def __init__(self, attributes, name):
    self.attributes = attributes
    self.name = name

  def __enter__(self):
    # Store the reference to the data to write it back on __exit__.
    self.data = get_attribute(self.attributes, self.name)
    return self.data
    
  def __exit__(self, *exc_details):
    attr = self.attributes[self.name]
    attr.data.foreach_set(_attribute_value_string[attr.data_type], np.ravel(self.data))
    
def get_attribute_for_write(attributes, name):
    return AttributeContextWriter(attributes, name)

def get_stroke_offsets(drawing):
    offsets = np.ndarray(shape=(len(drawing.curve_offsets)), dtype='int')
    drawing.curve_offsets.foreach_get('value', offsets)
    return offsets

def stroke_to_point_index_mask(stroke_mask, offsets):
    return np.hstack([np.arange(offsets[i], offsets[i+1]) for i in stroke_mask])

#########################################################################################

# Fixed random seed to make sure the outcome stays the same
random.seed(0)

ob = bpy.context.active_object
gpf = ob.data.layers.active.current_frame()

drawing = gpf.drawing

offsets = get_stroke_offsets(drawing)

number_of_strokes = len(offsets) - 1
number_of_points = offsets[-1]

# Random selection of strokes
stroke_selection = [i for i in range(number_of_strokes) if random.random() > 0.6]
point_selection = stroke_to_point_index_mask(stroke_selection, offsets)

# Set the radii of all the selected points to a value
with get_attribute_for_write(drawing.attributes, "radius") as radii:
    radii[point_selection] = 0.01

# Set the opacity to a random value for each point
with get_attribute_for_write(drawing.attributes, "opacity") as opacities:
    opacities[point_selection] = [random.random() for i in point_selection]
