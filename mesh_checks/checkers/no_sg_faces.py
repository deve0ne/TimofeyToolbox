import bpy
import bmesh
from .. import mesh_check_helpers


class OBJECT_OT_FindNoSGfaces(bpy.types.Operator):
    bl_idname = "tt.find_no_sg_faces"
    bl_label = "Check Smoothing groups"
    bl_options = {"UNDO"}

    @staticmethod
    def main_check(obj, info):
        bm = mesh_check_helpers.bmesh_copy_from_object(
            obj, transform=False, triangulate=False)
        no_sg_faces = []

        if hasattr(obj, "SG"):
            attr = obj.attributes["SG"].data

            no_sg_faces = [index for index,
                           face in enumerate(attr) if face.value == 0]
        else:
            # Костыль, но иное придумывать лень
            no_sg_faces = [face.index for face in bm.faces]

        info.append(
            (("No SG faces: {}").format(
                len(no_sg_faces)),
                (bmesh.types.BMFace,
                 no_sg_faces)))

        bm.free()

    def execute(self, context):
        return mesh_check_helpers.execute_check(self, context)


class OBJECT_OT_SelectNoSGfaces(bpy.types.Operator):
    bl_idname = "tt.select_no_sg_faces"
    bl_label = "Select Faces with No Smooth Group"

    def execute(self, context):
        obj = context.active_object

        if not obj or obj.type != "obj" or "no_sg_faces" not in obj:
            self.report(
                {"WARNING"}, "No faces to select or active object is not a obj"
            )
            return {"CANCELLED"}

        bpy.ops.tt.mode_set(mode="EDIT")

        obj = bmesh.from_edit_mesh(obj.data)
        obj.faces.ensure_lookup_table()

        for index in obj["no_sg_faces"]:
            if index < len(obj.faces):
                obj.faces[index].select_set(True)

        bmesh.update_edit_mesh(obj.data)
        return {"FINISHED"}


classes = [OBJECT_OT_FindNoSGfaces, OBJECT_OT_SelectNoSGfaces]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
