from ..helpers import report
import bmesh


def execute_check(self, context):
    info = []

    for obj in context.selected_objects:
        if obj.type == 'MESH':
            self.main_check(obj, info)

    report.update(*info)
    return {'FINISHED'}


def bmesh_copy_from_object(obj, transform=True, triangulate=True, apply_modifiers=False):
    """Returns a transformed, triangulated copy of the mesh"""

    assert obj.type == 'MESH'

    if apply_modifiers and obj.modifiers:
        import bpy
        depsgraph = bpy.context.evaluated_depsgraph_get()
        obj_eval = obj.evaluated_get(depsgraph)
        me = obj_eval.to_mesh()
        bm = bmesh.new()
        bm.from_mesh(me)
        obj_eval.to_mesh_clear()
    else:
        me = obj.data
        if obj.mode == 'EDIT':
            bm_orig = bmesh.from_edit_mesh(me)
            bm = bm_orig.copy()
        else:
            bm = bmesh.new()
            bm.from_mesh(me)

    if transform:
        matrix = obj.matrix_world.copy()
        if not matrix.is_identity:
            bm.transform(matrix)
            # Update normals if the matrix has no rotation.
            matrix.translation.zero()
            if not matrix.is_identity:
                bm.normal_update()

    if triangulate:
        bmesh.ops.triangulate(bm, faces=bm.faces)

    return bm


def bmesh_from_object(obj):
    """Object/Edit Mode get mesh, use bmesh_to_object() to write back."""
    me = obj.data

    if obj.mode == 'EDIT':
        bm = bmesh.from_edit_mesh(me)
    else:
        bm = bmesh.new()
        bm.from_mesh(me)

    return bm


def bmesh_to_object(obj, bm):
    """Object/Edit Mode update the object."""
    me = obj.data

    if obj.mode == 'EDIT':
        bmesh.update_edit_mesh(me, loop_triangles=True)
    else:
        bm.to_mesh(me)
        me.update()
