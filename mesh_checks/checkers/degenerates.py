import bpy
import bmesh
from .. import mesh_check_helpers


class TT_OT_find_degenerates(bpy.types.Operator):
    bl_idname = "tt.find_degenerates"
    bl_label = "Degenerates"

    @staticmethod
    def main_check(obj, info):
        bm = mesh_check_helpers.bmesh_copy_from_object(
            obj, transform=False, triangulate=False)

        # It's difficult to track which elements were removed, so we create a custom layers
        face_layer = bm.faces.layers.int.new('face_id')
        edge_layer = bm.edges.layers.int.new('edge_id')

        original_face_ids = set()
        original_edge_ids = set()

        for face in bm.faces:
            face[face_layer] = face.index
            original_face_ids.add(face.index)
        for edge in bm.edges:
            edge[edge_layer] = edge.index
            original_edge_ids.add(edge.index)

        bmesh.ops.dissolve_degenerate(bm, dist=0.0001, edges=bm.edges)

        # Collect the identifiers of the remaining faces and edges
        new_face_ids = {face[face_layer] for face in bm.faces}
        new_edge_ids = {edge[edge_layer] for edge in bm.edges}

        # Determine which faces and edges were deleted
        deleted_face_ids = original_face_ids - new_face_ids
        deleted_edge_ids = original_edge_ids - new_edge_ids

        info.append((f"Degenerate Faces: {len(deleted_face_ids)}", (bmesh.types.BMFace, deleted_face_ids)))
        info.append((f"Degenerate Edges: {len(deleted_edge_ids)}", (bmesh.types.BMEdge, deleted_edge_ids)))

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
