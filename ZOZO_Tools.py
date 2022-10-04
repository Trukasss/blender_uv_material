import bpy

bl_info = {
    "name": "ZOZO Tools",
    "author": "Lukas",
    "version": (0, 5),
    "blender": (2, 80, 0),
    "category": "Material",
}



MATERIAL_NAME = "UV_checkboard"



class ZOZO_OT_AddChecker(bpy.types.Operator):
    bl_idname = "uv.add_uv_checker"
    bl_label = "add_uv_checker"
    bl_description = "Ajouter un matériel checkboard aux objets séléctionnés"

    def create_material(self):
        material = bpy.data.materials.new(MATERIAL_NAME)
        material.use_nodes = True
        tree = material.node_tree
        for node in tree.nodes:
            tree.nodes.remove(node)
        n_checker = tree.nodes.new("ShaderNodeTexChecker")
        n_output = tree.nodes.new("ShaderNodeOutputMaterial")
        n_output.location = (200, 0)
        tree.links.new(n_checker.outputs[0], n_output.inputs[0])
        return material

    def assign_material(self, obj, material):
        if not obj.material_slots:
            obj.data.materials.append(material)
        else:
            materials = [material] + [mat for mat in obj.data.materials if mat.name != MATERIAL_NAME]
            obj.data.materials.clear()
            for mat in materials:
                obj.data.materials.append(mat)

    def set_viewport_settings(self, context):
        viewport = None
        for area in context.screen.areas:
            if area.type == "VIEW_3D":
                for space in area.spaces:
                    if space.type == "VIEW_3D":
                        viewport = space
        if viewport:
            if viewport.shading.type not in ("MATERIAL", "RENDERED"):
                viewport.shading.type = "MATERIAL"

    def get_selected_mesh_objects(self, context):
        return [obj for obj in context.selected_objects if obj.type == "MESH"]

    def execute(self, context):
        material = bpy.data.materials.get(MATERIAL_NAME)
        if not material:
            material = self.create_material()
        objects = self.get_selected_mesh_objects(context)
        for obj in objects:
            self.assign_material(obj, material)
        self.set_viewport_settings(context)
        return {"FINISHED"}



class ZOZO_OT_RemoveChecker(bpy.types.Operator):
    bl_idname = "uv.remove_uv_checker"
    bl_label = "remove_uv_checker"
    bl_description = "Retirer le matériel checkboard des objets séléctionnés"

    def get_selected_mesh_objects(self, context):
        return [obj for obj in context.selected_objects if obj.type == "MESH"]
    
    def remove_material(self, obj):
        index = obj.data.materials.find(MATERIAL_NAME)
        if index == -1:
            return
        obj.data.materials.pop(index=index)

    def execute(self, context):
        objects = self.get_selected_mesh_objects(context)
        for obj in objects:
            self.remove_material(obj)
        return {"FINISHED"}



class ZOZO_PT_panel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "UV auto material"
    bl_idname = "UV_PT_material"
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "ZOZO"

    def draw(self, context):
        layout = self.layout

        col = layout.column()
        col.operator(
            "uv.add_uv_checker",
            text="Ajouter UV checker",
            icon="MATERIAL",
        )
        col.operator(
            "uv.remove_uv_checker",
            text="Retirer UV checker",
            icon="CANCEL",
        )



def register():
    bpy.utils.register_class(ZOZO_PT_panel)
    bpy.utils.register_class(ZOZO_OT_AddChecker)
    bpy.utils.register_class(ZOZO_OT_RemoveChecker)

def unregister():
    bpy.utils.unregister_class(ZOZO_PT_panel)
    bpy.utils.unregister_class(ZOZO_OT_AddChecker)
    bpy.utils.unregister_class(ZOZO_OT_RemoveChecker)

if __name__ == "__main__":
    register()