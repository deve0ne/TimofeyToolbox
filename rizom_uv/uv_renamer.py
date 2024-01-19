import bpy


class UVrenamer(bpy.types.Operator):
    bl_idname = "tt.uv_replace_to_dots"
    bl_label = "Replace underscores to dots in UV names"

    def execute(self, context):
        for obj in bpy.data.objects:
            try:
                uvs = obj.data.uv_layers
                for uv in uvs:
                    uv.name = uv.name.replace(".", "_")
            except:
                return {"FINISHED"}

        return {"FINISHED"}
    

classes = [UVrenamer]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)