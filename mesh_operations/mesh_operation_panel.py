import bpy


class TT_PT_mesh_operations(bpy.types.Panel):
    bl_label = "Mesh Operations"
    bl_idname = "TT_PT_mesh_operation"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {"HEADER_LAYOUT_EXPAND"}
    bl_category = "TimofeyToolbox"

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj is not None and obj.type == 'MESH' and obj.mode in {'OBJECT', 'EDIT'}

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.operator("tt.dissolve_degenerates")
        col.operator("tt.uv_replace_to_dots")
        col.operator("tt.box_mapping")
        # col.operator("tt.fix_mat_paths")


classes = (TT_PT_mesh_operations,)


register, unregister = bpy.utils.register_classes_factory(classes)
