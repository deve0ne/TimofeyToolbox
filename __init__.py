from .rizom_uv import uv_renamer
from . import preferences_panel
from . import addon_updater_ops
from .misc import correct_uv_button, texture_optimization, visibility_cls

bl_info = {
    "name": "TimofeyToolbox",
    "author": "Deveone",
    "version": (1, 4, 8),
    "blender": (3, 5, 1),
    "location": "3D View > Sidebar",
    "wiki_url": "https://github.com/deve0ne/TimofeyToolbox",
    "category": "Mesh"
}


classes = []


# Mesh checks

from .mesh_checks.checkers import (incorrect_geometry,
                                   loose_verts_edges,
                                   no_sg_faces,
                                   degenerates,
                                   manifold,
                                   check_all)
from .mesh_checks import (mesh_check_panel,
                          bounding_box_mode)

classes.extend([no_sg_faces,
                loose_verts_edges,
                incorrect_geometry,
                degenerates,
                manifold,
                check_all,
                bounding_box_mode,
                mesh_check_panel])

# Mesh operations

from .mesh_operations import (fix_mat_names,
                              box_mapping,
                              advanced_sg,
                              dissolve_degenerates,
                              mesh_operation_panel)

classes.extend([uv_renamer,
                fix_mat_names,
                box_mapping,
                dissolve_degenerates,
                advanced_sg,
                mesh_operation_panel])

# Misc

classes.extend([preferences_panel,
                correct_uv_button,
                texture_optimization,
                visibility_cls])


def register():
    addon_updater_ops.register(bl_info)

    for c in classes:
        c.register()


def unregister():
    addon_updater_ops.unregister()

    for c in reversed(classes):
        c.unregister()


if __name__ == '__main__':
    register()
