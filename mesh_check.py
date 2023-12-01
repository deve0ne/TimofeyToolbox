import bpy
import bmesh

class OBJECT_OT_CheckFacesAttribute(bpy.types.Operator):
    """Check if Faces of Selected Meshes Have a Specific Attribute Value"""
    bl_idname = "object.check_faces_attribute"
    bl_label = "Check Smoothing groups"
    bl_options = {'REGISTER', 'UNDO'}

    attribute_to_check = "SG"

    def execute(self, context):
        init_mode = bpy.context.object.mode
        # print(init_mode)
        bpy.ops.object.mode_set(mode='OBJECT')

        obj = context.active_object

        if not obj or obj.type != 'MESH':
            self.report({'WARNING'}, "Active object is not a mesh")
            return {'CANCELLED'}

        mesh = obj.data
        if self.attribute_to_check in mesh.attributes:
            attr = mesh.attributes[self.attribute_to_check].data
            faces_with_attr_zero = [index for index, face in enumerate(attr) if face.value == 0]

            # Store the indices in the active object's property
            obj["faces_to_select"] = faces_with_attr_zero
            context.scene.attribute_check_results = f"{len(faces_with_attr_zero)} faces with no smoothing groups."
        else:
            context.scene.attribute_check_results = "Attribute not found on active object."

        bpy.ops.object.mode_set(mode = init_mode)
        return {'FINISHED'}

class OBJECT_OT_SelectFacesWithAttrZero(bpy.types.Operator):
    """Select Faces with Attribute Value Zero"""
    bl_idname = "object.select_faces_with_attr_zero"
    bl_label = "Select Faces with No Smooth Group"

    def execute(self, context):
        obj = context.active_object

        if not obj or obj.type != 'MESH' or "faces_to_select" not in obj:
            self.report({'WARNING'}, "No faces to select or active object is not a mesh")
            return {'CANCELLED'}

        # Switch to edit mode
        bpy.ops.object.mode_set(mode='EDIT')

        # Select faces
        mesh = bmesh.from_edit_mesh(obj.data)
        mesh.faces.ensure_lookup_table()
        for index in obj["faces_to_select"]:
            if index < len(mesh.faces):
                mesh.faces[index].select_set(True)

        bmesh.update_edit_mesh(obj.data)
        return {'FINISHED'}

def register():
    bpy.utils.register_class(OBJECT_OT_CheckFacesAttribute)
    bpy.utils.register_class(OBJECT_OT_SelectFacesWithAttrZero)
    bpy.types.Scene.attribute_check_results = bpy.props.StringProperty(name="Results", default="")

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_CheckFacesAttribute)
    bpy.utils.unregister_class(OBJECT_OT_SelectFacesWithAttrZero)

if __name__ == "__main__":
    register()
