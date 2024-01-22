import bpy


class TT_OT_uv_renamer(bpy.types.Operator):
    bl_idname = "tt.uv_replace_to_dots"
    bl_label = "Fix UV names"
    bl_options = {"UNDO"}

    def execute(self, context):
        for obj in bpy.data.objects:
            try:
                uvs = obj.data.uv_layers
                for uv in uvs:
                    uv.name = uv.name.replace(".", "_")
            except:
                return {"ERROR"}

        return {"FINISHED"}
    

classes = [TT_OT_uv_renamer]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)