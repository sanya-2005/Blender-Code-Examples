# У каждого аддона должна быть переменная bl_info, где пишется описание аддона. ЧТо значат ключи внутри нее - можно легко догадаться
bl_info = {
    "name": "My Test Addon",
    "author": "You",
    "version": (1, 0),
    "blender": (3, 4, 0),
    "location": "3D View > Menus, 3D View > N Panels",
    "description": "",
    "warning": "",
    "doc_url": "",
    "category": "Other",
}

import bpy

class PrintSelectedObjects(bpy.types.Operator):
    bl_idname = "text.print_selected_objects"
    bl_label = "Print selected objects"
    bl_options = {'UNDO', 'REGISTER'}
    bl_description = "Print selected objets name in text datablock"

    @classmethod
    def poll(cls, context):
        return context.selected_objects is not None

    def execute(self, context):
        text_datablock = bpy.data.texts.new("selected_objects")

        for obj in context.selected_objects:
            text_datablock.write(obj.name)
            text_datablock.write('\n')

        return {'FINISHED'}

class MyPanel(bpy.types.Panel):
    bl_idname = "VIEW3D_PT_MyPanel"
    bl_label = "My Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "My Stuff"

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.label(text="My Panel!")

        row = layout.row()
        text_str = ""

        if context.active_object is None:
            text_str = "None"
        else:
            text_str = context.active_object.name

        row.label(text = "active object: " + text_str)

        row = layout.row()
        row.operator("wm.quit_blender", text="хватить сидеть в своем блендере!")

class MyMenu(bpy.types.Menu):
    bl_label = "My Menu"
    bl_idname = 'VIEW3D_MT_MyMenu'

    def draw(self, context):
        layout = self.layout

        layout.operator('transform.translate')
        layout.operator('transform.rotate')
        layout.operator('transform.resize')

        layout.separator()

        layout.operator('text.print_selected_objects', icon = "TEXT")

def my_draw(self, context):
    self.layout.menu(MyMenu.bl_idname)

# Стоит заметить, что если какой-то класс использует другой класс (например меню использует оператор), то сначала надо зарегистрировать используемый класс
# А потом использующий. По такому принципу надо строить порядок элементов в этом списке
classes = [
    PrintSelectedObjects,
    MyPanel,
    MyMenu
]

# Эти две функции обязательно должны присутствовать. Первая исполняется при включении аддона (и соответственно установке), а вторая при отключении
def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.VIEW3D_MT_editor_menus.append(my_draw)

def unregister():
    # разрегистрацию рекомендуется делать в обратном порядке, так как в таком случае сначала будет разрегистрировано UI, которое например использует оператор
    # А потом сам оператор
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    bpy.types.VIEW3D_MT_editor_menus.remove(my_draw)

