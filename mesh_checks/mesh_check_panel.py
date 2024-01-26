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
            main_box = layout.box()
            col = main_box.column()

            # Group entries by mesh name
            grouped_info = {}
            for i, (name, text, data) in enumerate(info):
                if name not in grouped_info:
                    grouped_info[name] = []
                grouped_info[name].append((i, text, data))

            # Determine if there's only one mesh in the info
            batch_mode = len(grouped_info) > 1

            # Flag to track if any errors are found
            any_errors_found = False

            # Iterate through unique mesh names and create labels
            for name, entries in grouped_info.items():
                has_nonzero_entry = any(data and data[1] for _, text, data in entries)
                any_errors_found |= has_nonzero_entry  # Update the flag if any errors are found

                if has_nonzero_entry or not batch_mode:
                    # if not batch_mode:
                    col.label(text=name, icon='OBJECT_DATA')
                    mesh_box = col.box()
                    mesh_col = mesh_box.column()

                if has_nonzero_entry:
                    for i, text, data in entries:
                        if is_edit and data and data[1]:
                            bm_type, _bm_array = data
                            mesh_col.operator("tt.select_report", text=text,
                                              icon=self._type_to_icon[bm_type]).index = i
                        elif (data and data[1]):
                            mesh_col.label(text=text)
                elif not batch_mode:
                    mesh_col.label(text="No errors were found")

            # If in batch mode and no errors were found, display a single message
            if batch_mode and not any_errors_found:
                col.label(text=f"No errors were found in {len(grouped_info.items())} selected")

    def draw(self, context):
        layout = self.layout

        col = layout.column(align=True)
        col.operator("tt.find_no_sg_faces")
        col.operator("tt.find_loose_verts_edges")
        col.operator("tt.find_incorrect_geometry")
        col.operator("tt.find_degenerates")
        # col.operator("tt.check_manifold")

        layout.operator("tt.check_all")

        self.draw_report(context)

        layout.separator()

        layout.label(text="Viewer modes")

        layout.operator("tt.bounding_box_mode")


classes = (TT_PT_mesh_check, TT_OT_select_report)


register, unregister = bpy.utils.register_classes_factory(classes)
