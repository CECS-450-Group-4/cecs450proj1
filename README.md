# CECS 450 Group 4 Project 1
## How to run this program
Install environment:

`python3 -m venv env`

`source env/bin/activate` (or for windows: `env\scripts\activate`)

`pip3 install -r requirements.txt`

Then run program, which will generate an html file containing the visualization.

`python data_processing.py`

## How to work on the project
### First time
* Open terminal, change working directory to loation where you want cloned directory to be made (ex ~/repos/),then Clone Repository
`git clone git@github.com:CECS-450-Group-4/cecs450proj1.git`
* change to cecs450proj1 directory, then make virtual environment, activate env, then install requirements
`python3 -m venv env`
`source env/bin/activate` (or for windows: `env\scripts\activate`)
`pip3 install -r requirements.txt`
* then continue with regular workflow
### Regular Workflow
* Make sure you are up to date with the master branch
`git pull origin master`
* create a new branch locally to work on every new feature (never work on master)
`git checkout -b branchName`
* create branch on github
`git push --set-upstream origin branchName`
* work on new feature
* when you are done, add/commit files locally and then push changes to your branch
`git add -A`
`git commit -am "commit message"`
`git push origin branchName`
* Then when you are ready to merge your branch with Master, make a pull request on GitHub
    * Your organization > branches > your branch > compare & pull request
    * Someone else in your group should approve the pull request before merging your branch with master
* before merging, make sure you are up to date with master
`git checkout master`
`git pull origin master`
`git checkout branchName`
`git merge master`
* resolve conflicts.  if you can't, abort and try again
`git merge --abort`
* once you have merged your branch with master, you can delete the branch
* On Github:
`git push origin :BranchName`
* Then locally:
`git branch -d branchName`