# ---------------------------- ПРОСТАЯ ПАНЕЛЬ ----------------------------
# Будет находится во Вьюпорте, в N панелях в категории My Panel. Внутри ее будет текст "Hello Blender!"
# Результат: https://github.com/sanya-2005/Blender-Code-Examples/blob/main/images/simple_panel.png

class MyPanel(bpy.types.Panel):
    # Как и у оператора, у панели должно быть свое имя. Желательно составлять имя по определенному правилу (а иначе блендер будет ругаться в консоль):
    # ИМЯПРОСТРАНСТВА_PT_СВОЙТЕКСТ
    bl_idname = 'VIEW3D_PT_My_panel'
    # То, что будет отображаться в заголовке панели
    bl_label = "My panel"    
    # Редактор, в котором будет отображаться панель, в нашем случае - Вьюпорт
    # Полный список можно найти на https://docs.blender.org/api/current/bpy.types.Panel.html
    bl_space_type = 'VIEW_3D'
    # Регион окна, в котором будет панель. Мы выбрали 'UI', во вьюпорте это N панели
    bl_region_type = 'UI'
    # Вкладка, в которой находится панель. Если указать несуществующую - то появится новая категория с этим именем
    bl_category = 'My Panel'

    # Функция отрисовки содержимого панели - самое главное
    def draw(self, context):
        self.layout.label(text="Hello Blender!")



# ---------------------------- ПРОСТОЕ МЕНЮ ----------------------------
# Как и панель, сначала необходимо зарегистрировать элемент. Однако от этого он не появится в UI, необходимо еще вызвать UILayout.menu() в нужном месте
# При отрисовке содержимого меню нам доступен весь функционал, что и при панелях/другом элементе, однако смысла от этого нету:
# То же создание двух операторов от одного row приведет к тому, что у меню поломается верстка
# Поэтому вместо создания промежуточных контейнеров работают напрямую с self.layout
# Меню в этом примере появится в заголовке Вьюпорта
# Результат: https://github.com/sanya-2005/Blender-Code-Examples/blob/main/images/simple_menu.png

class MyMenu(bpy.types.Menu):
    # Название меню
    bl_label = "My Menu"
    # имя для блендера
    bl_idname = "OBJECT_MT_my_menu"

    def draw(self, context):
        layout = self.layout

        layout.operator('object.align')
        layout.operator('object.join')
        layout.operator('object.convert')

        layout.separator()

        layout.operator('view3d.copybuffer')
        layout.operator('view3d.pastebuffer')

#..............

def draw(self, context):
    # Стоит обратить внимание на то, что меню по разному отображается в зависимости от того, где оно рисуется
    # На панели например оно будет отображаться как кнопка с выпадающим списком, а в меню секции вьюпорта - как обычное меню
    self.layout.menu(MyMenu.bl_idname)

bpy.types.VIEW3D_MT_editor_menus.append(draw)



# ---------------------------- РАБОТА С ОПЕРАТОРАМИ ----------------------------
# Операторы в UI отображаются в виде кнопок/пунктов меню. Есть пару интересных вещей, которые вам точно пригодятся

def draw(self, context):
    layout = self.layout

    # в UI появится кнопка, название которой - bl_label у оператора
    # Результат: https://github.com/sanya-2005/Blender-Code-Examples/blob/main/images/simple_operator.png
    layout.operator('object.add')

    # У UILayout.operator() много интересных аргументов. Например так можно сделать кнопку, у которой вместо названия будет иконка плюса
    # В качестве иконки надо указать текстовой ID иконки. Получить их можно через встроенный аддон Icon Viewer,
    # появится кнопка в Info и панель в тест едиторе
    # Результат: https://github.com/sanya-2005/Blender-Code-Examples/blob/main/images/operator_custom_icon.png
    layout.operator('object.add', text="", icon="ADD")

    # У многих операторов есть параметры. Если при вызове из кода их можно указывать как обычной функции, то в UI это делаетя через
    # operator().имя_параметра = значение
    # Результат аналогичен https://github.com/sanya-2005/Blender-Code-Examples/blob/main/images/operator_custom_icon.png. Рзаница в поведении
    layout.operator('object.add', text="", icon="ADD").type = "MESH"

    # Есть довольно интересные способы отображения операторов. operator_menu_enum() отображает оператор в виде меню, где
    # его элементы - значения для EnumProperty
    # вторым аргументом после оператора надо указать имя свойства - перечисления, элементы которого будет представлять меню
    # Результат: https://github.com/sanya-2005/Blender-Code-Examples/blob/main/images/operator_menu_enum.png
    layout.operator_menu_enum('object.convert', 'target')

    # Похожий на operator_menu_enum() метод - operator_enum(). Тоже самое, но operator_enum() 
    # Не создает отдельную подменюшку, а просто располагает все значения перечисления как отдельные элементы меню
    # Результат: https://github.com/sanya-2005/Blender-Code-Examples/blob/main/images/operator_enum.png
    layout.operator_enum('object.convert', 'target')



# ---------------------------- РАБОТА СО СВОЙСТВАМИ ----------------------------
# В UI также можно отображать свойства чего-либо (bpy.props). То, как рисуется свойство - зависит от его настроек

def draw(self, context):
    layout = self.layout

    # Сначала пишем то, с чего берем свойство, потом путь к свойству. Стоит заметить, что блендер не распознает в пути вложенность
    # Т.Е. путь - это по сути только название свойства
    # Например на prop(context.scene, "cycles.preview_samples") выдаст оишбку, но не на prop(context.scene.cycles, "preview_samples")
    # Результат: https://github.com/sanya-2005/Blender-Code-Examples/blob/main/images/prop.png
    layout.prop(context.object, "mode")

    # Некоторые свойства представлены массивами (например слои арматуры). Если прописать просто prop(armature, "layers")
    # То оно создает виджет со всеми слоями. Но вам например для рига надо получить доступ к конкретному слою
    # Это можно сделать, указав index. Стоит заметить, что правило нумерации массивов с 0 тут работает,
    # Первый элемент - это 0, второй - это 1, и т.п. Просто нумерация идет с нуля
    # Результат: https://github.com/sanya-2005/Blender-Code-Examples/blob/main/images/prop_array.png
    layout.prop(context.object.data, "layers", index = 0, text = "Layer 1", toggle = True)






