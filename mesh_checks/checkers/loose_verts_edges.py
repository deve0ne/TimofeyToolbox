import bpy
import bmesh
from .. import mesh_check_helpers


class TT_OT_find_loose_verts_edges(bpy.types.Operator):
    bl_idname = "tt.find_loose_verts_edges"
    bl_label = "Loose Verts & Edges"
    bl_options = {"REGISTER", "UNDO"}

    @staticmethod
    def main_check(obj, info):
        bm = mesh_check_helpers.bmesh_copy_from_object(
            obj, transform=False, triangulate=False)

        # Finding loose vertices and edges
        loose_verts = [v.index for v in bm.verts if not v.link_edges]
        loose_edges = [e.index for e in bm.edges if not e.link_faces]

        # Storing the results in the object
        info.append(
            (("Loose verts: {}").format(
                len(loose_verts)),
                (bmesh.types.BMVert,
                 loose_verts)))

        info.append(
            (("Loose edges: {}").format(
                len(loose_edges)),
                (bmesh.types.BMEdge,
                 loose_edges)))

        bm.free()

    def execute(self, context):
        return mesh_check_helpers.execute_check(self, context)


classes = [TT_OT_find_loose_verts_edges]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
