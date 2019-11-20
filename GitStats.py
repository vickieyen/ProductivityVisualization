from github import Github
import matplotlib.pyplot as plt
import numpy as np

# DO NOT PUSH TOKEN, DELETE BEFORE PUSHING
token = ""
g = Github(token)

repo = g.get_user().get_repo("ExamGenerator")

if __name__ == '__main__':
    commits = repo.get_commits().reversed
    # commit_additions = []
    # commit_deletions = []
    commit_authors = []
    commit_lines = []
    commit_dates = []
    current_date = None
    for commit in commits:
        commit_date = commit.commit.author.date.date()
        if commit_date != current_date:
            current_date = commit_date
            commit_dates.append(commit_date)
            commit_lines.append(commit.stats.total)
            commit_authors.append({commit.commit.author.name: {"additions": commit.stats.additions, "deletions": commit.stats.deletions}})
        else:
            if commit_authors[-1].get(commit.commit.author.name) != None:
                commit_authors[-1][commit.commit.author.name]["additions"] += commit.stats.additions
                commit_authors[-1][commit.commit.author.name]["deletions"] += commit.stats.deletions
            else:
                commit_authors[-1][commit.commit.author.name] = {"additions": commit.stats.additions, "deletions": commit.stats.deletions}
            commit_lines[-1] += commit.stats.total

    x = np.arange(len(commit_dates))

    fig, axes = plt.subplots()
    plt.xticks(x, commit_dates, rotation='vertical')
    graph = plt.plot(x, commit_lines)

    annot = plt.annotate("", xy=(0,0), xytext=(50,50), textcoords="offset pixels",
                        bbox=dict(boxstyle="round", fc="w"),
                        arrowprops=dict(arrowstyle="->"), verticalalignment="center")
    annot.set_visible(False)

    def annotation_text(index):
        text = "%s Changes:" % (commit_dates[index])
        for key in commit_authors[index]:
            author = key
            print(key)
            additions = commit_authors[index][author]["additions"]
            deletions = commit_authors[index][author]["deletions"]
            text += "\n\nLines added: %s\nLines deleted: %s\nModified by: %s" % (additions, deletions, author)
        return text

    def update_annotation(line, index):
        mid_y = (max(commit_lines)/2)
        y_coord = line.get_ydata()[index]
        annot.xy = (index, y_coord)
        text = annotation_text(index)
        annot.set_text(text)
        annot.set_fontsize('xx-small')

        annot_x = 50
        annot_y = mid_y - y_coord
        if index >= (len(x)/2):
            bbox_width = annot.get_bbox_patch().get_width()
            annot_x = (-bbox_width - 50)

        annot.set_position((annot_x, annot_y))


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
    fig.tight_layout()
    plt.show()
    