bl_info = {
        "name": "TimofeyToolbox",
        "author": "Deveone",
        "version": (1, 3, 2),
        "blender": (3, 5, 1),
        "location": "3D View > Sidebar",
        "category": "Mesh"
        }

import bpy
from . import mesh_check
from . import mesh_operations
from . import mesh_panel

main_cl = [mesh_check, mesh_operations, mesh_panel]

def register():
    for c in main_cl:
        c.register()

def unregister():
    for c in main_cl:
        c.unregister()

if __name__ == '__main__':
    register()
