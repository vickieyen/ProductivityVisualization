from github import Github
import base64

# DO NOT PUSH TOKEN, DELETE BEFORE PUSHING
token = ""

g = Github(token)
repo = g.get_user().get_repo("ExamGenerator")

content_files = repo.get_contents("/src")


def read_content_file(content_file):
    content = content_file.content
    decoded = base64.b64decode(content).decode("utf-8")
    print(decoded)


def traverse_content_files(content_files):
    for content_file in content_files:
        name = content_file.name.split('.')
        if content_file.type == "dir":
            traverse_content_files(repo.get_contents(content_file.path))
        if len(name) < 2 or name[1] != "java":
            continue
        read_content_file(content_file)


f = open("uml_output.txt","w+")
f.write("@startuml")

traverse_content_files(content_files)
