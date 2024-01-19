import bpy
                
class OBJECT_PT_MeshOperationsPanel(bpy.types.Panel):
    bl_label = "Mesh Operations"
    bl_idname = "OBJECT_PT_mesh_operation_panel"
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
        col.operator("tt.uv_replace_to_dots", icon="UV")
        col.operator("tt.box_mapping", icon="UV_DATA")
        col.operator("tt.fix_mat_names", icon="UV_DATA")


classes = [OBJECT_PT_MeshOperationsPanel]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

