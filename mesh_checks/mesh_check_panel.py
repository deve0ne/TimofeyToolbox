import bpy
from . import report
from bmesh import types
from .select_report import TT_OT_select_report


class TT_PT_mesh_check(bpy.types.Panel):
    bl_label = "Mesh Check"
    bl_idname = "TT_PT_mesh_check"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {"HEADER_LAYOUT_EXPAND"}
    bl_category = "TimofeyToolbox"

    _type_to_icon = {
        types.BMVert: 'VERTEXSEL',
        types.BMEdge: 'EDGESEL',
        types.BMFace: 'FACESEL',
    }

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
                    col.operator("tt.select_report", text=text,
                                 icon=self._type_to_icon[bm_type]).index = i
                else:
                    col.label(text=text)

    def draw(self, context):
        layout = self.layout

        layout.label(text="Checks")
        
        col = layout.column(align=True)
        col.operator("tt.find_no_sg_faces")
        col.operator("tt.find_loose_verts_edges")
        col.operator("tt.find_incorrect_geometry")
        col.operator("tt.find_degenerates")
        col.operator("tt.check_manifold")

        layout.operator("tt.check_all")

        self.draw_report(context)
    
        layout.separator()
        
        layout.label(text="Viewer modes")
        
        layout.operator("tt.bounding_box_mode")


classes = [TT_PT_mesh_check, TT_OT_select_report]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
