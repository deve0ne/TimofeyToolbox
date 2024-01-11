import bpy
import bmesh


class OBJECT_OT_FindNoSGfaces(bpy.types.Operator):
    bl_idname = "object.find_no_sg_faces"
    bl_label = "Check Smoothing groups"
    bl_options = {"UNDO"}

    def execute(self, context):
        original_mode = bpy.context.object.mode
        bpy.ops.object.mode_set(mode="OBJECT")

        obj = context.active_object
        mesh = obj.data

        if not obj or obj.type != "MESH":
            self.report({"WARNING"}, "Active object is not a mesh")
            return {"CANCELLED"}

        if "SG" in mesh.attributes:
            attr = mesh.attributes["SG"].data
            no_sg_faces = [index for index,
                           face in enumerate(attr) if face.value == 0]

            obj["no_sg_faces"] = no_sg_faces

        if original_mode == "EDIT":
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.object.select_no_sg_faces()

        return {"FINISHED"}


class OBJECT_OT_SelectNoSGfaces(bpy.types.Operator):
    bl_idname = "object.select_no_sg_faces"
    bl_label = "Select Faces with No Smooth Group"

    def execute(self, context):
        obj = context.active_object

        if not obj or obj.type != "MESH" or "no_sg_faces" not in obj:
            self.report(
                {"WARNING"}, "No faces to select or active object is not a mesh"
            )
            return {"CANCELLED"}

        bpy.ops.object.mode_set(mode="EDIT")

        mesh = bmesh.from_edit_mesh(obj.data)
        mesh.faces.ensure_lookup_table()

        for index in obj["no_sg_faces"]:
            if index < len(mesh.faces):
                mesh.faces[index].select_set(True)

        bmesh.update_edit_mesh(obj.data)
        return {"FINISHED"}


classes = [OBJECT_OT_FindNoSGfaces, OBJECT_OT_SelectNoSGfaces]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
