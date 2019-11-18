import os

from class_parser import Class

def read_as_text(filename):
    with open(filename, 'r') as f:
        return f.read()

classes = []

root_dir = "../Project 1/src"

# create Class objects from all .java files in root directory
for subdir, dirs, files in os.walk(root_dir):
    for file in files:
        if (file.endswith(".java")):
            file_path = subdir + os.sep + file
            file_txt = read_as_text(file_path)
            new_class = Class(file_txt)
            classes.append(new_class)

# set dependencies
class_names = []
for class_found in classes:
    class_names.append(class_found.name)

for class_found in classes:
    class_found.find_dependencies(class_names)

# print for debug
for class_found in classes:
    print(class_found)
