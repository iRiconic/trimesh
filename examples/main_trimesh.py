import trimesh
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import LineString
#%pylab inline
#%config InlineBackend.figure_format = 'svg'

# load the mesh from filename
# file objects are also supported (original code)
#mesh = trimesh.load_mesh('../models/featuretype.STL')

#testing for other file objects
mesh = trimesh.load_mesh('../models/featuretype.STL')

slice = mesh.section(plane_origin=mesh.centroid, 
                     plane_normal=[0,0,1])


# the section will be in the original mesh frame
slice.show()

# we can move the 3D curve to a Path2D object easily
slice_2D, to_3D = slice.to_planar()
slice_2D.show()

# if we wanted to take a bunch of parallel slices, like for a 3D printer
# we can do that easily with the section_multiplane method
# we're going to slice the mesh into evenly spaced chunks along z
# this takes the (2,3) bounding box and slices it into [minz, maxz]
z_extents = mesh.bounds[:,2]
# slice every .125 model units (eg, inches) - original code
z_levels  = np.arange(*z_extents, step=.125)

# fix the number of layers - how??
#z_levels  = np.arange(*z_extents, step=0.125)


# find a bunch of parallel cross sections
sections = mesh.section_multiplane(plane_origin=mesh.bounds[0], 
                                   plane_normal=[0,0,1], 
                                   heights=z_levels)
sections

# summing the array of Path2D objects will put all of the curves
# into one Path2D object, which we can plot easily
combined = np.sum(sections)
combined.show()

'''
# if we want to intersect a line with this 2D polygon, we can use shapely methods
polygon = slice_2D.polygons_full[0]
# intersect line with one of the polygons
hits = polygon.intersection(LineString([[-4,-1], [3,0]]))
# check what class the intersection returned
hits.__class__

# we can plot the intersection (red) and our original geometry(black and green)
ax = plt.gca()
for h in hits:
    ax.plot(*h.xy, color='r')
slice_2D.show()

# the medial axis is available for closed Path2D objects
(slice_2D + slice_2D.medial_axis()).show()
'''