from .misc import correct_uv_button, texture_optimization
from . import mesh_panel

bl_info = {
    "name": "TimofeyToolbox",
    "author": "Deveone",
    "version": (1, 3, 3),
    "blender": (3, 5, 1),
    "location": "3D View > Sidebar",
    "category": "Mesh"
}


classes = [mesh_panel, correct_uv_button, texture_optimization]


### Mesh checks

from .mesh_checks import no_sg_faces, loose_verts_edges

classes.extend([no_sg_faces,
                loose_verts_edges])

### Mesh operations

from .mesh_operations import advanced_sg
from .mesh_operations import box_mapping
from .mesh_operations import fix_mat_names
from .rizom_uv import uv_renamer 

classes.extend([uv_renamer,
                fix_mat_names,
                box_mapping,
                advanced_sg])


def register():
    for c in classes:
        c.register()


def unregister():
    for c in classes:
        c.unregister()


if __name__ == '__main__':
    register()
