import bpy
from bmesh import types
from ..helpers import report
from ..helpers.select_report import TT_OT_select_report


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
    
            # Group entries by mesh name
            grouped_info = {}
            for i, (name, text, data) in enumerate(info):
                if name not in grouped_info:
                    grouped_info[name] = []
                grouped_info[name].append((i, text, data))
    
            # Iterate through unique mesh names and create labels
            for name, entries in grouped_info.items():
                col.label(text=name)  # Label for the mesh name
                for i, text, data in entries:
                    if is_edit and data and data[1]:
                        bm_type, _bm_array = data
                        col.operator("tt.select_report", text=text,
                                     icon=self._type_to_icon[bm_type]).index = i
                    elif data and data[1]:  # If we want to show 0 result check's, replace this to "else"
                        col.label(text=text)

    def draw(self, context):
        layout = self.layout

        batch_mode = False
        if len(context.selected_objects) > 1:
            layout.label(text="Batch mode: Multiple objects selected", icon='INFO')
            batch_mode = True

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


classes = (TT_PT_mesh_check, TT_OT_select_report)


register, unregister = bpy.utils.register_classes_factory(classes)
