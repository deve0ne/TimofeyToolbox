import bpy


class TT_OT_uv_renamer(bpy.types.Operator):
    bl_idname = "tt.uv_replace_to_dots"
    bl_label = "Fix UV names"
    bl_description = "Replaces dots to underscores in all UV names on scene for RizomUV support"
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


classes = (TT_OT_uv_renamer,)


register, unregister = bpy.utils.register_classes_factory(classes)
