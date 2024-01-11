import bpy


class TEXTURE_PT_LimitSizePanel(bpy.types.Panel):
    bl_label = "Scene Optimization"
    bl_idname = "OBJECT_PT_mesh_scene_optimization_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {"HEADER_LAYOUT_EXPAND"}
    bl_category = "TimofeyToolbox"

    def draw(self, context):
        layout = self.layout
        prefs = context.preferences
        system = prefs.system

        col = layout.column()
        col.prop(system, "gl_texture_limit", text="Limit Size")
        col.prop(system, "anisotropic_filter")


def register():
    bpy.utils.register_class(TEXTURE_PT_LimitSizePanel)


def unregister():
    bpy.utils.unregister_class(TEXTURE_PT_LimitSizePanel)
