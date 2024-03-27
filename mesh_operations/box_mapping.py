import bpy
import math

# Global variables
HELPER_NAMES = [
    "UVW_Gizmo",
    "UVW_Top",
    "UVW_Bottom",
    "UVW_Front",
    "UVW_Back",
    "UVW_Left",
    "UVW_Right",
]

ROTATION_CONFIGS = [
    (0, 0, 0),  # TOP
    (math.pi, 0, 0),  # BOTTOM
    (math.pi / 2, 0, 0),  # FRONT
    (-math.pi / 2, 0, 0),  # BACK
    (-math.pi / 2, -math.pi, math.pi / 2),  # LEFT (TODO simplify and verify)
    (math.pi / 2, math.pi, math.pi / 2),  # RIGHT (TODO simplify and verify)
]

class TT_OT_box_mapping(bpy.types.Operator):
    bl_idname = "tt.box_mapping"
    bl_label = "Box Mapping"
    bl_description = "Apply box mapping (2x2x2) modifier with the box center at the origin"
    bl_options = {"UNDO"}

    def create_arrow(self, name, location, rotation_euler=(0, 0, 0)):
        bpy.ops.object.empty_add(type="SINGLE_ARROW", align="WORLD", location=location)
        arrow = bpy.context.object
        arrow.name = name
        arrow.rotation_euler = rotation_euler
        return arrow

    def create_gizmo(self):
        parent_cube = bpy.ops.object.empty_add(type="CUBE", align="WORLD", location=(0, 0, 0))
        parent_cube = bpy.context.object
        parent_cube.name = HELPER_NAMES[0]

        arrows = []
        for i, rotation in enumerate(ROTATION_CONFIGS):
            arrow = self.create_arrow(HELPER_NAMES[i + 1], (0, 0, 0), rotation)
            arrow.parent = parent_cube
            arrows.append(arrow)

        return parent_cube, arrows

    def execute(self, context):
        if context.object.mode != "OBJECT":
            bpy.ops.object.mode_set(mode="OBJECT")

        selected_objects = context.selected_objects
        if not selected_objects:
            self.report({'ERROR'}, "No selected objects")
            return {'CANCELLED'}

        # Find existing gizmo objects
        gizmo_objects = [bpy.data.objects.get(name) for name in HELPER_NAMES]
        created_gizmos = False
        if not all(gizmo_objects):
            # Create gizmo objects
            parent_cube, arrows = self.create_gizmo()
            created_gizmos = True
        else:
            parent_cube, arrows = gizmo_objects[0], gizmo_objects[1:]

        # Apply UV projection
        for obj in selected_objects:
            # Remove existing UV_PROJECT modifiers
            uv_modifiers = [mod for mod in obj.modifiers if mod.type == "UV_PROJECT"]
            for mod in uv_modifiers:
                obj.modifiers.remove(mod)

            # Add new UV_PROJECT modifier
            uv_project_modifier = obj.modifiers.new(name="UV Box Mapping 2x2x2", type="UV_PROJECT")
            uv_project_modifier.projector_count = 6
            for i, projector in enumerate(uv_project_modifier.projectors):
                obj.select_set(True)
                context.view_layer.objects.active = obj
                projector.object = arrows[i]

            # Apply modifier if needed
            if not context.scene.tt_keep_as_modifier:
                bpy.ops.object.modifier_apply(modifier=uv_project_modifier.name)

        # Clean up if not keeping as modifier and gizmos were created by the script
        if not context.scene.tt_keep_as_modifier and created_gizmos:
            bpy.data.objects.remove(parent_cube, do_unlink=True)
            for arrow in arrows:
                bpy.data.objects.remove(arrow, do_unlink=True)

        return {'FINISHED'}

classes = (TT_OT_box_mapping,)


register, unregister = bpy.utils.register_classes_factory(classes)