import javalang

class Class:
    def __init__(self, file):
        self.file = file
        self.tree = javalang.parse.parse(file)
        self.name = None
        self.fields = []
        self.methods = []
        self.extends = None
        self.implements = None
        self.dependencies = []
        
        # parse class using tree provided
        self.parse()

    def __repr__(self):
        result = "CLASS - " + self.name + "\n"
        for field in self.fields:
            result += "     FIELDS - " + repr(field) + "\n"
        result += "\n"
        for method in self.methods:
            result += "     METHODS - " + repr(method) + "\n"
        result += "\n"
        for dependency in self.dependencies:
            result += "     DEPENDENCIES - " + dependency + "\n"
        result += "\n"
        return result

    def parse(self):
        self.parse_name(self.tree)
        self.parse_implements(self.tree)
        self.parse_extends(self.tree)
        for body in self.tree.types[0].body:
            if isinstance(body, javalang.tree.FieldDeclaration):
                self.parse_field(body)
            if isinstance(body, javalang.tree.MethodDeclaration):
                self.parse_method(body)

    def parse_name(self, tree):
        self.name = tree.types[0].name.encode("utf-8")
        # print(self.name)

    def parse_implements(self, tree):
        implements = tree.types[0].implements
        if (implements):
            self.implements = implements.name.encode("utf-8")
        # print(self.implements)

    def parse_extends(self, tree):
        extends = tree.types[0].extends
        if (extends):
            self.extends = extends.name.encode("utf-8")
        # print(self.extends)
    
    def parse_field(self, field_dec):
        field = Field()

        # set access
        field.access = "public"
        if (field_dec.modifiers):
            field.access = field_dec.modifiers.pop().encode("utf-8")

        # set name
        field.name = field_dec.declarators[0].name.encode("utf-8")

        # set type
        field.var_type = field_dec.type.name.encode("utf-8")

        self.fields.append(field)
        # print(vars(field))

    def parse_method(self, method_dec):
        method = Method()

        # set annotation
        method.annotation = None
        if (method_dec.annotations):
            method.annotation = method_dec.annotations[0].name.encode("utf-8")

        # set access
        method.access = "public"
        if (method_dec.modifiers):
            method.access = method_dec.modifiers.pop().encode("utf-8")

        # set name
        method.name = method_dec.name.encode("utf-8")

        # set parameters
        method.params = []
        for form_param in method_dec.parameters:
            param = {"name": form_param.name.encode("utf-8"), "type": form_param.type.name.encode("utf-8")}
            method.params.append(param)
        
        # set return type
        method.return_type = "void"
        if (method_dec.return_type):
            method.return_type = method_dec.return_type.name.encode("utf-8")

        self.methods.append(method)
        # print(vars(method))

    # feed names of the classes that you want to find dependencies for
    # and it will return the class names that it depends on
    def find_dependencies(self, class_names):
        tokens = list(javalang.tokenizer.tokenize(self.file))
        for token in tokens:
            if (isinstance(token, javalang.tokenizer.Identifier)):
                token_type = token.value.encode("utf-8")
                if (token_type in class_names):
                    self.dependencies.append(token_type)

        # remove duplicates
        self.dependencies = list(dict.fromkeys(self.dependencies))

        # remove itself
        self.dependencies.remove(self.name)

class Field:
    def __repr__(self):
        result = "name: " + self.name + " / "        
        result += "access: " + self.access + " / "
        result += "type: " + self.var_type
        return result

class Method:
    def __repr__(self):
        result = "name: " + self.name + " / "
        result += "access: " + self.access + " / "
        result += "return type: " + self.return_type
        return result