import bpy
import bmesh
from ...helpers import mesh_helpers


class TT_OT_find_loose_verts_edges(bpy.types.Operator):
    bl_idname = "tt.find_loose_verts_edges"
    bl_label = "Loose Verts & Edges"
    bl_description = "Finds verts without linked edges and edges without linked faces"

    @staticmethod
    def main_check(obj, info):
        bm = mesh_helpers.bmesh_copy_from_object(
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
        return mesh_helpers.execute_check(self, context)


classes = (TT_OT_find_loose_verts_edges,)


register, unregister = bpy.utils.register_classes_factory(classes)