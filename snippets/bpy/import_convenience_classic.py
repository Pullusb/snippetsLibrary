import bpy
import os
from os import listdir
from os.path import join, dirname, basename, exists, isfile, isdir, splitext
import re, fnmatch, glob
from mathutils import Vector, Matrix
from math import radians, degrees
C = bpy.context
D = bpy.data
scn = scene = C.scene