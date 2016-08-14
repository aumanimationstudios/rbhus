import bpy
import sys
import os
bpy.context.scene.unit_settings.system = 'IMPERIAL'
bpy.ops.file.make_paths_absolute()
bpy.context.scene.render.fps = 24
bpy.context.scene.render.fps_base = 1
# bpy.context.scene.render.use_single_layer = False

try:
  assPath = os.environ['rp_assets_path']
  bpy.context.scene.render.use_stamp = True
  bpy.context.scene.render.use_stamp_time = False
  bpy.context.scene.render.use_stamp_date = False
  bpy.context.scene.render.use_stamp_render_time = False
  bpy.context.scene.render.use_stamp_frame = True
  bpy.context.scene.render.use_stamp_scene = False
  bpy.context.scene.render.use_stamp_camera = False
  bpy.context.scene.render.use_stamp_filename = False
  bpy.context.scene.render.use_stamp_note = True

  try:
    if(os.environ['rp_sequenceScenes_sFrame'] != os.environ['rp_sequenceScenes_eFrame']):
      bpy.context.scene.frame_start = int(os.environ['rp_sequenceScenes_sFrame'])
      bpy.context.scene.frame_end = int(os.environ['rp_sequenceScenes_eFrame'])
    else:
      if(os.environ['rp_assets_fRange'] != "1"):
        bpy.context.scene.frame_start = int(os.environ['rp_assets_fRange'].split("-")[0])
        bpy.context.scene.frame_end = int(os.environ['rp_assets_fRange'].split("-")[1])
  except:
    print(str(sys.exc_info()))

  if(os.environ['rp_assets_fileType'] != "default"):
    bpy.context.scene.render.stamp_note_text = ":".join(assPath.split(":")[0:-1])
  else:
    bpy.context.scene.render.stamp_note_text = assPath
except:
  bpy.context.scene.render.use_stamp = False
  print(str(sys.exc_info()))



  


