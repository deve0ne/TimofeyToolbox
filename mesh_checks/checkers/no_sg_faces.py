import bpy
import bmesh
from ...helpers import mesh_helpers


class TT_OT_find_no_sg_faces(bpy.types.Operator):
    bl_idname = "tt.find_no_sg_faces"
    bl_label = "No SG Faces"
    bl_description = "Finds faces without assigned SG"

    @staticmethod
    def main_check(obj, info):
        bm = mesh_helpers.bmesh_copy_from_object(
            obj, transform=False, triangulate=False)

        sg_layer = bm.faces.layers.int.get("SG")

        no_sg_faces = []

        if sg_layer is not None:
            for face in bm.faces:
                try:
                    # Try to access the SG attribute. If the attribute is missing, an exception will be raised.
                    if face[sg_layer] == 0:
                        no_sg_faces.append(face.index)
                except KeyError:
                    # The SG attribute is missing for this face, so we add it to the list.
                    no_sg_faces.append(face.index)
        else:
            no_sg_faces = [face.index for face in bm.faces]

        info.append((obj.name, f"No SG faces: {len(no_sg_faces)}",
                (bmesh.types.BMFace, no_sg_faces)))

        bm.free()

    def execute(self, context):
        return mesh_helpers.execute_check(self, context)

classes = (TT_OT_find_no_sg_faces,)


register, unregister = bpy.utils.register_classes_factory(classes)
