import bpy

def draw_correct_UV_button(self, context):
    if context.mode == 'EDIT_MESH':
        self.layout.prop(context.scene.tool_settings, 'use_transform_correct_face_attributes', text='Correct UV', icon='UV_DATA')

def register():
    bpy.types.VIEW3D_HT_tool_header.append(draw_correct_UV_button)

def unregister():
    bpy.types.VIEW3D_HT_tool_header.remove(draw_correct_UV_button)

if __name__ == "__main__":
    register()