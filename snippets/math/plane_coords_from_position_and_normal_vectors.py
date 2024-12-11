## Get a plane in world space from a coordiante and normal (create and apply a matrix)
## /!\ matrix will have unpredicted rotation along normal axis

plane_co, plane_no
## Define the half size of the plane

half_size = 1.0
## Calculate the corners of the plane in local space
local_corners = [
    Vector((-half_size, -half_size, 0)),
    Vector((half_size, -half_size, 0)),
    Vector((half_size, half_size, 0)),
    Vector((-half_size, half_size, 0))
]

# Calculate the orientation matrix from the plane normal
z_axis = plane_no.normalized()
x_axis = z_axis.cross(Vector((0, 1, 0))).normalized()
y_axis = x_axis.cross(z_axis).normalized()
orientation_matrix = Matrix((x_axis, y_axis, z_axis)).transposed()

# Transform the local corners to world space
coords = [orientation_matrix @ corner + plane_co for corner in local_corners]