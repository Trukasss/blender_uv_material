import bpy

bl_info = {
    "name": "ZOZO Tools",
    "author": "Lukas",
    "version": (0, 5),
    "blender": (2, 80, 0),
    "category": "Material",
}

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
        

class ZOZO_OT_AddChecker(bpy.types.Operator):
    bl_idname = "uv.add_uv_checker"
    bl_label = "add_uv_checker"
    bl_description = "Ajouter un matériel checkboard aux objets séléctionnés"
    
    material_name = "UV_checkboard"

    def create_material(self):
        material = bpy.data.materials.new(self.material_name)
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
            obj.data.materials.append(None)
        obj.material_slots[0].material = material

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

    def get_mesh_objects(self, context):
        return [obj for obj in context.selected_objects if obj.type == "MESH"]

    def execute(self, context):
        material = bpy.data.materials.get(self.material_name)
        if not material:
            material = self.create_material()
        objects = self.get_mesh_objects(context)
        for obj in objects:
            self.assign_material(obj, material)
        self.set_viewport_settings(context)
        return {"FINISHED"}

def register():
    bpy.utils.register_class(ZOZO_PT_panel)
    bpy.utils.register_class(ZOZO_OT_AddChecker)


def unregister():
    bpy.utils.unregister_class(ZOZO_PT_panel)
    bpy.utils.unregister_class(ZOZO_OT_AddChecker)