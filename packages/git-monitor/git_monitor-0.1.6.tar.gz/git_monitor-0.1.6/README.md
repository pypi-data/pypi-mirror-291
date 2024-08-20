# Use Case

This project is intended to improve datascience workflows. You may want to do these simultaneously:
1. Developing a package (the *package project*), possibly a machine learning model or a data pipeline.
2. Perform some experiments in another project (the *experiment project*) by such *package project* by running a jupyter notebook or a script.
3. Log the git status of the *package project* for reproducibiliy.

`git-monitor` help you to conviniently log the git status.

If we don't want the notebooks to polute the *package project*, we have to separate the *experiment project* from the *package project*, then we cannot track everying directly in a single git repo. This problem is what `git-monitor` built for.

# How to

## Basic usage

1. Install `git-monitor` into the environment of your *package project*.
2. Make a `.git_monitor` file in the *experiment project*:
```
<pkg-nm-1>=<path-to-package-1-project-root>
<pkg-nm-2>=<path-to-package-2-project-root>
```
3. In the root `__init__.py` of the *package project*, add the lines:
```python
import git_monitor
git_monitor.Monitor.by_env("<pkg-nm-1>")
```

Then everytime you `import` or `reload` the *package project* under the *experiment project*, `git-monitor` will print the git status, including current branch, commit hash, untracked files and modified files.

## logger
```python
from git_monitor import logger
```
the messages of `git-monitor` are directed to this `logger`, which is a python native `logging.Logger` and an `logging.StreamHandler` has already been added to. The logging level is `INFO`, and the `StreamHandler` uses `sys.stdout`.