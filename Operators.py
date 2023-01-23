# ---------------------------- ПРОСТОЙ ОПЕРАТОР ----------------------------
# просто выполняется. Можно вызвать в коде/через f3, забиндить на хоткей, либо вынести как кнопку в меню/панель/везде, где можно работать с UI

class MyOperator(bpy.types.Operator):
    # обязательное поле. Это имя оператора, по которому к нему будут обращаться. Сначала имя подпространства в bpy.ops, к которому принадлежит оператор
    # Если ввести существующее подпространство, то оператор будет включен в него. Т.е. введи object.my_operator, и он будет доступен через bpy.ops.object
    # Если же имя несуществующее, то подпространство будет создано, как у меня в примере. Перед запуском скрипта "ops.test" не будет существовать,
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



# ---------------------------- ОПЕРАТОР С УСЛОВИЕМ ЗАПУСКА ----------------------------
# Как известно, оператор работает с контекстом. Но контекст может оказаться невалидным. Например, активного объекта не будет
# Наш оператор в таком случае завершится с ошибкой. Чтобы не захламлять execute() кучей проверок, можно переопределить метод poll

class MyOperator(bpy.types.Operator):
    bl_idname = "test.my_operator"
    bl_label = "My Operator"
    bl_description = "My Operator description"
    bl_options = {'UNDO', 'REGISTER'}

    # Наверху всегда пишем декоратор @classmethod. poll возвращает булево значение, от его значения зависит, будет ли активен оператор
    # В нашем случае мы сделали проверку на то, является ли активный объект None (т.е. ничем ничего нету)
    # Если да - то возвращаем False, иначе - True. Самый простой способ проверить - удалить активный объект. В этом случае context.active_object = None
    # Оператор будем потемневшим, если вы вынесли его в UI, и не будет реагировать на нажатия, не будет искаться в f3 меню
    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):

        print(context.active_object)

        return {'FINISHED'}



# ---------------------------- ОПЕРАТОР С АРГУМЕНТАМИ ----------------------------
# В оператор можно передать аргументы. Делается это через создание в классе поля с определенным типом из bpy.props, и потом получения значения через self
# Значения можно установить разными способами. Один из них - через вызов из кода. у bpy.ops.<подпространство>.оператор появятся аргументы
# Результат: https://github.com/sanya-2005/Blender-Code-Examples/blob/main/images/operator_args.png

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



# ---------------------------- СООБЩЕНИЯ ПРИ ИСПОЛНЕНИИ ОПЕРАТОРА ----------------------------
# У некоторых операторов при выполнении выскакивает сообщение, либо у курсора, либо в нижней полосе
# Сделать его можно через Operator.report()
# Результат: https://github.com/sanya-2005/Blender-Code-Examples/blob/main/images/operator_msg.png

class MyOperator(bpy.types.Operator):
    bl_idname = "test.my_operator"
    bl_label = "My Operator"
    bl_description = "My Operator description"
    bl_options = {'UNDO', 'REGISTER'}

    def execute(self, context):

        if context.active_object is None:
            # В начале мы должны передать тип сообщения. Самые часто используемые - 'ERROR' и 'INFO', потом само сообщение
            # В зависимости от типа сообщения поведение немного отличается:
            # При 'ERROR' появится сообщение с заголовком "ошибка" прямо у курсора. При 'INFO' сообщение отправится в редактор Info, и в нижнюю полосуЫ
            self.report({'ERROR'}, "Active object is None!")
            return {'CANCELLED'}

        print(context.active_object)
        self.report({'INFO'}, "all is OK!")
  
        return {'FINISHED'}    



# ---------------------------- ОПЕРАТОР С ДИАЛОГОВЫМ ОКНОМ ПЕРЕД ЗАПУСКОМ ----------------------------
# Перед запуском появится диалог, где можно указать значения свойствам оператора перед запуском
# После нажатия кнопки ОК или нажатия Enter оператор исполнится
# Результат: https://github.com/sanya-2005/Blender-Code-Examples/blob/main/images/operator_invoke_dialog.png

class MyOperator(bpy.types.Operator):
    bl_idname = "test.my_operator"
    bl_label = "My Operator"
    bl_description = "My Operator description"
    bl_options = {'UNDO', 'REGISTER'}

    text_prop:bpy.props.StringProperty(name="Text Prop", default="default")
    int_prop: bpy.props.IntProperty(name="Int Prop", default=1, subtype='FACTOR', min = 0, max = 100)

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

        row = layout.row()
        row.label(text="Int Property")
        row.prop(self, "int_prop", text="")
