import bpy
import bmesh
from bpy.types import Operator
from bpy.props import IntProperty
from . import mesh_helpers

from . import report


import bpy
import bmesh
from bpy.types import Operator
from bpy.props import IntProperty

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
        name, _, data = info[self.index]
        
        if name not in bpy.data.objects:
            self.report({'WARNING'}, "Report is out of date, re-run check")
            return {'CANCELLED'}
        
        obj = bpy.data.objects[name]
        obj.hide_viewport = False

        if name not in context.view_layer.objects:
            return {'CANCELLED'}

        obj.hide_set(False)

        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')

        bm_type, bm_array = data
        bm_select_mode = self._type_to_mode[bm_type]
        bpy.ops.mesh.select_mode(type=bm_select_mode)

        bm = mesh_helpers.bmesh_from_object(obj)
        bm.select_mode = {bm_select_mode}   

        getattr(bm, self._type_to_attr[bm_type]).ensure_lookup_table()

        bpy.ops.mesh.reveal()
        bpy.ops.mesh.select_all(action='DESELECT')

        elems = getattr(bm, self._type_to_attr[bm_type])
        try:
            for i in bm_array:
                elems[i].select_set(True)
        except IndexError:
            self.report({'WARNING'}, "Report is out of date, re-run check")

        mesh_helpers.bmesh_to_object(obj, bm)
        return {'FINISHED'}