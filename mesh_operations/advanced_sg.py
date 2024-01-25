import bpy
import bmesh


class TT_OT_advanced_sg(bpy.types.Operator):
    bl_idname = "tt.advanced_init_smooth_groups"
    bl_label = "Advanced Recalculate SG"
    bl_description = "Recalculates Smoothing Groups from Hard Edges and fixes normal bugs"
    bl_options = {"UNDO"}
    
    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj is not None and obj.type == 'MESH' and (obj.mode in {'EDIT'})

    def execute(self, context):
        bpy.ops.dt.init_smooth_group()  # init default sg algorithm

        mesh = context.object.data
        bm = bmesh.from_edit_mesh(mesh)
        bm.faces.ensure_lookup_table()

        self.fix_sg(bm)

        bmesh.update_edit_mesh(mesh)
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
            if iterations > 1000:  # Защита от бесконечного цикла
                print("limited")
                break

    # Нейрокод
    def find_one_sg_bug(self, bm, sg_layer):
        # Словарь для группировки лиц по группам сглаживания
        sg_dict = {}

        # Проходим по всем лицам и группируем их по группам сглаживания
        for face in bm.faces:
            sg = face[sg_layer]
            if sg in sg_dict:
                sg_dict[sg].append(face)
            else:
                sg_dict[sg] = [face]

        # Функция для поиска в глубину
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

        # Use a queue to explore connected polygons
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
        # col.operator("tt.find_no_sg_faces")

    @classmethod
    def poll(cls, context):
        # Only allow in edit mode for a selected mesh.
        return context.mode == "EDIT_MESH"


classes = (TT_OT_advanced_sg, TT_PT_advanced_sg)


register, unregister = bpy.utils.register_classes_factory(classes)
