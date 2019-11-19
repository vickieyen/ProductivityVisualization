from github import Github

# DO NOT PUSH TOKEN, DELETE BEFORE PUSHING
token = "dc594fcd6d293bb8004fc1c9ddf2a6f89d961ff8"
g = Github(token)

repo = g.get_user().get_repo("ExamGenerator")

commits = repo.get_commits()

files = []

for commit in commits:
    files.append(commit.files)
