import bpy
i = 1
a = {'FINISHED'}
b = {'FINISHED'}
frame_start = 1
frame_end = 1
bpy.context.scene.frame_current = 1
while('FINISHED' in b):
  if(i != 1):
    a = bpy.ops.sequencer.strip_jump(next=True,center=False)
    frame_start = bpy.context.scene.frame_current
  b = bpy.ops.sequencer.strip_jump(next=True,center=False)
  frame_end = bpy.context.scene.frame_current - 1
  bpy.context.scene.frame_start = frame_start
  bpy.context.scene.frame_end = frame_end
  bpy.data.scenes['Scene'].render.filepath = '/tmp/' + str(i).zfill(3) +".mp4"
  # bpy.context.scene.file_format = 'H264'
  # bpy.context.scene.format = 'MPEG4'
  bpy.ops.render.render(animation=True)
  bpy.ops.sequencer.strip_jump(next=False, center=False)
  i = i+1