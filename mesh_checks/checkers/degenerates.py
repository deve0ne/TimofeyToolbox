import bpy
import bmesh
from .. import mesh_check_helpers


class TT_OT_find_degenerates(bpy.types.Operator):
    bl_idname = "tt.find_degenerates"
    bl_label = "Degenerates"
    bl_options = {"REGISTER", "UNDO"}

    @staticmethod
    def main_check(obj, info):
        bm = mesh_check_helpers.bmesh_copy_from_object(
            obj, transform=False, triangulate=False)

        threshold = 0.0001
        faces_zero = [f.index for f in bm.faces if f.calc_area() <= threshold]
        edges_zero = [e.index for e in bm.edges if e.calc_length()
                      <= threshold]

        # bmesh.ops.dissolve_degenerate(bm, dist = 0.0001, edges = bm.edges)

        info.append((("Degenerate Faces: {}").format(
            len(faces_zero)), (bmesh.types.BMFace, faces_zero)))
        info.append((("Degenerate Edges: {}").format(
            len(edges_zero)), (bmesh.types.BMEdge, edges_zero)))

        bm.free()

    def execute(self, context):
        return mesh_check_helpers.execute_check(self, context)


classes = [TT_OT_find_degenerates]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
