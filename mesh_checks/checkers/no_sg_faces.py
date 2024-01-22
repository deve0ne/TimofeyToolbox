import bpy
import bmesh
from .. import mesh_check_helpers


class TT_OT_find_no_sg_faces(bpy.types.Operator):
    bl_idname = "tt.find_no_sg_faces"
    bl_label = "No SG Faces"
    bl_options = {"UNDO"}

    @staticmethod
    def main_check(obj, info):
        bm = mesh_check_helpers.bmesh_copy_from_object(
            obj, transform=False, triangulate=False)
        
        sg_layer = bm.faces.layers.int.get("SG")
        
        no_sg_faces = []
        
        for face in bm.faces:
            try:
                # Try to access the SG attribute. If the attribute is missing, an exception will be raised.
                if face[sg_layer] == 0:
                    no_sg_faces.append(face.index)
            except KeyError:
                # The SG attribute is missing for this face, so we add it to the list.
                no_sg_faces.append(face.index)
        
        
        info.append(
            (("No SG faces: {}").format(
                len(no_sg_faces)),
                (bmesh.types.BMFace,
                 no_sg_faces)))

        bm.free()

    def execute(self, context):
        return mesh_check_helpers.execute_check(self, context)


class TT_OT_SelectNoSGfaces(bpy.types.Operator):
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


classes = [TT_OT_find_no_sg_faces, TT_OT_SelectNoSGfaces]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
