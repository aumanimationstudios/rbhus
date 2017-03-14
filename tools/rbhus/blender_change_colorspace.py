import bpy

strips = bpy.data.scenes['Scene'].sequence_editor.sequences_all
# a = {}
for x in strips:
  # a[x.type] = 1
  if(x.type == 'MOVIE'):
    x.colorspace_settings.name = 'sRGB EOTF'
  if (x.type == 'IMAGE' and x.name.endswith(".exr")):
    x.colorspace_settings.name = "Linear"
  else:
    if (x.type == 'IMAGE'):
      x.colorspace_settings.name = 'sRGB EOTF'

# print(a)