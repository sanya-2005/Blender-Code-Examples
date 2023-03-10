# ---------------------------- СВОЙСТВА ----------------------------
# Свойства - это обертка для различных типов данных, подобно как операторы для функций
# Их можно вешать так на операторы (как аргументы), так и на остальные блендеровские классы (Scene, Object, датаблоки, т.д.)
# Доступен не такй уж большой, но и не малофункциональный набор данных. Среди них Int, Float, String и т.д. 



# ---------------------------- ОПЕРАТОР С АРГУМЕНТАМИ ----------------------------
# См Operator.py



# ---------------------------- СВОЙСТВО НА ОБЪЕКТ ----------------------------
# Как уже говорилось, помимо операторов свойство можно повесить на объекты
# Для этого надо использовать опеделенный синтаксис

# Свойства присваются типам из bpy.types. Пишите класс.имя_свойства = bpy.props.свойство()
# На этом примере мы добавили сцене целочисленное свойство
# У свойство опять же куча параметров, name задает имя в UI, default - дефолтное значение, а вот subtype говорит, как будет отображаться виджет с доступом к свойству
# В нашем случае, если сделать layout.prop(scene, "my_prop"), то будет слайдер
# Результат: https://github.com/sanya-2005/Blender-Code-Examples/blob/main/images/int_prop.png

bpy.types.Scene.my_prop = bpy.props.IntProperty(name="My Prop", default = 2, subtype="FACTOR", min = 0, max = 100)



# ---------------------------- ENUM PROPERTY ----------------------------
# Это свойство, состоящее из перечисления, элементы которого - текст
# Самое сложное - это синтаксис, определяющий сами элементы перечисления. Это список, который содержит кортежи
# Кортежи и предоставляют описания элементов перечисления

# Как уже говорилось, список содержит кортежи, кортежи должны иметь строго определенную структуру
# ("ID", "ИМЯ", "ОПИСАНИЕ", "ИКОНКА", ID_ЧИСЛОМ)
# Два последних можно не писать, но если понадобится хоть один из них - придется указывать оба
prop_items = [("ONE", "One", "One number"),
              ("TWO", "Two", "Two number"),
              ("THREE", "Three", "Three number")            
            ]

# Значение свойства будет текстом, а точнее текстовым ID, которое указывали первым в кортеже
bpy.types.Object.my_enum_prop = bpy.props.EnumProperty(items=prop_items, name="My Enum Prop")



# ---------------------------- POINTER PROPERTY ----------------------------
# Весьма необычное для питона свойство. Это по сути сырой указатель из С++, который хранит в себе адрес в памяти каких-то данных
# Наш Pointer property может указывать лишь на наследников bpy.types.PropertyGroup(все свойства) и bpy.types.ID (все остальное)
# Где-то в документации было написано предостережение, что никакого отслеживания за тем, куда указывает Pointer Property не ведется
# Это значит, что если данные, на которые указывают - будут удалены, то может и вовсе случится вылет блендера

bpy.types.Object.p_prop = bpy.props.PointerProperty(type=bpy.types.Mesh, name="my pointer property")
# Присваиваем нашему указателю меш от второго объекта
bpy.data.objects['Cube'].p_prop = bpy.data.meshes['Cube.002']



# ---------------------------- PROPERTY GROUP ----------------------------
# Это базовый тип для свойств, на его основе можно сделать свое свойство
# Это можно использовать, например, если вам надо сгруппировать несколько свойств в одно
# А вот уже это придется сначала зарегистрировать перед использованием
# Т.е. сначала надо сделать bpy.utils.register_class(мой_класс), а только потом вешать куда-то его

class MyProp(bpy.types.PropertyGroup):
    int_prop:bpy.props.IntProperty(name="int")
    str_prop:bpy.props.StringProperty(name="str")

bpy.types.Object.my_prop = bpy.props.PointerProperty(type=MyProp, name="my prop")

bpy.context.object.my_prop.int_prop = 1
bpy.context.object.my_prop.str_prop = "LOL"