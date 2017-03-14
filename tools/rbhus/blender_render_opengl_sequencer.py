import bpy
frame_start = bpy.context.scene.frame_start
frame_end = bpy.context.scene.frame_end
bpy.context.scene.frame_current = frame_start
filepath = bpy.data.scenes['Scene'].render.filepath
while(frame_start <= frame_end):
  bpy.context.scene.frame_current = frame_start
  bpy.data.scenes['Scene'].render.filepath = filepath + str(frame_start).zfill(4)
  bpy.ops.render.opengl(sequencer=True,write_still=True)
  frame_start = frame_start+1