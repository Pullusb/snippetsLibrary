## region <-> location coordinate switch, converted from native Blender functions to receive parameters instead of context.region and context.region.data arguments.
# This allow to use stored parameters, so they don't change over time (ex: within a redo panel)
# Note: for matrix_view and matrix_perspective args, it is recommended to use .copy() to keep them unchanged during operation

# Two sets of functions: 
# - single coord: basic function with same name as native in `bpy_extras.view3d_utils`. (important note: those can be ~4 times slower than original ones)
# - vectorized coords: Faster method to apply direcly on lists of coordinates, same name with `_list` suffix.

import bpy
import numpy as np
from mathutils import Vector, Matrix, geometry
from mathutils.geometry import intersect_line_plane, intersect_point_line

# region view <-> world

def _get_context_values():
    """Extract values from bpy.context when parameters are not provided."""
    region = bpy.context.region
    region_data = bpy.context.region_data
    
    return {
        'region_width': region.width,
        'region_height': region.height,
        'view_matrix': region_data.view_matrix,
        'perspective_matrix': region_data.perspective_matrix,
        'is_perspective': region_data.is_perspective,
        'view_perspective': region_data.view_perspective,
    }

# region single coord 
# (for individual operations, still slower than native function)

def region_2d_to_vector_3d(coord, *, region_width=None, region_height=None, view_matrix=None, perspective_matrix=None, is_perspective=None):
    """
    Return a direction vector from the viewport at the specific 2d region coordinate.

    :arg coord: 2d coordinates relative to the region: [x, y].
    :type coord: 2d vector
    :arg region_width: width of the region in pixels. If None, uses bpy.context.region.width.
    :type region_width: int | None
    :arg region_height: height of the region in pixels. If None, uses bpy.context.region.height.
    :type region_height: int | None
    :arg view_matrix: the view matrix of the 3D viewport. If None, uses bpy.context.region_data.view_matrix.
    :type view_matrix: :class:`mathutils.Matrix` | None
    :arg perspective_matrix: the perspective matrix of the 3D viewport. If None, uses bpy.context.region_data.perspective_matrix.
    :type perspective_matrix: :class:`mathutils.Matrix` | None
    :arg is_perspective: whether the view is perspective or orthographic. If None, uses bpy.context.region_data.is_perspective.
    :type is_perspective: bool | None
    :return: normalized 3d vector.
    :rtype: :class:`mathutils.Vector`
    """
    # Get missing parameters from context
    if any(param is None for param in [region_width, region_height, view_matrix, perspective_matrix, is_perspective]):
        context_values = _get_context_values()
        region_width = region_width if region_width is not None else context_values['region_width']
        region_height = region_height if region_height is not None else context_values['region_height']
        view_matrix = view_matrix if view_matrix is not None else context_values['view_matrix']
        perspective_matrix = perspective_matrix if perspective_matrix is not None else context_values['perspective_matrix']
        is_perspective = is_perspective if is_perspective is not None else context_values['is_perspective']
    
    viewinv = view_matrix.inverted()
    if is_perspective:
        persinv = perspective_matrix.inverted()

        out = Vector((
            (2.0 * coord[0] / region_width) - 1.0,
            (2.0 * coord[1] / region_height) - 1.0,
            -0.5
        ))

        w = out.dot(persinv[3].xyz) + persinv[3][3]

        view_vector = ((persinv @ out) / w) - viewinv.translation
    else:
        view_vector = -viewinv.col[2].xyz

    view_vector.normalize()

    return view_vector


def region_2d_to_origin_3d(coord, *, region_width=None, region_height=None, view_matrix=None, perspective_matrix=None, is_perspective=None, view_perspective=None, clamp=None):
    """
    Return the 3d view origin from the region relative 2d coords.

    :arg coord: 2D coordinates relative to the region: [x, y].
    :type coord: 2d vector
    :arg region_width: width of the region in pixels. If None, uses bpy.context.region.width.
    :type region_width: int | None
    :arg region_height: height of the region in pixels. If None, uses bpy.context.region.height.
    :type region_height: int | None
    :arg view_matrix: the view matrix of the 3D viewport. If None, uses bpy.context.region_data.view_matrix.
    :type view_matrix: :class:`mathutils.Matrix` | None
    :arg perspective_matrix: the perspective matrix of the 3D viewport. If None, uses bpy.context.region_data.perspective_matrix.
    :type perspective_matrix: :class:`mathutils.Matrix` | None
    :arg is_perspective: whether the view is perspective or orthographic. If None, uses bpy.context.region_data.is_perspective.
    :type is_perspective: bool | None
    :arg view_perspective: the view perspective mode (e.g., 'CAMERA', 'PERSP', 'ORTHO'). If None, uses bpy.context.region_data.view_perspective.
    :type view_perspective: str | None
    :arg clamp: Clamp the maximum far-clip value used.
    :type clamp: float | None
    :return: The origin of the viewpoint in 3d space.
    :rtype: :class:`mathutils.Vector`
    """
    # Get missing parameters from context
    if any(param is None for param in [region_width, region_height, view_matrix, perspective_matrix, is_perspective, view_perspective]):
        context_values = _get_context_values()
        region_width = region_width if region_width is not None else context_values['region_width']
        region_height = region_height if region_height is not None else context_values['region_height']
        view_matrix = view_matrix if view_matrix is not None else context_values['view_matrix']
        perspective_matrix = perspective_matrix if perspective_matrix is not None else context_values['perspective_matrix']
        is_perspective = is_perspective if is_perspective is not None else context_values['is_perspective']
        view_perspective = view_perspective if view_perspective is not None else context_values['view_perspective']
    
    viewinv = view_matrix.inverted()

    if is_perspective:
        origin_start = viewinv.translation.copy()
    else:
        persmat = perspective_matrix.copy()
        dx = (2.0 * coord[0] / region_width) - 1.0
        dy = (2.0 * coord[1] / region_height) - 1.0
        persinv = persmat.inverted()
        origin_start = (
            (persinv.col[0].xyz * dx) +
            (persinv.col[1].xyz * dy) +
            persinv.translation
        )

        if clamp != 0.0:
            if view_perspective != 'CAMERA':
                # this value is scaled to the far clip already
                origin_offset = persinv.col[2].xyz
                if clamp is not None:
                    if clamp < 0.0:
                        origin_offset.negate()
                        clamp = -clamp
                    if origin_offset.length > clamp:
                        origin_offset.length = clamp

                origin_start -= origin_offset

    return origin_start


def region_2d_to_location_3d(coord, depth_location, *, region_width=None, region_height=None, view_matrix=None, perspective_matrix=None, is_perspective=None, view_perspective=None):
    """
    Return a 3d location from the region relative 2d coords, aligned with *depth_location*.

    :arg coord: 2d coordinates relative to the region: [x, y].
    :type coord: 2d vector
    :arg depth_location: the returned vectors depth is aligned with this since
       there is no defined depth with a 2d region input.
    :type depth_location: 3d vector
    :arg region_width: width of the region in pixels. If None, uses bpy.context.region.width.
    :type region_width: int | None
    :arg region_height: height of the region in pixels. If None, uses bpy.context.region.height.
    :type region_height: int | None
    :arg view_matrix: the view matrix of the 3D viewport. If None, uses bpy.context.region_data.view_matrix.
    :type view_matrix: :class:`mathutils.Matrix` | None
    :arg perspective_matrix: the perspective matrix of the 3D viewport. If None, uses bpy.context.region_data.perspective_matrix.
    :type perspective_matrix: :class:`mathutils.Matrix` | None
    :arg is_perspective: whether the view is perspective or orthographic. If None, uses bpy.context.region_data.is_perspective.
    :type is_perspective: bool | None
    :arg view_perspective: the view perspective mode (e.g., 'CAMERA', 'PERSP', 'ORTHO'). If None, uses bpy.context.region_data.view_perspective.
    :type view_perspective: str | None
    :return: 3d location.
    :rtype: :class:`mathutils.Vector`
    """
    # Get missing parameters from context
    if any(param is None for param in [region_width, region_height, view_matrix, perspective_matrix, is_perspective, view_perspective]):
        context_values = _get_context_values()
        region_width = region_width if region_width is not None else context_values['region_width']
        region_height = region_height if region_height is not None else context_values['region_height']
        view_matrix = view_matrix if view_matrix is not None else context_values['view_matrix']
        perspective_matrix = perspective_matrix if perspective_matrix is not None else context_values['perspective_matrix']
        is_perspective = is_perspective if is_perspective is not None else context_values['is_perspective']
        view_perspective = view_perspective if view_perspective is not None else context_values['view_perspective']
    
    coord_vec = region_2d_to_vector_3d(
        coord, 
        region_width=region_width, 
        region_height=region_height, 
        view_matrix=view_matrix, 
        perspective_matrix=perspective_matrix, 
        is_perspective=is_perspective
    )
    depth_location = Vector(depth_location)

    origin_start = region_2d_to_origin_3d(
        coord, 
        region_width=region_width, 
        region_height=region_height, 
        view_matrix=view_matrix, 
        perspective_matrix=perspective_matrix, 
        is_perspective=is_perspective, 
        view_perspective=view_perspective
    )
    origin_end = origin_start + coord_vec

    if is_perspective:
        viewinv = view_matrix.inverted()
        view_vec = viewinv.col[2].copy()
        return intersect_line_plane(
            origin_start,
            origin_end,
            depth_location,
            view_vec,
        )
    else:
        return intersect_point_line(
            depth_location,
            origin_start,
            origin_end,
        )[0]


def location_3d_to_region_2d(coord, *, region_width=None, region_height=None, perspective_matrix=None, default=None):
    """
    Return the *region* relative 2d location of a 3d position.

    :arg coord: 3d world-space location: [x, y, z].
    :type coord: 3d vector
    :arg region_width: width of the region in pixels. If None, uses bpy.context.region.width.
    :type region_width: int | None
    :arg region_height: height of the region in pixels. If None, uses bpy.context.region.height.
    :type region_height: int | None
    :arg perspective_matrix: the perspective matrix of the 3D viewport. If None, uses bpy.context.region_data.perspective_matrix.
    :type perspective_matrix: :class:`mathutils.Matrix` | None
    :arg default: Return this value if ``coord`` is behind the origin of a perspective view.
    :return: 2d location
    :rtype: :class:`mathutils.Vector` | Any
    """
    # Get missing parameters from context
    if any(param is None for param in [region_width, region_height, perspective_matrix]):
        context_values = _get_context_values()
        region_width = region_width if region_width is not None else context_values['region_width']
        region_height = region_height if region_height is not None else context_values['region_height']
        perspective_matrix = perspective_matrix if perspective_matrix is not None else context_values['perspective_matrix']
    
    prj = perspective_matrix @ Vector((coord[0], coord[1], coord[2], 1.0))
    if prj.w > 0.0:
        width_half = region_width / 2.0
        height_half = region_height / 2.0

        return Vector((
            width_half + width_half * (prj.x / prj.w),
            height_half + height_half * (prj.y / prj.w),
        ))
    else:
        return default

# endregion single coord

# region vectorized coords
# (Optimized for batch operations)

def _ensure_numpy_array(coords, expected_dims=2):
    """Convert input coordinates to numpy array."""
    coords = np.asarray(coords, dtype=np.float64)
    
    if coords.ndim == 1:
        coords = coords.reshape(1, -1)
        
    if coords.shape[1] != expected_dims:
        raise ValueError(f"Expected {expected_dims}D coordinates, got {coords.shape[1]}D")
        
    return coords


def _matrix_to_numpy(matrix):
    """Convert mathutils Matrix to numpy array."""
    return np.array([list(row) for row in matrix], dtype=np.float64)


def _numpy_to_vectors(arr):
    """Convert numpy array back to mathutils Vectors."""
    return [Vector(row) for row in arr]


def region_2d_to_vector_3d_list(coords, *, region_width=None, region_height=None, view_matrix=None, perspective_matrix=None, is_perspective=None):
    """
    Return direction vectors from the viewport at the specific 2d region coordinates.

    :arg coords: List of 2d coordinates relative to the region: [[x1, y1], [x2, y2], ...].
    :type coords: list of 2d vectors
    :arg region_width: width of the region in pixels. If None, uses bpy.context.region.width.
    :type region_width: int | None
    :arg region_height: height of the region in pixels. If None, uses bpy.context.region.height.
    :type region_height: int | None
    :arg view_matrix: the view matrix of the 3D viewport. If None, uses bpy.context.region_data.view_matrix.
    :type view_matrix: :class:`mathutils.Matrix` | None
    :arg perspective_matrix: the perspective matrix of the 3D viewport. If None, uses bpy.context.region_data.perspective_matrix.
    :type perspective_matrix: :class:`mathutils.Matrix` | None
    :arg is_perspective: whether the view is perspective or orthographic. If None, uses bpy.context.region_data.is_perspective.
    :type is_perspective: bool | None
    :return: list of normalized 3d vectors.
    :rtype: list of :class:`mathutils.Vector`
    """
    # Get missing parameters from context
    if any(param is None for param in [region_width, region_height, view_matrix, perspective_matrix, is_perspective]):
        context_values = _get_context_values()
        region_width = region_width if region_width is not None else context_values['region_width']
        region_height = region_height if region_height is not None else context_values['region_height']
        view_matrix = view_matrix if view_matrix is not None else context_values['view_matrix']
        perspective_matrix = perspective_matrix if perspective_matrix is not None else context_values['perspective_matrix']
        is_perspective = is_perspective if is_perspective is not None else context_values['is_perspective']
    
    coords = _ensure_numpy_array(coords, 2)
    n_coords = coords.shape[0]
    
    viewinv = _matrix_to_numpy(view_matrix.inverted())
    
    if is_perspective:
        persinv = _matrix_to_numpy(perspective_matrix.inverted())
        
        # Convert to normalized device coordinates
        ndc = np.column_stack([
            (2.0 * coords[:, 0] / region_width) - 1.0,
            (2.0 * coords[:, 1] / region_height) - 1.0,
            np.full(n_coords, -0.5)
        ])
        
        # Add homogeneous coordinate
        ndc_homo = np.column_stack([ndc, np.ones(n_coords)])
        
        # Calculate w values
        w = np.dot(ndc, persinv[3, :3]) + persinv[3, 3]
        
        # Transform to world space
        transformed = np.dot(ndc_homo, persinv.T)
        view_vectors = (transformed[:, :3] / w.reshape(-1, 1)) - viewinv[:3, 3]
        
    else:
        # Orthographic: view vector is constant
        view_vec = -viewinv[:3, 2]
        view_vectors = np.tile(view_vec, (n_coords, 1))
    
    # Normalize vectors
    norms = np.linalg.norm(view_vectors, axis=1, keepdims=True)
    view_vectors = view_vectors / norms
    
    return _numpy_to_vectors(view_vectors)


def region_2d_to_origin_3d_list(coords, *, region_width=None, region_height=None, view_matrix=None, perspective_matrix=None, is_perspective=None, view_perspective=None, clamp=None):
    """
    Return the 3d view origins from the region relative 2d coords.

    :arg coords: List of 2D coordinates relative to the region: [[x1, y1], [x2, y2], ...].
    :type coords: list of 2d vectors
    :arg region_width: width of the region in pixels. If None, uses bpy.context.region.width.
    :type region_width: int | None
    :arg region_height: height of the region in pixels. If None, uses bpy.context.region.height.
    :type region_height: int | None
    :arg view_matrix: the view matrix of the 3D viewport. If None, uses bpy.context.region_data.view_matrix.
    :type view_matrix: :class:`mathutils.Matrix` | None
    :arg perspective_matrix: the perspective matrix of the 3D viewport. If None, uses bpy.context.region_data.perspective_matrix.
    :type perspective_matrix: :class:`mathutils.Matrix` | None
    :arg is_perspective: whether the view is perspective or orthographic. If None, uses bpy.context.region_data.is_perspective.
    :type is_perspective: bool | None
    :arg view_perspective: the view perspective mode (e.g., 'CAMERA', 'PERSP', 'ORTHO'). If None, uses bpy.context.region_data.view_perspective.
    :type view_perspective: str | None
    :arg clamp: Clamp the maximum far-clip value used.
    :type clamp: float | None
    :return: list of origins of the viewpoint in 3d space.
    :rtype: list of :class:`mathutils.Vector`
    """
    # Get missing parameters from context
    if any(param is None for param in [region_width, region_height, view_matrix, perspective_matrix, is_perspective, view_perspective]):
        context_values = _get_context_values()
        region_width = region_width if region_width is not None else context_values['region_width']
        region_height = region_height if region_height is not None else context_values['region_height']
        view_matrix = view_matrix if view_matrix is not None else context_values['view_matrix']
        perspective_matrix = perspective_matrix if perspective_matrix is not None else context_values['perspective_matrix']
        is_perspective = is_perspective if is_perspective is not None else context_values['is_perspective']
        view_perspective = view_perspective if view_perspective is not None else context_values['view_perspective']
    
    coords = _ensure_numpy_array(coords, 2)
    n_coords = coords.shape[0]
    
    viewinv = _matrix_to_numpy(view_matrix.inverted())
    
    if is_perspective:
        # All origins are the same for perspective view
        origin = viewinv[:3, 3]
        origins = np.tile(origin, (n_coords, 1))
    else:
        persmat = _matrix_to_numpy(perspective_matrix)
        persinv = np.linalg.inv(persmat)
        
        # Calculate dx, dy for all coordinates
        dx = (2.0 * coords[:, 0] / region_width) - 1.0
        dy = (2.0 * coords[:, 1] / region_height) - 1.0
        
        # Calculate origins
        origins = (
            np.outer(dx, persinv[:3, 0]) +
            np.outer(dy, persinv[:3, 1]) +
            persinv[:3, 3]
        )
        
        if clamp != 0.0 and view_perspective != 'CAMERA':
            origin_offset = persinv[:3, 2]
            if clamp is not None:
                if clamp < 0.0:
                    origin_offset = -origin_offset
                    clamp = -clamp
                offset_length = np.linalg.norm(origin_offset)
                if offset_length > clamp:
                    origin_offset = origin_offset * (clamp / offset_length)
            
            origins = origins - origin_offset
    
    return _numpy_to_vectors(origins)


def region_2d_to_location_3d_list(coords, depth_location, *, region_width=None, region_height=None, view_matrix=None, perspective_matrix=None, is_perspective=None, view_perspective=None):
    """
    Return 3d locations from the region relative 2d coords, aligned with *depth_location*.

    :arg coords: List of 2d coordinates relative to the region: [[x1, y1], [x2, y2], ...].
    :type coords: list of 2d vectors
    :arg depth_location: the returned vectors depth is aligned with this since
       there is no defined depth with a 2d region input.
    :type depth_location: 3d vector
    :arg region_width: width of the region in pixels. If None, uses bpy.context.region.width.
    :type region_width: int | None
    :arg region_height: height of the region in pixels. If None, uses bpy.context.region.height.
    :type region_height: int | None
    :arg view_matrix: the view matrix of the 3D viewport. If None, uses bpy.context.region_data.view_matrix.
    :type view_matrix: :class:`mathutils.Matrix` | None
    :arg perspective_matrix: the perspective matrix of the 3D viewport. If None, uses bpy.context.region_data.perspective_matrix.
    :type perspective_matrix: :class:`mathutils.Matrix` | None
    :arg is_perspective: whether the view is perspective or orthographic. If None, uses bpy.context.region_data.is_perspective.
    :type is_perspective: bool | None
    :arg view_perspective: the view perspective mode (e.g., 'CAMERA', 'PERSP', 'ORTHO'). If None, uses bpy.context.region_data.view_perspective.
    :type view_perspective: str | None
    :return: list of 3d locations.
    :rtype: list of :class:`mathutils.Vector`
    """
    # Get missing parameters from context
    if any(param is None for param in [region_width, region_height, view_matrix, perspective_matrix, is_perspective, view_perspective]):
        context_values = _get_context_values()
        region_width = region_width if region_width is not None else context_values['region_width']
        region_height = region_height if region_height is not None else context_values['region_height']
        view_matrix = view_matrix if view_matrix is not None else context_values['view_matrix']
        perspective_matrix = perspective_matrix if perspective_matrix is not None else context_values['perspective_matrix']
        is_perspective = is_perspective if is_perspective is not None else context_values['is_perspective']
        view_perspective = view_perspective if view_perspective is not None else context_values['view_perspective']
    
    # Get direction vectors and origins
    coord_vecs = region_2d_to_vector_3d_list(
        coords, 
        region_width=region_width, 
        region_height=region_height, 
        view_matrix=view_matrix, 
        perspective_matrix=perspective_matrix, 
        is_perspective=is_perspective
    )
    origins = region_2d_to_origin_3d_list(
        coords, 
        region_width=region_width, 
        region_height=region_height, 
        view_matrix=view_matrix, 
        perspective_matrix=perspective_matrix, 
        is_perspective=is_perspective, 
        view_perspective=view_perspective
    )
    
    depth_location = Vector(depth_location)
    
    results = []
    if is_perspective:
        viewinv = view_matrix.inverted()
        view_vec = viewinv.col[2].xyz.copy()
        
        for origin, coord_vec in zip(origins, coord_vecs):
            origin_end = origin + coord_vec
            result = intersect_line_plane(origin, origin_end, depth_location, view_vec)
            results.append(result)
    else:
        for origin, coord_vec in zip(origins, coord_vecs):
            origin_end = origin + coord_vec
            result = intersect_point_line(depth_location, origin, origin_end)[0]
            results.append(result)
    
    return results


def location_3d_to_region_2d_list(coords, *, region_width=None, region_height=None, perspective_matrix=None, default=None):
    """
    Return the region relative 2d locations of 3d positions.

    :arg coords: List of 3d world-space locations: [[x1, y1, z1], [x2, y2, z2], ...].
    :type coords: list of 3d vectors
    :arg region_width: width of the region in pixels. If None, uses bpy.context.region.width.
    :type region_width: int | None
    :arg region_height: height of the region in pixels. If None, uses bpy.context.region.height.
    :type region_height: int | None
    :arg perspective_matrix: the perspective matrix of the 3D viewport. If None, uses bpy.context.region_data.perspective_matrix.
    :type perspective_matrix: :class:`mathutils.Matrix` | None
    :arg default: Return this value if coords are behind the origin of a perspective view.
    :return: list of 2d locations
    :rtype: list of :class:`mathutils.Vector` or Any
    """
    # Get missing parameters from context
    if any(param is None for param in [region_width, region_height, perspective_matrix]):
        context_values = _get_context_values()
        region_width = region_width if region_width is not None else context_values['region_width']
        region_height = region_height if region_height is not None else context_values['region_height']
        perspective_matrix = perspective_matrix if perspective_matrix is not None else context_values['perspective_matrix']
    
    coords = _ensure_numpy_array(coords, 3)
    n_coords = coords.shape[0]
    
    perspective_np = _matrix_to_numpy(perspective_matrix)
    
    # Add homogeneous coordinate
    coords_homo = np.column_stack([coords, np.ones(n_coords)])
    
    # Project to clip space
    projected = np.dot(coords_homo, perspective_np.T)
    
    # Check which points are in front of camera
    valid_mask = projected[:, 3] > 0.0
    
    results = []
    width_half = region_width / 2.0
    height_half = region_height / 2.0
    
    for i in range(n_coords):
        if valid_mask[i]:
            w = projected[i, 3]
            screen_pos = Vector((
                width_half + width_half * (projected[i, 0] / w),
                height_half + height_half * (projected[i, 1] / w),
            ))
            results.append(screen_pos)
        else:
            results.append(default)
    
    return results

# endregion vectorized coords

# endregion view <-> world
