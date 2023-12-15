import bpy
import bmesh


class AdvancedSG(bpy.types.Operator):
    bl_idname = "mesh.advanced_init_smooth_groups"
    bl_label = "Advanced Recalculate SG"
    bl_description = "Initialize smoothing groups"
    bl_options = {"UNDO"}

    def execute(self, context):
        bpy.ops.dt.init_smooth_group()  # init default sg algorithm

        # bpy.ops.object.editmode_toggle()

        mesh = context.object.data
        self.fix_SG(mesh)

        bpy.ops.object.editmode_toggle()
        return {"FINISHED"}

    def fix_SG(self, mesh):
        # SG=mesh.attributes.get('SG') #SG is <bpy_struct, IntAttribute("SG") at 0x000001E1021F4A08> type

        sg_bug_poly = self.find_one_sg_bug(mesh)

        while sg_bug_poly is not None:
            # sg_bug_island = expand_sg_bug_poly(sg_bug_poly)

        #     sg_to_reassign = find_free_sg(mesh, sg_bug_island)
        #     reassign_island_sg(sg_bug_island)

        #     sg_bug_poly = find_one_sg_bug()

    def find_one_sg_bug(self, mesh):
        bm = bmesh.from_edit_mesh(mesh)
        for face in bm.faces:
            self.adj_faces_dict = {}

            for vert in face.verts:
                for link_face in vert.link_faces:
                    if link_face.index in self.adj_faces_dict:
                        self.adj_faces_dict[link_face.index] = (self.adj_faces_dict[link_face.index] + 1)
                    else:
                        self.adj_faces_dict[link_face.index] = 1
                        
            sg_bug = {key: value for key, value in self.adj_faces_dict.items() if value == 1}
            
            if len(sg_bug) > 0:
                return [face.index,  sg_bug.popitem()[0]]

    
        return None

    def expand_sg_bug_poly(mesh, sg_bug_poly):
        sg_bug_island = set()
        sg_bug_island.add(sg_bug_poly)
        # Use a queue to explore connected polygons
        queue = [sg_bug_poly]
        while queue:
            current_poly = queue.pop(0)
            for vertex in current_poly.vertices:
                for edge in mesh.edges:
                    if edge.vertices[0] == vertex or edge.vertices[1] == vertex:
                        other_poly = (
                            edge.polygons[1]
                            if edge.polygons[0] == current_poly
                            else edge.polygons[0]
                        )
                        if (
                            other_poly.use_smooth
                            and other_poly.attributes["SG"].value
                            == sg_bug_poly.attributes["SG"].value
                        ):
                            sg_bug_island.add(other_poly)
                            queue.append(other_poly)
        return sg_bug_island

    # def find_free_sg(mesh, sg_bug_island):

    # def reassign_island_sg(sg_bug_island, sg_to_reassign, ):
    #     for i in range(SG.data.__len__()):
    #         SG.data[i].value=fixed_SG[i] if mesh.polygons[i].use_smooth else 0


class OBJECT_PT_MeshOperationsPanel(bpy.types.Panel):
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
