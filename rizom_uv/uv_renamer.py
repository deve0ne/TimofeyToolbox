import bpy


class TT_OT_uv_renamer(bpy.types.Operator):
    bl_idname = "tt.uv_replace_to_dots"
    bl_label = "Fix UV names"
    bl_options = {"UNDO"}

    def execute(self, context):
            
        user_mode = bpy.context.object.mode
        if user_mode != "OBJECT":
            bpy.ops.object.mode_set(mode="OBJECT")
        
        for obj in bpy.data.objects:
            if obj.type != 'MESH':
                continue
            
            if obj.data.uv_layers:
                uvs = obj.data.uv_layers
                for uv in uvs:
                    uv.name = uv.name.replace(".", "_")

        bpy.ops.object.mode_set(mode=user_mode)
        return {"FINISHED"}
    

classes = [TT_OT_uv_renamer]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)