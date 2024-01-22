import bpy

class TT_OT_bounding_box_mode(bpy.types.Operator):
    bl_idname = "tt.bounding_box_mode"
    bl_label = "Show/Hide Bounding Box"
    bl_description = "Enables/Disables Bounding Box on selected objects"
    
    @classmethod
    def poll(cls, context):
        return context.scene is not None
    
    def execute(self, context):
        selected_objects = context.selected_objects
        
        # Check if any object is already in bounding box mode
        bounding_box_mode = any(obj.show_bounds for obj in selected_objects)
        
        # Toggle the display type
        new_display_type = True if not bounding_box_mode else False
        
        for obj in selected_objects:
            # Skip objects that are not meshes or should not be toggled
            if obj.type != 'MESH' or obj.hide_get():
                continue
            
            # Set the display type to bounding box or textured
            obj.show_bounds = new_display_type
        
        return {'FINISHED'}

classes = [TT_OT_bounding_box_mode]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)