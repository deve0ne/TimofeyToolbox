import bpy
import bmesh


class TT_OT_advanced_subdivide(bpy.types.Operator):
    bl_idname = "tt.advanced_subdivide"
    bl_label = "Advanced Subdivide"
    name: bpy.props.StringProperty()

    def execute(self, context):
        # Ensure we're in edit mode
        if context.mode != 'EDIT_MESH':
            return "CANCELLED"

        # Get the active mesh
        obj = bpy.context.edit_object
        me = obj.data

        # Get a BMesh representation
        bm = bmesh.from_edit_mesh(me)

        # Check if the active selection is an edge or vertices
        active_selection = bm.select_history
        if isinstance(active_selection.active, bmesh.types.BMEdge):
            # Subdivide the edge
            edge = active_selection.active
        if isinstance(active_selection.active, bmesh.types.BMVert):
            # Subdivide the vertices
            selected_verts = [v for v in bm.verts if v.select]
            print(len(selected_verts))
            edge = bm.edges.get(selected_verts)

        bmesh.ops.subdivide_edges(bm, edges=[edge], cuts=1)

        # Deselect all vertices
        for v in bm.verts:
            v.select = False

        bm.verts.ensure_lookup_table()

        # Select the newly created vertex (it should be the last one)
        bm.verts[-1].select = True
        bm.select_history.add(bm.verts[-1])

        # Update the mesh
        bmesh.update_edit_mesh(me)

        return {'FINISHED'}


def register():
    bpy.utils.register_class(TT_OT_advanced_subdivide)


def unregister():
    bpy.utils.unregister_class(TT_OT_advanced_subdivide)
