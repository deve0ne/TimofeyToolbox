import bpy
from bpy.types import Panel

class OBJECT_PT_MeshCheckPanel(bpy.types.Panel):
    bl_label = "Mesh Check"
    bl_idname = "OBJECT_PT_mesh_check_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'HEADER_LAYOUT_EXPAND'}
    bl_category = 'TimofeyToolbox'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        obj = context.active_object

        # Operator for checking attributes
        check_op = layout.operator("object.check_faces_attribute", text="Check Smooth Groups")

        # Centered label for the results section
        row = layout.row()
        # row.alignment = 'CENTER'
        row.label(text="Results:")

        # Create a box for results
        results_box = layout.box()

        if obj and obj.type == 'MESH':
            # Check if we are in Edit Mode
            if context.mode == 'EDIT_MESH' and "faces_to_select" in obj:
                # Button for selecting faces - active in Edit Mode
                select_faces_op = results_box.operator(
                    "object.select_faces_with_attr_zero", 
                    text=f"{len(obj['faces_to_select'])} Faces with no Smooth Group"
                )
            elif context.mode == 'OBJECT':
                # Text field for attribute results - visible in Object Mode
                results_box.label(text=scene.attribute_check_results)

class OBJECT_PT_MeshOperationsPanel(bpy.types.Panel):
    bl_label = "Mesh Operations"
    bl_idname = "OBJECT_PT_mesh_operation_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'HEADER_LAYOUT_EXPAND'}
    bl_category = 'TimofeyToolbox'
    
    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.operator("mesh.remap_dub_materials", icon="MATERIAL")
        col.operator("mesh.uv_replace_to_dots", icon="UV")
        col.operator("mesh.box_mapping", icon="UV_DATA")

    

def register():
    bpy.utils.register_class(OBJECT_PT_MeshOperationsPanel)
    bpy.utils.register_class(OBJECT_PT_MeshCheckPanel)

def unregister():
    bpy.utils.unregister_class(OBJECT_PT_MeshOperationsPanel)
    bpy.utils.unregister_class(OBJECT_PT_MeshCheckPanel)
