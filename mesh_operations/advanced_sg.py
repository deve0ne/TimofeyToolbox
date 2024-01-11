import bpy
import bmesh


class AdvancedSG(bpy.types.Operator):
    bl_idname = "mesh.advanced_init_smooth_groups"
    bl_label = "Advanced Recalculate SG"
    bl_description = "Initialize smoothing groups"
    bl_options = {"UNDO"}

    def execute(self, context):
        bpy.ops.dt.init_smooth_group()  # init default sg algorithm

        mesh = context.object.data
        self.fix_sg(mesh)

        return {"FINISHED"}

    def fix_sg(self, mesh):
        i = 0

        while True:
            sg_bug = self.find_one_sg_bug(mesh)

            print(sg_bug)

            if sg_bug is None:
                break

            sg_bug_island = self.expand_sg_bug_poly(mesh, sg_bug[0])
            print(sg_bug_island)
            self.select_faces(mesh, sg_bug_island)
            free_sg = self.find_free_sg(mesh)
            print(free_sg)
            self.reassign_island_sg(mesh, sg_bug_island, free_sg)

            i += 1
            if i > 100:
                break

    # DEBUG
    def select_faces(self, mesh, faces):
        bm = bmesh.from_edit_mesh(mesh)
        bm.faces.ensure_lookup_table()
        for face in faces:
            bm.faces[face].select = True

        # Show the updates in the viewport
        bmesh.update_edit_mesh(mesh)

    def find_one_sg_bug(self, mesh):
        bm = bmesh.from_edit_mesh(mesh)
        bm.faces.ensure_lookup_table()
        sg_layer = bm.faces.layers.int.get("SG")

        for face in bm.faces:
            adj_faces_dict = {}

            for vert in face.verts:
                for link_face in vert.link_faces:
                    if link_face[sg_layer] != face[sg_layer]:
                        continue

                    if link_face.index in adj_faces_dict:
                        adj_faces_dict[link_face.index] = (
                            adj_faces_dict[link_face.index] + 1)
                    else:
                        adj_faces_dict[link_face.index] = 1

            sg_bug = {key: value for key,
                      value in adj_faces_dict.items() if value == 1}

            if len(sg_bug) > 0:
                return [face.index,  sg_bug.popitem()[0]]

        bm.free()

        return None

    def expand_sg_bug_poly(self, mesh, sg_bug_index):
        bm = bmesh.from_edit_mesh(mesh)
        bm.faces.ensure_lookup_table()

        sg_layer = bm.faces.layers.int.get("SG")

        sg_bug_face = bm.faces[sg_bug_index]

        sg_bug_island = set()
        sg_bug_island.add(sg_bug_index)

        # Use a queue to explore connected polygons
        queue = [sg_bug_face]

        while queue:
            current_face = queue.pop(0)
            # print(f"Current face: {current_face.index}")
            for edge in current_face.edges:
                for face in edge.link_faces:
                    # print(f"face: {face.index} sg: {face[sg_layer]} another face: {current_face.index} sg: {current_face[sg_layer]}")
                    if face.index not in sg_bug_island and face[sg_layer] == sg_bug_face[sg_layer]:
                        sg_bug_island.add(face.index)
                        queue.append(face)
                        # print(f"Adding face {face.index} to island")

        return sg_bug_island

    def find_free_sg(self, mesh):
        bm = bmesh.from_edit_mesh(mesh)
        bm.faces.ensure_lookup_table()

        sg_layer = bm.faces.layers.int.get("SG")

        pressed = set()
        for face in bm.faces:
            pressed.add(face[sg_layer])

        for i in [2**x for x in range(0, 32)]:
            if i not in pressed:
                return i

        return -1

    def reassign_island_sg(self, mesh, sg_bug_island, sg_to_reassign):
        bm = bmesh.from_edit_mesh(mesh)
        bm.faces.ensure_lookup_table()

        SG = bm.faces.layers.int.get("SG")

        for face in sg_bug_island:
            bm.faces[face][SG] = sg_to_reassign

        bm.faces.ensure_lookup_table()

        bmesh.update_edit_mesh(mesh)


class OBJECT_PT_MeshSGPanel(bpy.types.Panel):
    bl_label = "Timofey Toolbox SG"
    bl_idname = "OBJECT_PT_TT_SG_panel"
    bl_region_type = "UI"
    bl_space_type = "VIEW_3D"
    bl_category = "Dagor"

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.operator("mesh.advanced_init_smooth_groups", icon="UV_DATA")

    @classmethod
    def poll(cls, context):
        # Only allow in edit mode for a selected mesh.
        return context.mode == "EDIT_MESH"


classes = [AdvancedSG, OBJECT_PT_MeshSGPanel]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
