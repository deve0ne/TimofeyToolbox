import bpy


class OBJECT_PT_MeshCheckPanel(bpy.types.Panel):
    bl_label = "Mesh Check"
    bl_idname = "OBJECT_PT_mesh_check_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {"HEADER_LAYOUT_EXPAND"}
    bl_category = "TimofeyToolbox"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        obj = context.active_object

        layout.operator("object.find_no_sg_faces", text="Check Smooth Groups")
        layout.operator(
            "object.find_loose_verts_edges", text="Find Loose Vertices and Edges"
        )

        row = layout.row()
        row.label(text="Results:")

        results_box = layout.box()

        if obj and obj.type == "MESH" and "no_sg_faces" in obj:
            no_sg_faces_count = len(obj["no_sg_faces"])

            resultText = (
                f"{no_sg_faces_count} Faces with no Smooth Group"
                if no_sg_faces_count != 0
                else "All faces have Smoothing groups"
            )

            if context.mode == "EDIT_MESH":
                results_box.operator("object.select_no_sg_faces", text=resultText)
            elif context.mode == "OBJECT":
                results_box.label(text=resultText)

            if obj and obj.type == "MESH" and ("loose_verts" in obj or "loose_edges" in obj):
                loose_verts_count = len(obj["loose_verts"]) if "loose_verts" in obj else 0
                loose_edges_count = len(obj["loose_edges"]) if "loose_edges" in obj else 0
    
                # Combined text for loose vertices and edges
                combined_text = f"Loose: {loose_verts_count} Verts & {loose_edges_count} Edges"
    
                # Check the mode to determine if it should be a label or a button
                if context.mode == "EDIT_MESH":
                    # In Edit mode, display as a button for selection
                    if loose_verts_count > 0 or loose_edges_count > 0:
                        results_box.operator("object.select_loose_verts_edges", text=combined_text)
                else:
                    # In Object mode (or any other mode), display as a label
                    results_box.label(text=combined_text)


class OBJECT_PT_MeshOperationsPanel(bpy.types.Panel):
    bl_label = "Mesh Operations"
    bl_idname = "OBJECT_PT_mesh_operation_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {"HEADER_LAYOUT_EXPAND"}
    bl_category = "TimofeyToolbox"

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.operator("mesh.remap_dub_materials", icon="MATERIAL")
        col.operator("mesh.uv_replace_to_dots", icon="UV")
        col.operator("mesh.box_mapping", icon="UV_DATA")
        col.operator("mesh.advanced_init_smooth_groups", icon="UV_DATA")
        col.operator("mesh.fix_mat_names", icon="UV_DATA")
        
        



classes = (OBJECT_PT_MeshOperationsPanel, OBJECT_PT_MeshCheckPanel)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
