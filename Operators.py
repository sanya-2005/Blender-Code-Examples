# ---------------------------- ПРОСТОЙ ОПЕРАТОР ----------------------------
# просто выполняется. Можно вызвать в коде, забиндить на хоткей, либо вынести как кнопку в меню/панель/везде, где можно работать с UI

class MyOperator(bpy.types.Operator):
    # обязательное поле. Это имя оператора, по которому к нему будут обращаться. Сначала имя подпространства в bpy.ops, к которому принадлежит оператор
    # Если ввести существующее подпространство, то оператор будет включен в него. Т.е. введи object.my_operator, и он будет доступен через bpy.ops.object
    # Если же имя несуществующее, то подпространство будет создано, как у меня в примере. Перед запуском скрипта ops.test не будет существовать,
    # но после него появится
    # После подпространства идет имя оператора. Оно может быть любое, но лучше сохранять стиль блендера (без заглавных букв, нижние прочерки между словами)
    bl_idname = "test.my_operator"

    # Тоже обязательное поле. Имя оператора в UI
    bl_label = "My Operator"

    # Необязательное поле. Описание оператора, которое появляется в всплывающей подсказке
    bl_description = "My Operator description"

    # Необязательное поле, если вам не надо, чтоб оператор мог отменяться и имел редо панель :^)
    # Принимает словарь с определенными строками. Чаще всего используют:
    # 'UNDO' - оператор может отменяться и имеет редо панель
    # 'REGISTER' - не известно зачем, но по дефолту стоит ¯\_(ツ)_/¯
    # Остальные нужны для тонкой настройки, например, когда оператор модальный, как я понял
    # можно почитать тут https://docs.blender.org/api/current/bpy_types_enum_items/operator_type_flag_items.html#rna-enum-operator-type-flag-items
    bl_options = {'UNDO', 'REGISTER'}

    # Тут то и происходит вся магия. Этот метод выполняется при запуске оператора
    def execute(self, context):
        # теперь может быть любой код, мы будем просто выводить активный объект в консоль
        print(context.active_object)

        # Оператор обязательно должен возвращать словарь с одной-единственной определенной строкой
        # Так блендер понимает, что все ок, или все пошло по одному месту. Можно отправить:
        # 'FINISHED' - все хорошо
        # 'CANCELLED' - оператор остановлен по какой-то причине
        # Остальное используется в специфичных случаях, можно прочитать на https://docs.blender.org/api/current/bpy.ops.html#calling-operators
        return {'FINISHED'}



# ---------------------------- ОПЕРАТОР С АРГУМЕНТАМИ ----------------------------
# В оператор можно передать аргументы. Делается это через создание в классе поля с определенным типом из bpy.props, и потом получения значения через self
# Значения можно установить разными способами, мы поговорим мозже
# Один из способов - это через вызов из кода. у bpy.ops.<подпространство>.оператор появятся аргументы

class MyOperator(bpy.types.Operator):
    bl_idname = "test.my_operator"
    bl_label = "My Operator"
    bl_description = "My Operator description"
    bl_options = {'UNDO', 'REGISTER'}

    # Вот и свойство. У bpy.ops.test.my_operator() появится аргумент text_prop. Это текстовое свойство, оно хранит значение в виде строки
    text_prop:bpy.props.StringProperty(name="Text Prop", default="default")
    # Целочисленное свойство. Хранит число без чисел после запятой
    int_prop: bpy.props.IntProperty(name="Int Prop", default=1, subtype='FACTOR')

    # Свойств много, и у каждого много параметров. Например, subtype='FACTOR' заставит отображаться свойство в UI как слайдер 
    # Прочитать о всем можно на https://docs.blender.org/api/current/bpy.props.html

    def execute(self, context):

        # Доступ к свойствам осуществляется через self.имя_свойства
        print(self.text_prop)

        print(self.int_prop + 1)
        return {'FINISHED'}    



# ---------------------------- ОПЕРАТОР С ДИАЛОГОВЫМ ОКНОМ ----------------------------
# Перед запуском появится диалог, где можно указать значения свойствам оператора перед запуском
# После нажатия кнопки ОК или нажатия Enter оператор исполнится

class MyOperator(bpy.types.Operator):
    bl_idname = "test.my_operator"
    bl_label = "My Operator"
    bl_description = "My Operator description"
    bl_options = {'UNDO', 'REGISTER'}

    text_prop:bpy.props.StringProperty(name="Text Prop", default="default")
    int_prop: bpy.props.IntProperty(name="Int Prop", default=1, subtype='FACTOR')

    def execute(self, context):

        print(self.text_prop)
        print(self.int_prop + 1)

        return {'FINISHED'}    

    # Метод invoke запускается перед исполнением оператора, если у элемента GUI в operator_context указано определенное значение 
    # Вроде оно должно работать с дефолтным значением ('INVOKE_DEFAULT'), но мне пришлось переставить на 'INVOKE_AREA'
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
    # Если хочется зарядить в выскакивающий диалог что-то свое, то надо переопределть draw(self, context). Иначе просто будут свойства в стоблик
    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.label(text="Text Property")
        row.prop(self, "text_prop", text="")

        row - layout.row()
        row.label(text="Int Property")
        row.prop(self, "int_prop", text="")



# ---------------------------- ОПЕРАТОР С  ВЫПАДАЮЩИМ СПИСКОМ ----------------------------
# Если прикрепить к bpy.types.Menu, то появится пункт с выпадающим списком, где в качестве контента будут элементы bpy.props.EnumProperty
# После клика по элементу запустится оператор со значением свойства, по которому вы кликнули


