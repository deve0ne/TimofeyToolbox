from bpy.types import Operator
from bpy.utils import register_class, unregister_class
from .incorrect_geometry import OBJECT_OT_FindIncorrectGeometry
from .loose_verts_edges import OBJECT_OT_FindLooseVertsEdges
from .no_sg_faces import OBJECT_OT_FindNoSGfaces
from .. import report
from ..mesh_check_helpers import multiple_obj_warning

class TT_Check_all(Operator):
    bl_idname = "tt.check_all"
    bl_label = "TT Check All"
    bl_description = "Run all checks"

    check_cls = (
        OBJECT_OT_FindNoSGfaces,
        OBJECT_OT_FindLooseVertsEdges,
        OBJECT_OT_FindIncorrectGeometry
    )

    def execute(self, context):
        obj = context.active_object

        info = []
        for cls in self.check_cls:
            cls.main_check(obj, info)

        report.update(*info)

        multiple_obj_warning(self, context)

        return {'FINISHED'}
    
classes = [TT_Check_all]


def register():
    for cls in classes:
        register_class(cls)


def unregister():
    for cls in classes:
        unregister_class(cls)
