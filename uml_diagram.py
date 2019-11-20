from github import Github
import base64
import plyj.parser as plyj
import plantuml
import os

# DO NOT PUSH TOKEN, DELETE BEFORE PUSHING
token = ""

g = Github(token)
repo = g.get_user().get_repo("ExamGenerator")

content_files = repo.get_contents("/src")
uml_output_txt_file_name = "uml_output.txt"

parser = plyj.Parser()
classes = []
filtered_content_files = []

def writeFields(dec):
    if hasattr(dec.type, "name"):
        var_type = dec.type.name.value
    else:
        var_type = dec.type
    f.write(var_type)
    if hasattr(dec.type, "type_arguments") and len(dec.type.type_arguments) > 0:
        f.write("<")
        args = dec.type.type_arguments
        for arg in args:
            f.write(arg.name.value + ", ")
        # remove comma and space if last arg
        f.seek(f.tell() - 2, os.SEEK_SET)
        f.write('')
        f.write(">")
    var_name = dec.variable_declarators[0].variable.name
    f.write(" " + var_name + "\n")

def add_class_dependency(class_name, file_str):
    print("Adding dependencies for " + class_name)

    # parse a compilation unit from a string
    tree = parser.parse_string(file_str)

    for td in tree.type_declarations:
        # add extends and implements arrows
        if td.extends != None and td.extends:
            extends_from = td.extends.name.value
            f.write(extends_from + " <|-- " + td.name + "\n")
        elif len(td.implements) > 0:
            for superclass in td.implements:
                class_implemented = superclass.name.value
                f.write(class_implemented + " <|.. " + td.name + "\n\n")

def parse_class(class_name, file_str):
    print("Adding class " + class_name)

    # parse a compilation unit from a string
    tree = parser.parse_string(file_str)

    # add class fields and methods to plant uml dsl
    for td in tree.type_declarations:
        body = td.body
        if 'abstract' in td.modifiers:
            f.write("abstract ")
        f.write("class " + td.name + " {\n")
        for dec in body:
            if hasattr(dec, "body") or hasattr(dec, "block"): # MethodDeclaration or ConstructorDeclaration
                method_name = dec.name
                f.write(dec.name + "()\n")
            else: # FieldDeclaration
                if hasattr(dec, "modifiers"):
                    for m in dec.modifiers:
                        f.write(m + " ")
                writeFields(dec)
    f.write("}\n\n")

def read_content_file(content_file):
    content = content_file.content
    decoded = base64.b64decode(content).decode("utf-8")
    return decoded

def traverse_content_files(content_files):
    # add classes to dsl
    for content_file in content_files:
        name = content_file.name.split('.')
        if content_file.type == "dir":
            traverse_content_files(repo.get_contents(content_file.path))
        if len(name) < 2 or name[1] != "java":
            continue
        class_name = name[0]
        classes.append(class_name)
        filtered_content_files.append(content_file)
        decoded = read_content_file(content_file)
        parse_class(class_name, decoded)

def add_dependencies():
    for file in filtered_content_files:
        name = file.name.split('.')
        class_name = name[0]
        decoded = read_content_file(file)
        add_class_dependency(class_name, decoded)

f = open(uml_output_txt_file_name,"w+")
f.write("@startuml\n")
traverse_content_files(content_files)
add_dependencies()
f.write("@enduml")
f.close()

def replace_in_file(to_be_replaced, replace_with):
    s = open(uml_output_txt_file_name).read()
    s = s.replace(to_be_replaced, replace_with)
    f = open(uml_output_txt_file_name, 'w')
    f.write(s)
    f.close()

# modify public, private, protected symbols
replace_in_file("private", "-");
replace_in_file("protected", "#");
replace_in_file("public", "~");

plantuml = plantuml.PlantUML("http://www.plantuml.com/plantuml/img/")
plantuml.processes_file("./uml_output.txt", "./uml_diagram.png")