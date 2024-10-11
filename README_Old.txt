1. Open git hub

2. Create a new repository - TGSRTC_Productivity
   - Keep it "Public"
   - Add a readme file
   - Add a git ignore
   - Take an MIT license

Copy the web URL in GitHub for the repository. Its under <> Code button
https://github.com/sure-AI/TGSRTC_Productivity.git

3. Create a project folder on your PC for the project and give it a name

4. In that folder open git bash 
(this tool gets installed when GitHub is installed on the machine)

In git bash:
git clone [repository address]
https://github.com/sure-AI/TGSRTC_Productivity.git

All the files from GitHub get copied to the local folder.

5. Open vscode from git bash
code . (enter)

6. In VScode the project opens

7. Create a file called template.py in this folder by clicking the 'create file' option button. In that give the "project name" and take the folder structure code from a previous file

8. Go to git bash terminal - clear the terminal
clear

9. ISSUES - CONDA ENVIRONMENT
Creating a conda environment using this command:
conda activate "C:\Users\sr\OneDrive\Documents\Work\Agni\Wine Quality ML Project\MLProject_Winequality\venv"

Checking which environment is active 
conda info --envs

IMPORTANT: You should be in the right conda environment

10. In the conda environment execute 
python template.py

all folders will get created

11. Commit to githum

git add .
git commit -m "folder structure added"
git push -u origin main

12. Add all the required libraries into requirements.txt and SAVE (ctrl+s)

13. Add the code to setup.py. Change the user name and email and save

14. Now in git bash run
pip install -r requirements.txt
\
Check if all the requirements got installed properly
pip check 

15. Commit to github

git add .
git commit -m "requirements added"
git push -u origin main

16. Update the Utils package _init_.py file with the standard code

17. Update the Utils package common.py file with the standard code

18. Open the config file and in that copy the standard code
Point the right path to the CSV file.

Save the CSV file in your git hub folder. Copy the link to that folder and paste that in the config file

19. Open the entity folder and in that config_entity.py
Paste the standard code

20. Open constants file and update it

21. 
























