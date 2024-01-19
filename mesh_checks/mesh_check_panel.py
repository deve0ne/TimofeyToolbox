import bpy
from . import report
from .select_report import MESH_OT_print3d_select_report

class OBJECT_PT_MeshCheckPanel(bpy.types.Panel):
    bl_label = "Mesh Check"
    bl_idname = "OBJECT_PT_mesh_check_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {"HEADER_LAYOUT_EXPAND"}
    bl_category = "TimofeyToolbox"
    
    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj is not None and obj.type == 'MESH' and obj.mode in {'OBJECT', 'EDIT'}

    def draw_report(self, context):
        layout = self.layout
        info = report.info()
        if info:
            is_edit = context.edit_object is not None
            layout.label(text="Result")
            box = layout.box()
            col = box.column()
            for i, (text, data) in enumerate(info):
                if is_edit and data and data[1]:
                    bm_type, _bm_array = data
                    col.operator("tt.select_report", text=text,).index = i
                else:
                    col.label(text=text)

    def draw(self, context):
        layout = self.layout
        # obj = context.active_object
        
        layout.label(text="Checks")
        col = layout.column(align=True)
        col.operator("tt.find_no_sg_faces", text="No SG faces")
        col.operator("tt.find_loose_verts_edges", text="Loose Verts & Edges")
        col.operator("tt.find_incorrect_geometry", text="Incorrect Geometry")
        
        layout.operator("tt.check_all", text="Check All")
        
        self.draw_report(context)
        
        
classes = [OBJECT_PT_MeshCheckPanel, MESH_OT_print3d_select_report]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)