import bpy

class SvgCleanUp(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.svg_cleanup"
    bl_label = "SVG cleanup"
    bl_options = {'REGISTER', 'UNDO'}


    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        bpy.ops.object.convert(target='MESH')
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all()
        bpy.ops.mesh.dissolve_limited()
        bpy.ops.mesh.remove_doubles()
        bpy.ops.object.editmode_toggle()
        return {'FINISHED'}


#def register():
    #bpy.utils.register_class(SvgCleanUp)


#def unregister():
    #bpy.utils.unregister_class(SvgCleanUp)


#if __name__ == "__main__":
    #register()

    ## test call
##    bpy.ops.object.svg_cleanup()

classes = (
    SvgCleanUp,
)
