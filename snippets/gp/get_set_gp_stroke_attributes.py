## Set values to drawing stroke. Examples script from Sietse Brouwer

import bpy
import numpy as np

drawing = bpy.context.grease_pencil.layers.active.current_frame().drawing

# Get number of strokes and points in drawing
number_of_strokes = len(drawing.curve_offsets) - 1
number_of_points = drawing.curve_offsets[-1].value

# Example: set radius of stroke 1
my_stroke_index = 1
point_start = drawing.curve_offsets[my_stroke_index].value
point_end = drawing.curve_offsets[my_stroke_index + 1].value

radii = np.ndarray(shape=(number_of_points), dtype='float')
drawing.attributes['radius'].data.foreach_get('value', radii)
radii[point_start:point_end] = 0.01
drawing.attributes['radius'].data.foreach_set('value', radii)

# Example: move stroke 1 on the x axis
positions = np.ndarray(shape=(number_of_points, 3), dtype='float')
drawing.attributes['position'].data.foreach_get('vector', positions.ravel())
positions[point_start:point_end, 0] += 0.2
drawing.attributes['position'].data.foreach_set('vector', positions.ravel())

# Example: make stroke 1 cyclic
cyclic = np.ndarray(shape=(number_of_strokes), dtype='bool')
drawing.attributes['cyclic'].data.foreach_get('value', cyclic)
cyclic[my_stroke_index:my_stroke_index + 1] = True
drawing.attributes['cyclic'].data.foreach_set('value', cyclic)
