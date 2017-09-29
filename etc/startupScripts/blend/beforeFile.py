import bpy
import addon_utils
import sys
bpy.context.user_preferences.filepaths.use_relative_paths= False


def isLessThanEqualVersion(ver):
  app_version = list(bpy.app.version)
  if(type(ver) == str):
    ver_list = [int(x) for x in ver.split(".")]
    if(ver_list[0] >= app_version[0]):
      print(ver_list[0],app_version[0])
      if (ver_list[1] >= app_version[1]):
        print(ver_list[1], app_version[1])
        if (ver_list[2] >= app_version[2]):
          print(ver_list[2], app_version[2])
          return True
    return False
    # elif(ver_list[1] < app_version[1]):
    #   return True
    # elif(ver_list[2] < app_version[2]):
    #   return True
    # else:
    #   return False




if(isLessThanEqualVersion("2.78.0")):
  bpy.context.user_preferences.filepaths.use_load_ui = False
  print("NOT LOADING UI")
bpy.context.user_preferences.filepaths.save_version=0
bpy.context.user_preferences.system.use_scripts_auto_execute = True
bpy.context.user_preferences.filepaths.temporary_directory = "/crap/LOCAL.crap"

try:
  addon_utils.disable("ui_layer_manager")
except:
  print(sys.exc_info())

try:
  addon_utils.enable("ui_layer_manager",default_set=True)
  print("ui_layer_manager enabled")
except:
  print(sys.exc_info())

if(isLessThanEqualVersion("2.78.0")):
  try:
    addon_utils.disable("bone_selection_groups")
  except:
    print(sys.exc_info())

  try:
    addon_utils.enable("bone_selection_groups")
    print("bone_selection_groups enabled")
  except:
    print(sys.exc_info())

else:
  try:
    addon_utils.disable("bone_selection_sets")
  except:
    print(sys.exc_info())

  try:
    addon_utils.enable("bone_selection_sets")
    print("bone_selection_sets enabled")
  except:
    print(sys.exc_info())
# addon_utils.disable("camera_add_title_safe")
# addon_utils.enable("camera_add_title_safe")




