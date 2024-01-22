import bpy
from bpy.types import Operator
import bmesh
from .. import mesh_check_helpers


class TT_OT_check_manifold(Operator):
    bl_idname = "tt.check_manifold"
    bl_label = "Manifold"
    bl_description = "Check for geometry is solid (has valid inside/outside) and correct normals"

    @staticmethod
    def main_check(obj, info):
        import array

        bm = mesh_check_helpers.bmesh_copy_from_object(
            obj, transform=False, triangulate=False)

        edges_non_manifold = array.array(
            'i', (i for i, ele in enumerate(bm.edges) if not ele.is_manifold))
        # edges_non_contig = array.array(
        #     'i',
        #     (i for i, ele in enumerate(bm.edges) if ele.is_manifold and (not ele.is_contiguous)),
        # )

        info.append((
            ("Non Manifold Edges: {}").format(
                len(edges_non_manifold)),
            (bmesh.types.BMEdge,
             edges_non_manifold)))
        # info.append(("Bad Contiguous Edges: {}").format(len(edges_non_contig)), (bmesh.types.BMEdge, edges_non_contig)))

        bm.free()

    def execute(self, context):
        return mesh_check_helpers.execute_check(self, context)


classes = [TT_OT_check_manifold]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
