import bpy
import bmesh
from ...helpers import mesh_helpers


class TT_OT_find_incorrect_geometry(bpy.types.Operator):
    bl_idname = "tt.find_incorrect_geometry"
    bl_label = "Incorrect Geometry"
    bl_description = "Finds edges with > 2 polygons connected"

    @staticmethod
    def main_check(obj, info):
        bm = mesh_helpers.bmesh_copy_from_object(
            obj, transform=False, triangulate=False)

        # Finding incorrect geometry
        incorrect_edges = [
            edge.index for edge in bm.edges if edge.link_faces.__len__() > 2]

        # Storing the results in the object
        info.append(
            (("Incorrect Edges: {}").format(
                len(incorrect_edges)),
                (bmesh.types.BMEdge,
                 incorrect_edges)))

        bm.free()

    def execute(self, context):
        return mesh_helpers.execute_check(self, context)


classes = (TT_OT_find_incorrect_geometry,)


register, unregister = bpy.utils.register_classes_factory(classes)
