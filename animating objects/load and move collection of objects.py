# load blender model using script
from mathutils import Euler
import pandas as pd
import math
import bpy
import os

model = 'Test_model_2018.blend'
vehName = 'TestModel'
workingDir = '/Users/joe/Documents/blender/'
filepath = os.path.join(workingDir, model)

def importBlend(vehName, filepath):
    # create new collection
    my_coll = bpy.data.collections.new(vehName)
    bpy.context.scene.collection.children.link(my_coll)

    # access model file and identify all objects
    with bpy.data.libraries.load(filepath, link=False) as (data_from, data_to):
        data_to.objects = [name for name in data_from.objects]

    # copy all objects into new collection
    for obj in data_to.objects:
        if obj is not None:
           my_coll.objects.link(obj)
       

importBlend(vehName, filepath)


""" move collection by name """
# load position / rotation data
posData = pd.read_csv(os.path.join(workingDir, 'vehicleMotion.csv'))

coll = bpy.data.collections.get(vehName)

for index, row in posData.iterrows():
    bpy.context.scene.frame_set(row.KeyFrame)
    for obj in coll.objects:        
        # set new location
        obj.select_set(True)
        obj.rotation_euler = Euler((0, 0, math.radians(180)), 'XYZ')
        obj.location = (row.x, row.y, row.z)        
        obj.keyframe_insert(data_path = 'location', index = -1)
