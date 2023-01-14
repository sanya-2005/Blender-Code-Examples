bl_info = {
    "name": "Script Library User",
    "author": "You",
    "version": (1, 0),
    "blender": (3, 4, 0),
    "location": "",
    "description": "",
    "warning": "",
    "doc_url": "",
    "category": "",
}

import bpy
import addon_library

class PrintSelectedObjects(bpy.types.Operator):
    bl_idname = "object.print_selected_objects"
    bl_label = "Print Selected Objects"
    bl_options = {"UNDO", "REGISTER"}

    def execute(self, context):
        addon_library.print_selected_objects(context)
        return {'FINISHED'}

class MyPanel(addon_library.View3dPanel):
    bl_idname = 'VIEW3D_PT_My_panel'
    bl_label = "My Panel"
    bl_category = "My Panel"

    def draw(self, context):
        layout = self.layout

        layout.label(text = "My Panel!")

classes = [PrintSelectedObjects, MyPanel]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    


