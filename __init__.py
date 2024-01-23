from .rizom_uv import uv_renamer
from . import preferences_panel
from . import addon_updater_ops
from .misc import correct_uv_button, texture_optimization
from .mesh_operations import fix_mat_names
from .mesh_operations import box_mapping
from .mesh_operations import advanced_sg
from .mesh_operations import mesh_operation_panel
from .mesh_checks.checkers import incorrect_geometry, loose_verts_edges, no_sg_faces, degenerates, manifold, check_all
from .mesh_checks import mesh_check_panel, bounding_box_mode
bl_info = {
    "name": "TimofeyToolbox",
    "author": "Deveone",
    "version": (1, 4, 6),
    "blender": (3, 5, 1),
    "location": "3D View > Sidebar",
    "wiki_url": "https://github.com/deve0ne/TimofeyToolbox",
    "category": "Mesh"
}


classes = []


# Mesh checks


classes.extend([mesh_check_panel,
                no_sg_faces,
                loose_verts_edges,
                incorrect_geometry,
                degenerates,
                manifold,
                check_all,
                bounding_box_mode])

# Mesh operations


classes.extend([mesh_operation_panel,
                uv_renamer,
                fix_mat_names,
                box_mapping,
                advanced_sg])


# Misc

classes.extend([preferences_panel,
                correct_uv_button,
                texture_optimization])


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
