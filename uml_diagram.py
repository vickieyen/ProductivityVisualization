import plantuml

f = None

def replace_in_file(output_file, to_be_replaced, replace_with):
    s = open(output_file).read()
    s = s.replace(to_be_replaced, replace_with)
    f = open(output_file, 'w')
    f.write(s)
    f.close()

def add_class_dependencies(c):
    if c.extends != None:
        f.write(c.extends + " <|-- " + c.name + "\n")
    if c.implements != None:
        f.write(c.extends + " <|.. " + c.name + "\n")
    for d in c.dependencies:
        f.write(d + " <-- " + c.name + "\n")

def add_class_methods(methods):
    for method in methods:
        if len(method.params) == 0:
            f.write(method.name + "()\n")
        else:
            input_params = ''
            for param in method.params:
                input_params += param['type'] + " " + param['name']  + ", "
            input_params = input_params[:-2]
            f.write(method.name + "(" + input_params + ")\n")

def add_class_fields(fields):
    for field in fields:
        f.write(field.access + " " + field.var_type + " " + field.name + "\n")

def add_class_to_uml(c):
    f.write("class " + c.name + " {\n")
    add_class_fields(c.fields)
    add_class_methods(c.methods)
    f.write("}\n\n")
    add_class_dependencies(c)

def generate_uml(classes_found, output_file):
    global f
    f = open(output_file,"w+")
    f.write("@startuml\n")

    for class_found in classes_found:
        add_class_to_uml(class_found)

    f.write("@enduml")
    f.close()

    # modify public, private, protected symbols
    replace_in_file(output_file, "private", "-");
    replace_in_file(output_file, "protected", "#");
    replace_in_file(output_file, "public", "~");


plantuml = plantuml.PlantUML("http://www.plantuml.com/plantuml/img/")
plantuml.processes_file("./uml_output.txt", "./uml_diagram.png")