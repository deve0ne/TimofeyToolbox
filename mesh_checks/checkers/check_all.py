from bpy.types import Operator
from bpy.utils import register_classes_factory
from .incorrect_geometry import TT_OT_find_incorrect_geometry
from .loose_verts_edges import TT_OT_find_loose_verts_edges
from .no_sg_faces import TT_OT_find_no_sg_faces
from .degenerates import TT_OT_find_degenerates
from .manifold import TT_OT_check_manifold
from ...helpers import report


class TT_Check_All(Operator):
    bl_idname = "tt.check_all"
    bl_label = "Check All"
    bl_description = "Run all mesh checks"

    check_cls = (
        TT_OT_find_no_sg_faces,
        TT_OT_find_loose_verts_edges,
        TT_OT_find_incorrect_geometry,
        TT_OT_find_degenerates,
        TT_OT_check_manifold
    )

    def execute(self, context):
        obj = context.active_object

        info = []
        for cls in self.check_cls:
            cls.main_check(obj, info)

        report.update(*info)

        return {'FINISHED'}


classes = (TT_Check_All,)

register, unregister = register_classes_factory(classes)