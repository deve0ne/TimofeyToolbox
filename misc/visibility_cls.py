import bpy

class TT_OT_toggle_visibility_cls(bpy.types.Operator):
    """Toggle visibility of objects with '_cls' in their names in the active collection"""
    bl_idname = "tt.toggle_cls_visibility"
    bl_label = "Toggle collision visibility"
    
    # This variable keeps track of the visibility state
    is_hidden = {}

    def execute(self, context):
        # Get the active collection
        # active_collection = context.view_layer.active_layer_collection.collection
        
        active_collection = context.view_layer.objects.active.users_collection[0]

        # Loop through all objects in the active collection
        for obj in active_collection.objects:
            # Check if the object's name contains '_cls'
            if "_cls" in obj.name:
                # If the object's visibility state is not tracked, track it and hide it
                if obj.name not in self.is_hidden:
                    self.is_hidden[obj.name] = False  # Assume it's initially visible
                # Toggle the visibility based on the stored state
                self.is_hidden[obj.name] = not self.is_hidden[obj.name]
                obj.hide_set(self.is_hidden[obj.name])

        return {'FINISHED'}

classes = (TT_OT_toggle_visibility_cls,)

register, unregister = bpy.utils.register_classes_factory(classes)