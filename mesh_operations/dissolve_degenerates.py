import bpy
import bmesh
from ..helpers.popup import show_popup


class TT_OT_dissolve_degenerates(bpy.types.Operator):
    bl_idname = "tt.dissolve_degenerates"
    bl_label = "Dissolve Degenerates"
    # bl_description = "Remove weird postfixes from mat names"
    bl_options = {'UNDO'}

    def execute(self, context):
        msg = None
        mesh = context.object.data
        bm = bmesh.new()
        bm.from_mesh(mesh)
        
        og_count = [bm.edges.__len__(), bm.faces.__len__()]
        
        bmesh.ops.dissolve_degenerate(bm, dist = 0.0001, edges = bm.edges)
        
        bm.to_mesh(mesh)
        
        # if count changed, then some parts was removed as "bad geometry"
        if og_count != [bm.edges.__len__(), bm.faces.__len__()]:
            msg = f"{og_count[1]-bm.faces.__len__()} faces & {og_count[0]-bm.edges.__len__()} edges removed"
        else:
            msg = f"Degenerates not found"
            
        bm.free()
        show_popup(msg)

        return {'FINISHED'}


classes = [TT_OT_dissolve_degenerates]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
