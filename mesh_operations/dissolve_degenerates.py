import bpy
import bmesh
from ..helpers.popup import show_popup
from ..helpers import mesh_helpers


class TT_OT_dissolve_degenerates(bpy.types.Operator):
    bl_idname = "tt.dissolve_degenerates"
    bl_label = "Dissolve Degenerates"
    bl_description = "Dissolves degenerate edges and faces in the mesh. Use with caution!"
    bl_options = {'UNDO'}

    # @classmethod
    # def poll(cls, context):
    #     obj = context.active_object
    #     return obj is not None and obj.type == 'MESH' and (obj.mode in {'OBJECT, EDIT'})

    def execute(self, context):
        obj = context.active_object
        bm = mesh_helpers.bmesh_from_object(obj)
        og_count = [bm.edges.__len__(), bm.faces.__len__()]

        bmesh.ops.dissolve_degenerate(bm, dist=0.0001, edges=bm.edges)

        mesh_helpers.bmesh_to_object(obj, bm)

        # if count changed, then some parts was removed as "bad geometry"
        if og_count != [bm.edges.__len__(), bm.faces.__len__()]:
            msg = f"{og_count[1]-bm.faces.__len__()} faces & {og_count[0]-bm.edges.__len__()} edges removed"
        else:
            msg = f"Degenerates not found"

        show_popup(msg)
        bm.free()

        return {'FINISHED'}


classes = (TT_OT_dissolve_degenerates,)


register, unregister = bpy.utils.register_classes_factory(classes)
