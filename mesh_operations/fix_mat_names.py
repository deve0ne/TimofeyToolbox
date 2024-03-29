import bpy
import re
import os


class TT_OT_fix_mat_paths(bpy.types.Operator):
    bl_idname = "tt.fix_mat_paths"
    bl_label = "Fix Mat Path's"
    bl_description = "Remove weird postfixes from dagormat texture path's"
    bl_options = {'UNDO'}

    def execute(self, context):
        # mats=','.join([m.name for m in bpy.data.materials]) if pref.process_all else act_mat.name
        mats = ','.join([m.name for m in bpy.data.materials])
        names = mats.split(',')
        mats = [bpy.data.materials.get(n) for n in names]

        if mats == '':
            return {'CANCELLED'}

        for mat in mats:
            T = mat.dagormat.textures
            for tex in T.keys():
                # no extention needed
                tex_name = re.sub('[%#$@!^&*]', '', T[tex])

                if T[tex] == '':
                    continue
                elif os.path.exists(T[tex]):
                    continue

                img = bpy.data.images.get(tex_name)

                if img is None:
                    continue

                if os.path.exists(img.filepath):
                    T[tex] = img.filepath

                T[tex] = tex_name

        return {'FINISHED'}


classes = (TT_OT_fix_mat_paths,)


register, unregister = bpy.utils.register_classes_factory(classes)
