import bpy
import os

i = 1
e = 10017
a = {'FINISHED'}
b = {'FINISHED'}
frame_start = bpy.context.scene.frame_start
frame_end = bpy.context.scene.frame_end
filepath = bpy.data.scenes['Scene'].render.filepath

bpy.context.scene.frame_current = 1
while ('FINISHED' in b):
  if (i != 1):
    a = bpy.ops.sequencer.strip_jump(next=True, center=False)
    frame_start = bpy.context.scene.frame_current
  b = bpy.ops.sequencer.strip_jump(next=True, center=False)
  bpy.ops.sequencer.refresh_all()
  frame_end = bpy.context.scene.frame_current - 1
  bpy.context.scene.frame_start = frame_start
  bpy.context.scene.frame_end = frame_end
  bpy.data.scenes['Scene'].render.filepath = os.path.join(filepath, str(i).zfill(4) + ".mp4")
  bpy.ops.render.render(animation=True)
  bpy.ops.sequencer.strip_jump(next=False, center=False)
  i = i + 1

bpy.data.scenes['Scene'].render.filepath = filepath