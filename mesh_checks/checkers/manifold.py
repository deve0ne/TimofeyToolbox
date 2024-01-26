import bpy
from bpy.types import Operator
import bmesh
from ...helpers import mesh_helpers


class TT_OT_check_manifold(Operator):
    bl_idname = "tt.check_manifold"
    bl_label = "Manifold"
    bl_description = "Check for geometry is solid. Useful for phys collisions"

    @staticmethod
    def main_check(obj, info):
        import array

        bm = mesh_helpers.bmesh_copy_from_object(
            obj, transform=False, triangulate=False)

        edges_non_manifold = array.array(
            'i', (i for i, ele in enumerate(bm.edges) if not ele.is_manifold))
        # edges_non_contig = array.array(
        #     'i',
        #     (i for i, ele in enumerate(bm.edges) if ele.is_manifold and (not ele.is_contiguous)),
        # )

        info.append((obj.name, f"Non Manifold Edges: {len(edges_non_manifold)}",
                    (bmesh.types.BMEdge, edges_non_manifold)))
        # info.append(obj.name, ("Bad Contiguous Edges: {}").format(len(edges_non_contig)), (bmesh.types.BMEdge, edges_non_contig)))

        bm.free()

    def execute(self, context):
        return mesh_helpers.execute_check(self, context)


classes = (TT_OT_check_manifold,)


register, unregister = bpy.utils.register_classes_factory(classes)
