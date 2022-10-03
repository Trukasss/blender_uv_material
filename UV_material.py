import bpy


class HelloWorldPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "UV auto material"
    bl_idname = "UV_PT_material"
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout

        obj = context.object

        col = layout.column()
        col.label(text="Auto UV checker")
        col.operator(
            "uv.add_uv_material",
            text="Add UV checker Material",
            icon="MATERIAL",
        )
        

class AddUVMaterial(bpy.types.Operator):
    bl_idname = "uv.add_uv_material"
    bl_label = "add_uv_material"
    bl_description = "Ajouter un matériel checkboard"
    
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

    def assign_material(self, context, material):
        obj = context.active_object
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


    def execute(self, context):
        material = bpy.data.materials.get(self.material_name)
        if not material:
            material = self.create_material()
        self.assign_material(context, material)
        self.set_viewport_settings(context)
        return {"FINISHED"}

def register():
    bpy.utils.register_class(HelloWorldPanel)
    bpy.utils.register_class(AddUVMaterial)


def unregister():
    bpy.utils.unregister_class(HelloWorldPanel)
    bpy.utils.unregister_class(AddUVMaterial)
