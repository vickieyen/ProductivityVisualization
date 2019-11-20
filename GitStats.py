from github import Github
import matplotlib.pyplot as plt
import numpy as np

# DO NOT PUSH TOKEN, DELETE BEFORE PUSHING
token = ""
g = Github(token)

repo = g.get_user().get_repo("ExamGenerator")

if __name__ == '__main__':
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

    x = np.arange(len(commit_shas))

    fig, axes = plt.subplots()
    graph = plt.plot(x, commit_lines)

    annot = plt.annotate("", xy=(0,0), xytext=(30,30), textcoords="offset points",
                        bbox=dict(boxstyle="round", fc="w"),
                        arrowprops=dict(arrowstyle="->"))
    annot.set_visible(False)


    def update_annotation(line, index):
        annot.xy = (index, line.get_ydata()[index])
        text = "Lines added: %s\nLines deleted: %s\nModified by: %s" % (commit_additions[index], commit_deletions[index], commit_authors[index])
        annot.set_text(text)
        annot.get_bbox_patch().set_alpha(0.4)


    def onclick(event):
        is_visible = annot.get_visible()
        if event.inaxes == axes:
            for line in graph:
                contains, index = line.contains(event)
            if contains:
                update_annotation(line, index['ind'][0])
                annot.set_visible(True)
                fig.canvas.draw_idle()
            else:
                if is_visible:
                    annot.set_visible(False)
                    fig.canvas.draw_idle()


    fig.canvas.mpl_connect("button_press_event", onclick)

    plt.show()

