import bpy
import bmesh
from bpy.types import Operator
from bpy.props import IntProperty
from . import mesh_helpers

from . import report


class TT_OT_select_report(Operator):
    bl_idname = "tt.select_report"
    bl_label = "Select Report"
    bl_description = "Select the data associated with this report"
    bl_options = {'INTERNAL'}

    index: IntProperty()

    _type_to_mode = {
        bmesh.types.BMVert: 'VERT',
        bmesh.types.BMEdge: 'EDGE',
        bmesh.types.BMFace: 'FACE',
    }

    _type_to_attr = {
        bmesh.types.BMVert: "verts",
        bmesh.types.BMEdge: "edges",
        bmesh.types.BMFace: "faces",
    }

    def execute(self, context):
        info = report.info()
        name, _text, data = info[self.index]
        obj = bpy.data.objects[name]

        # TODO refactor
        # Unhide the object if it is hidden
        if obj.hide_viewport:
            obj.hide_viewport = False

        # We need to ensure the object is in the current view layer and visible
        if obj.name not in context.view_layer.objects:
            # Ensure the object is in the current view layer
            return {'CANCELLED'}

        # Make sure the object is also visible for rendering in the current view layer
        # Equivalent to obj.hide_viewport = False for the view layer
        obj.hide_set(False)

        # Operation on the object
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        context.view_layer.objects.active = obj

        bpy.ops.object.mode_set(mode='EDIT')

        bm_type, bm_array = data

        # Define the mesh selection mode based on bm_type
        bm_select_mode = self._type_to_mode[bm_type]
        bpy.ops.mesh.select_mode(type=bm_select_mode)

        # Create a bmesh from the active mesh
        bm = mesh_helpers.bmesh_from_object(obj)

        # TODO Not sure why it doesn't work without it
        bm.faces.ensure_lookup_table()
        bm.edges.ensure_lookup_table()
        bm.verts.ensure_lookup_table()

        # Clear existing selection and select based on the bm_array
        bpy.ops.mesh.reveal()
        bpy.ops.mesh.select_all(action='DESELECT')

        elems = getattr(bm, TT_OT_select_report._type_to_attr[bm_type])[:]

        # Select the elements
        try:
            for i in bm_array:
                elems[i].select_set(True)
        except IndexError:
            self.report({'WARNING'}, "Report is out of date, re-run check")

        # Update the mesh from the bmesh edit
        mesh_helpers.bmesh_to_object(obj, bm)
        bm.free()

        return {'FINISHED'}
