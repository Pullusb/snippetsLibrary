## place an object and pitch it (around X axis) so it look at a specific point (mostly for camera)
## like a temporary Track_to constraint with only X axis free.

def pitch_object_to_target(ob, ob_pos, look_pos):
    """Place ob at ob_pos and rotate it around its own local X axis so its
    view axis (-Z) points toward look_pos. Yaw and roll are left untouched.
    Return the applied angle in radians, or None if nothing could be done.
    """

    ## to_quaternion normalizes away scale/shear, unlike Vector.rotate(matrix_world)
    rot = ob.matrix_world.to_quaternion()
    axis = rot @ Vector((1, 0, 0))    ## local X (pitch axis), in world space
    view = rot @ Vector((0, 0, -1))   ## current view axis, in world space
    target = look_pos - ob_pos

    ## flatten both vectors on the plane orthogonal to the pitch axis:
    ## what remains is the only part a rotation around that axis can change
    v_from = view - view.project(axis)
    v_to = target - target.project(axis)
    if not v_from.length or not v_to.length:
        return None    ## target sits on the pitch axis: no pitch can aim at it

    angle = v_from.normalized().angle(v_to.normalized())
    ## angle() is unsigned: get the direction from the cross product
    if v_from.cross(v_to).dot(axis) < 0:
        angle = -angle

    ## assigning matrix_world is parent agnostic, unlike rotation_euler which is in parent space
    ob.matrix_world = Matrix.LocRotScale(
        ob_pos, 
        Quaternion(axis, angle) @ rot,
        ob.matrix_world.to_scale()
        )
    return angle
