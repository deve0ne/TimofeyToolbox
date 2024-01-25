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
        
        #TODO   
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')
        
        
        
        bm_type, bm_array = data

        bpy.ops.mesh.select_mode(type=self._type_to_mode[bm_type])

        bm = mesh_helpers.bmesh_from_object(obj)
        bm.faces.ensure_lookup_table()

        # Clear existing selection
        bpy.ops.mesh.reveal()
        bpy.ops.mesh.select_all(action='DESELECT')

        # Select the elements
        for i in bm_array:
            try:
                bm.faces[i      ].select_set(True)
            except IndexError:
                self.report({'WARNING'}, "Report is out of date, re-run check")
                break

        mesh_helpers.bmesh_to_object(obj, bm)

        return {'FINISHED'}