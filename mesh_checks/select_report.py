import math

import bpy
from bpy.types import Operator
from bpy.props import (
    IntProperty,
    FloatProperty,
)
import bmesh

from bpy.app.translations import pgettext_tip as tip_

from . import report

class MESH_OT_print3d_select_report(Operator):
    bl_idname = "tt.select_report"
    bl_label = "3D-Print Select Report"
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
        obj = context.edit_object
        info = report.info()
        _text, data = info[self.index]
        bm_type, bm_array = data

        bpy.ops.mesh.reveal()
        bpy.ops.mesh.select_all(action='DESELECT')
        
        bpy.ops.mesh.select_mode(type=self._type_to_mode[bm_type])

        bm = bmesh.from_edit_mesh(obj.data)
        elems = getattr(bm, MESH_OT_print3d_select_report._type_to_attr[bm_type])[:]

        try:
            for i in bm_array:
                elems[i].select_set(True)
        except Exception as e: 
            # possible arrays are out of sync
            self.report({'WARNING'}, "Report is out of date, re-run check")

        return {'FINISHED'}