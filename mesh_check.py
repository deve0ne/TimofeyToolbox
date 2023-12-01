import bpy
import bmesh


class OBJECT_OT_FindNoSGfaces(bpy.types.Operator):
    bl_idname = "object.find_no_sg_faces"
    bl_label = "Check Smoothing groups"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        original_mode = bpy.context.object.mode
        bpy.ops.object.mode_set(mode="OBJECT")

        obj = context.active_object
        mesh = obj.data

        if not obj or obj.type != "MESH":
            self.report({"WARNING"}, "Active object is not a mesh")
            return {"CANCELLED"}

        if "SG" in mesh.attributes:
            attr = mesh.attributes["SG"].data
            no_sg_faces = [index for index, face in enumerate(attr) if face.value == 0]

            obj["no_sg_faces"] = no_sg_faces

        if original_mode == "EDIT":
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.object.select_no_sg_faces()

        return {"FINISHED"}


class OBJECT_OT_SelectNoSGfaces(bpy.types.Operator):
    bl_idname = "object.select_no_sg_faces"
    bl_label = "Select Faces with No Smooth Group"

    def execute(self, context):
        obj = context.active_object

        if not obj or obj.type != "MESH" or "no_sg_faces" not in obj:
            self.report(
                {"WARNING"}, "No faces to select or active object is not a mesh"
            )
            return {"CANCELLED"}

        bpy.ops.object.mode_set(mode="EDIT")

        mesh = bmesh.from_edit_mesh(obj.data)
        mesh.faces.ensure_lookup_table()

        for index in obj["no_sg_faces"]:
            if index < len(mesh.faces):
                mesh.faces[index].select_set(True)

        bmesh.update_edit_mesh(obj.data)
        return {"FINISHED"}


class OBJECT_OT_FindLooseVertsEdges(bpy.types.Operator):
    bl_idname = "object.find_loose_verts_edges"
    bl_label = "Find Loose Vertices and Edges"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        obj = context.active_object

        if not obj or obj.type != "MESH":
            self.report({"WARNING"}, "Active object is not a mesh")
            return {"CANCELLED"}

        bpy.ops.object.mode_set(mode="OBJECT")

        mesh = bmesh.new()
        mesh.from_mesh(obj.data)

        # Finding loose vertices and edges
        loose_verts = [v.index for v in mesh.verts if not v.link_edges]
        loose_edges = [e.index for e in mesh.edges if not e.link_faces]

        # Storing the results in the object
        obj["loose_verts"] = loose_verts
        obj["loose_edges"] = loose_edges

        mesh.free()
        return {"FINISHED"}


class OBJECT_OT_SelectLooseVertsEdges(bpy.types.Operator):
    bl_idname = "object.select_loose_verts_edges"
    bl_label = "Select Loose Vertices and Edges"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        obj = context.active_object

        if not obj or obj.type != "MESH" or "loose_verts" not in obj or "loose_edges" not in obj:
            self.report({"WARNING"}, "No elements to select or active object is not a mesh")
            return {"CANCELLED"}

        bpy.ops.object.mode_set(mode="EDIT")

        bm = bmesh.from_edit_mesh(obj.data)
        bm.verts.ensure_lookup_table()
        bm.edges.ensure_lookup_table()

        # Select loose vertices
        for v_index in obj["loose_verts"]:
            if v_index < len(bm.verts):
                bm.verts[v_index].select_set(True)

        # Select loose edges
        for e_index in obj["loose_edges"]:
            if e_index < len(bm.edges):
                bm.edges[e_index].select_set(True)

        bmesh.update_edit_mesh(obj.data)
        return {"FINISHED"}



classes = (
    OBJECT_OT_FindNoSGfaces,
    OBJECT_OT_SelectNoSGfaces,
    OBJECT_OT_SelectLooseVertsEdges,
    OBJECT_OT_FindLooseVertsEdges,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
