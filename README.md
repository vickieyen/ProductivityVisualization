# Dependency Visualization
A program that scrapes github repos to output analysis of dependencies

## Install
```
pip install PyGithub
pip install matplotlib
    Note: may need to isntall system requirements 
          brew install freetype
pip install javalang
pip install plantuml
pip install networkx
pip install pillow

OR

pip install -r requirements.txt
```


## Viz Project Specs

#### Intent of Visualization
- As a software engineer working on a large enterprise project, it would be great to know how the structure of the codebase look like.
- Imagine there was a commit that caused a critical bug and you have to revert the commit.But you’re uncertain about whether the commit has other unrelated changes
- With the Java Analyzer, you can specify a commit number and it will provide you with an analysis of whether a commit had unrelated changes. The analyzer will provide you with a UML diagram,  Contribution Graph and  a Dependency graph 
- The contribution graph can also help show when new features may have been added (increase in code) or when refactoring or deprecation of features may have occurred (decrease in code)

#### Original design
1. UML class diagram that displays hierarchies and associations 
Enable users to quickly visualize the structure of their codebase
Contribution Graph
2. Line graph that displays the contributions for all the commits
Enable users to identify when and who commited changes and can help show when feature additions and refactoring may have occurred
Dependency Graph
3. Displays the dependencies between classes for a given commit
Provides users with an analysis of whether a commit should’ve been broken down into smaller commits

#### Outcome of prototype testing
- User found UML diagram symbols were confusing, thus a legend was added to make the meaning of the symbols clear

#### New design
- Original design + legend added to UML diagram

#### Outcome of end-user testing
- User felt the contribution graph components were slightly confusing,  so improvements were made to fix this
    1. Combined additions and deletions
    2. Use date as x-axis in graph for a more comprehensive view
    2. Made text in info panel more easy to understand

#### Techniques used:
- Static Analysis
- Syntactic Analysis
- Metadata Analysis

#### Using the Java Analyzer, developers can:
1. Visualize codebase to understand hierarchies and associations using the UML Diagram
2. Identify who committed changes and when major feature additions and refactorings occurred via Contribution Graph
3. Understand dependencies for a given commit and whether commit should’ve been broken down into smaller commits via Dependency Graph