# GRIT: a light tool for easy management of open-source repositories

This simple script aims at speeding up multiples repository handling in different cases :
- Cloning multiple repository from the same owner
- Handling multiple remote
- Making quick PRs
- Listing most recently changed branch


## Installation :

```bash
python3 -m pip install .
```
or since python3.12 and venv generalization
```bash
pipx install .
```

## How to use : 
### Prerequisites
The script requires a coherent folder naming. Each repository needs to be inside a parent folder named after the owner of the repository on github. 
For instance, the [sofa](https://www.github.com/sofa-framework/sofa) repository needs to be inside a folder named `sofa-framework` : `/[...]/sofa-framework/sofa`.

### Commands

---
```bash 
grit pr <start/push> <branch_name/remote_name>
```
- ***_start_***: creates a branch with the name given as last parameter. It keeps the current un-stashed changes (same as `git checkout -b branch_name`).
- ***_push_***: push the created branch to the given remote with the branch name and track it (same as `git push --set-upstream remote_name branch_name`)

The `origin` remote will always be considered as the name of the owner (thus the folder containing the repository). It will be used to display quick link for PR making when pushing the branch.

---
```bash 
grit remote add <remote_name>
```
This command adds a remote with the same name and remote_name as the owner name to the current repository and fetch it. (same as `git remote add git@github.com/remote_name/current_folder_name`)

---
```bash 
grit clone <repository_name>
```
This command must be launched in a directory which name is the name of the owner of the repository we want to clone. 
For instance, if you wanted to clone [sofa](https://www.github.com/sofa-framework/sofa), you need to call `grit clone sofa` inside of the folder `sofa-framework`. (same as `git clone git@github.com:current_folder_name/repository_name.git`)

---
```bash 
grit branch list <remote_name> [-n number_of_branch]
```
If the `number_of_branch` is not specified, this command lists all branches of the input remote in alphabetical order
Let `n` be the number of branch given as input, it will list the `n` most recently updated branches of the remote, sorted by date of modification (the more recent in first).


---
