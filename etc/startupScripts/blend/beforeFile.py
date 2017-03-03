import bpy
import addon_utils
bpy.context.user_preferences.filepaths.use_relative_paths= False
if(str(bpy.app.version).find("(2, 78") < 0 ):
  bpy.context.user_preferences.filepaths.use_load_ui = False
bpy.context.user_preferences.filepaths.save_version=0
bpy.context.user_preferences.system.use_scripts_auto_execute = True
addon_utils.disable("ui_layer_manager")
addon_utils.enable("ui_layer_manager")
addon_utils.disable("bone_selection_groups")
addon_utils.enable("bone_selection_groups")
# addon_utils.disable("camera_add_title_safe")
# addon_utils.enable("camera_add_title_safe")




