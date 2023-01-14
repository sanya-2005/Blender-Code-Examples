bl_info = {
    "name": "Script Library",
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

def print_selected_objects(context):
    for obj in context.selected_objects:
        print(obj)

class View3dPanel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

# register и unregister необходимы для регистрации аддона, так что оставим их пустыми

def register():
    pass

def unregister():
    pass