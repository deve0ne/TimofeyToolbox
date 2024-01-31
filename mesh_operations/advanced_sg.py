import bpy
import bmesh
from math import radians
from ..helpers import mesh_helpers, popup


class TT_OT_advanced_sg_init(bpy.types.Operator):
    bl_idname = "tt.advanced_init_smooth_groups"
    bl_label = "Advanced Recalculate SG"
    bl_description = "Recalculates Smoothing Groups from Hard Edges and fixes normal bugs"
    bl_options = {"UNDO"}

    def execute(self, context):
        bpy.ops.dt.init_smooth_group()  # init default sg algorithm

        obj = context.object
        bm = mesh_helpers.bmesh_from_object(context.object)
        bm.faces.ensure_lookup_table()

        self.fix_sg(bm)

        mesh_helpers.bmesh_to_object(obj, bm)
        bm.free()

        return {"FINISHED"}

    def fix_sg(self, bm):
        iterations = 0

        sg_layer = bm.faces.layers.int.get("SG")

        while True:
            sg_bug = self.find_one_sg_bug(bm, sg_layer)

            # None means there is no bugs in mesh anymore
            if sg_bug is None:
                break

            sg_bug_island = self.expand_sg_bug_poly(bm, sg_bug[0], sg_layer)

            free_sg = self.find_free_sg(bm, sg_bug_island)

            self.reassign_island_sg(bm, sg_bug_island, free_sg)

            iterations += 1
            if iterations > 1000:  # Infinite loop protection
                popup.show_popup(icon="ERROR",
                                 title="Aborting: Too much bugs",
                                 message="Too large mesh or infinite loop")
                break

    def find_one_sg_bug(self, bm, sg_layer):
        sg_dict = {}

        for face in bm.faces:
            sg = face[sg_layer]
            if sg in sg_dict:
                sg_dict[sg].append(face)
            else:
                sg_dict[sg] = [face]

        def dfs(face, visited):
            visited.add(face)
            group = [face]
            for edge in face.edges:
                for link_face in edge.link_faces:
                    if link_face not in visited and link_face[sg_layer] == face[sg_layer]:
                        group.extend(dfs(link_face, visited))
            return group

        # Проходим по всем группам сглаживания и проверяем на наличие багов
        for sg, faces in sg_dict.items():
            visited = set()
            for face in faces:
                if face not in visited:
                    # Находим группу полигонов, связанных общими гранями
                    group = dfs(face, visited)

                    # Проверяем, есть ли другие группы, которые связаны с этой группой только через общую вершину
                    for face in group:
                        for vert in face.verts:
                            for link_face in vert.link_faces:
                                if link_face not in group and link_face[sg_layer] == face[sg_layer]:
                                    return [face.index, link_face.index]

        return None

    def expand_sg_bug_poly(self, bm, sg_bug_index, sg_layer):
        sg_bug_face = bm.faces[sg_bug_index]

        sg_bug_island = set()
        sg_bug_island.add(sg_bug_index)

        queue = [sg_bug_face]

        while queue:
            current_face = queue.pop(0)
            for edge in current_face.edges:
                for face in edge.link_faces:
                    if face.index not in sg_bug_island and face[sg_layer] == sg_bug_face[sg_layer]:
                        sg_bug_island.add(face.index)
                        queue.append(face)

        return sg_bug_island

    def find_free_sg(self, bm, sg_bug_island):
        sg_layer = bm.faces.layers.int.get("SG")

        pressed = set()
        neigbour_faces = set()
        for face in sg_bug_island:
            for vert in bm.faces[face].verts:
                for face in vert.link_faces:
                    neigbour_faces.add(face)

        for face in neigbour_faces:
            pressed.add(face[sg_layer])

        for i in [2**x for x in range(0, 32)]:
            if i not in pressed:
                if i == 2**31:  # костыль, чтобы не добавлять конвертацию в uint
                    return -2147483648
                return i
        return -1

    def reassign_island_sg(self, bm, sg_bug_island, sg_to_reassign):
        SG = bm.faces.layers.int.get("SG")

        for face in sg_bug_island:
            bm.faces[face][SG] = sg_to_reassign

        bm.faces.ensure_lookup_table()


bpy.types.Scene.tt_sg_angle = bpy.props.FloatProperty(
    name="SG Angle",
    description="Angle threshold for setting hard edges",
    subtype='ANGLE',
    default=radians(45),
    min=0.0,
    max=radians(180),
    step=100,
)


class TT_OT_auto_sg_by_angle(bpy.types.Operator):
    bl_idname = "tt.auto_sg_by_angle"
    bl_label = "Auto SG"
    bl_description = "Automatically set smooth groups based on angle"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        angle_radians = context.scene.tt_sg_angle
        
        for obj in context.selected_objects:
            bm = mesh_helpers.bmesh_from_object(obj)
            bm.edges.ensure_lookup_table()

            # recalculating hard edges
            for edge in bm.edges:
                if edge.is_manifold:
                    angle = edge.calc_face_angle_signed()
                    edge.smooth = abs(angle) <= angle_radians

            mesh_helpers.bmesh_to_object(obj, bm)

            # recalculating SG's
            bpy.ops.tt.advanced_init_smooth_groups()

        return {'FINISHED'}


class TT_PT_advanced_sg(bpy.types.Panel):
    bl_label = "Timofey Toolbox SG"
    bl_idname = "TT_PT_TT_SG_panel"
    bl_region_type = "UI"
    bl_space_type = "VIEW_3D"
    bl_category = "Dagor"

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)

        col.operator("tt.advanced_init_smooth_groups")

        row = col.row(align=True)
        row.operator("tt.auto_sg_by_angle", text="Auto SG")
        row.prop(context.scene, "tt_sg_angle", text="")

    @classmethod
    def poll(cls, context):
        return context.mode == "EDIT_MESH"


classes = (TT_OT_advanced_sg_init, TT_PT_advanced_sg, TT_OT_auto_sg_by_angle,)

register, unregister = bpy.utils.register_classes_factory(classes)