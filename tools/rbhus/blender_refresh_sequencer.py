import bpy


def my_handler(scene):
    bpy.ops.sequencer.refresh_all()
#    print("Frame Change", scene.frame_current)

bpy.app.handlers.frame_change_post.append(my_handler)