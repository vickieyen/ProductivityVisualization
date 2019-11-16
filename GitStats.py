from github import Github
import matplotlib.pyplot as plt
import numpy as np

# DO NOT PUSH TOKEN, DELETE BEFORE PUSHING
token = "4dbd74599404d9bce28a9ee9440d8100f44bcd13"
g = Github(token)

repo = g.get_user().get_repo("ExamGenerator")

# same
commits = repo.get_commits()
commit_shas = []
commit_additions = []
commit_deletions = []
commit_lines = []
commit_authors = []
for commit in commits:
    commit_shas.append(commit.sha)
    commit_additions.append(commit.stats.additions)
    commit_deletions.append(commit.stats.deletions)
    commit_lines.append(commit.stats.total)
    if commit.author is not None:
        commit_authors.append(commit.author.login)
    else:
        commit_authors.append("Unnamed")

fig = plt.figure()
x = np.arange(len(commit_shas))
plt.xticks(x, commit_shas, rotation = 'vertical')
plt.plot(x, commit_lines)
plt.show()


