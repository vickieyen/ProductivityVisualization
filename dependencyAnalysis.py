from github import Github
import re
import os

# Private token
token = ""
g = Github(token)

repo = g.get_user().get_repo("ExamGenerator")

def analyzeCommitDependency(commitHash, classes, threshold):
    commit = repo.get_commit(commitHash)
    stats = commit.stats
    files = commit.files
    dependencies = []
    filesNotInDependency = []

    # Get the dependency of the first file
    firstFilePath = files[0].filename
    firstFileNameWithExtension = os.path.basename(firstFilePath)
    firstFileName = os.path.splitext(firstFileNameWithExtension)[0]

    for class_object in classes:
        if class_object.name == firstFileName:
            dependencies += class_object.dependencies

    # Determine whether committed file belong together
    for file in files[1:]:
        filePath = file.filename
        fileNameWithExtension = os.path.basename(filePath)
        fileName = os.path.splitext(fileNameWithExtension)[0]

        try:
            dependencies.index(fileName)
        except:
            if (file.changes/ stats.total) > threshold:
                filesNotInDependency += fileName


    if len(filesNotInDependency) > 0:
        return "Summary: The following files does not fit into the overall dependency of the commit" + filesNotInDependency

    return "Summary: All file changes are part of the same dependency."