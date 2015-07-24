import bpy
i = 0
a = {'FINISHED'}
while('FINISHED' in a):
  bpy.data.scenes['Scene'].render.filepath = '/blueprod/STOR2/stor2/ep001_beautyAndTheFeast/preproduction/storyboard/shrinidhi/' + str(i).zfill(3)
  bpy.ops.render.render(write_still=True)
  a = bpy.ops.sequencer.strip_jump()
  i = i+1