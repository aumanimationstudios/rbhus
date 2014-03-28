import bpy
import os
import sys

sys.path.append("/home/shrinidhi/bin/gitHub/rbhus/rbhus")

import dbPipe
import constantsPipe
import utilsPipe

dirSelf = os.path.dirname(os.path.realpath(__file__))
print(dirSelf)



class CustomPanel(bpy.types.Panel):
  """A Custom Panel in the Viewport Toolbar"""
  bl_label = "RbhusPipe Tools"
  bl_space_type = 'VIEW_3D'
  bl_region_type = 'TOOLS'

  def draw(self, context):
    layout = self.layout

    row = layout.row()
    row.label(text="Add Objects:")

    split = layout.split()
    col = split.column(align=True)

    col.operator("rbhuspipe.version_up", text="register asset")
    col.operator("mesh.primitive_torus_add", text="WTF2")

class versionUp(bpy.types.Operator):
  bl_idname = "rbhuspipe.version_up"
  bl_label = "register asset"
  #bl_options = {"UNDO"}
  
  def invoke(self,context,event):
    os.system("/home/shrinidhi/bin/gitHub/rbhus/rbhusUI/rbhusRender.py &")
    return({"FINISHED"})
  
  

def register():
  bpy.utils.register_class(versionUp)
  bpy.utils.register_class(CustomPanel)
  

def unregister():
  bpy.utils.unregister_class(CustomPanel)
  bpy.utils.unregister_class(versionUp)

if __name__ == "__main__":
  register()