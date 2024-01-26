import bpy

bpy.types.Scene.tt_keep_as_modifier = bpy.props.BoolProperty(
    name="Keep as Modifier",
    description="Keep box mapping modifier",
    default=False
)

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

        # Add a box to group the box mapping options
        # box = col.box()
        box_mapping_row = col.row()
        box_mapping_row.operator("tt.box_mapping", text="Box Mapping")
        box_mapping_row.prop(context.scene, "tt_keep_as_modifier", text="Keep as Modifier")
            # col.operator("tt.fix_mat_paths")


classes = (TT_PT_mesh_operations,)


register, unregister = bpy.utils.register_classes_factory(classes)
