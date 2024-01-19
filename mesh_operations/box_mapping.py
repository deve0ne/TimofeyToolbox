import bpy
import math


class TT_OT_box_mapping(bpy.types.Operator):
    bl_idname = "tt.box_mapping"
    bl_label = "BoxMapping"

    created_objects = []

    def create_arrow(self, name, location, rotation_euler=(0, 0, 0)):
        bpy.ops.object.empty_add(
            type="SINGLE_ARROW", align="WORLD", location=location, scale=(1, 1, 1)
        )

        new_arrow = bpy.context.object
        new_arrow.name = name
        new_arrow.rotation_euler = rotation_euler

        self.created_objects.append(new_arrow)

        rotation_angles = {
            "UVW_Left": -90,
            "UVW_Right": 90,
            "UVW_Back": 180,
            "UVW_Bottom": 180,
        }

        if name in rotation_angles:
            new_arrow.rotation_euler.rotate_axis(
                "Z", math.radians(rotation_angles[name])
            )

        return new_arrow

    def create_gizmo(self, helper_names):
        rotation_configs = [
            (0, 0, 0),  # TOP
            (1.5708 * 2, 0, 0),  # BOTTOM
            (1.5708, 0, 0),  # FRONT
            (-1.5708, 0, 0),  # BACK
            (0, -1.5708, 0),  # LEFT
            (0, 1.5708, 0),  # RIGHT
        ]

        for i in range(0, 6):
            self.create_arrow(
                helper_names[i + 1], (0, 0, 0), rotation_configs[i])

        bpy.ops.object.empty_add(
            type="CUBE", align="WORLD", location=(0, 0, 0), scale=(1, 1, 1)
        )

        bpy.context.object.name = helper_names[0]
        parent_cube = bpy.context.object

        for obj in self.created_objects:
            obj.parent = parent_cube

    def execute(self, context):
        self.created_objects = []

        if bpy.context.selected_objects:
            user_selected_objects = bpy.context.selected_objects
        else:
            print("No objects are currently selected.")
            return {"FINISHED"}

        helper_names = [
            "UVW_Gizmo",
            "UVW_Top",
            "UVW_Bottom",
            "UVW_Front",
            "UVW_Back",
            "UVW_Left",
            "UVW_Right",
        ]

        finded_objects = []
        for name in helper_names:
            obj = bpy.data.objects.get(name)
            if obj:
                finded_objects.append(obj)

        if len(finded_objects) == 7:
            self.created_objects = finded_objects[-6:]
        else:
            if len(finded_objects) != 0:
                for obj in finded_objects:
                    bpy.data.objects.remove(obj)

            self.create_gizmo(helper_names)

        for obj in user_selected_objects:
            modifiers_to_remove = [
                modifier for modifier in obj.modifiers if modifier.type == "UV_PROJECT"
            ]

            for modifier in modifiers_to_remove:
                obj.modifiers.remove(modifier)

            uv_project_modifier = obj.modifiers.new(
                "UV Box Mapping 2x2x2", "UV_PROJECT"
            )
            uv_project_modifier.projector_count = 6

            for i in range(6):
                uv_project_modifier.projectors[i].object = self.created_objects[i]

        bpy.ops.object.select_all(action="DESELECT")
        for obj in user_selected_objects:
            obj.select_set(True)

        return {"FINISHED"}


classes = [TT_OT_box_mapping]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
