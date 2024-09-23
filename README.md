# TGSRTC_Productivity

## 1. Open Github
    - Create a new repository - TGSRTC_Productivity
    - Keep it "Public"
    - Add a readme file
    - Add a gitignore
    - Take an MIT license

    Copy the web URL in GitHub for the repository. Its under <> Code button

## 2. Go the parent folder where you want the project folder to get created
    - In that folder right click and open git bash prompt (make sure its installed)
    - Run: git clone [github repository name]
    - All files in github get copied to the folder including the repository folder

## 3. In that parent folder, right and open a command prompt. Type vscode .
    - vscode opes with all the folder contents (make sure vscode is installed)

## 4. Create a folder called template.py
    - In that folder, copy the code from a previous template.py file
    - In the code, make the project name as 'TGSRTC_Productivity'

## 5. Create the conda environment
    - Right click in the project folder and open git bash
    - Create the conda environment
    - SETTING UP THE ENVIRONMENT CAN BE A BIG CHALLENGE
    - SOMETIMES CONDA COMMAND WILL NOT WORK
    - DO ECHO PATH MAKE SURE /C/Users/sr/anaconda3/Scripts AND /C/Users/sr/anaconda3/condabin ARE THERE
    - EDIT .BASHRC FILE
        - nano ~/.bash_profile
        - source ~/.bashrc
        - SAVE & EXIT & RESTART
    - USE /C/Users/sr/anaconda3/Scripts/conda init bash TO INITIATE
    - RESTART GITBASH
    - conda activate tgsrtc_prod
    - In Github the right environment should get shown at the top of the prompt as shown below
    (tgsrtc_prod)
    sr@Suneel MINGW64 ~/OneDrive/Documents/Work/Agni/Development/Python/TGSRTC_Productivity (main)
    - conda info --envs -The current environment should have a * infront of it

    ```python
    conda create -n tgsrtc_prod python=3.12 -y
    ```
    - Activate the environment: 
    
    ```python
    conda activate tgsrtc_prod
    ```
    - To view the environment: 
    
    ```python
    conda info --envs
    ```
    - The tgsrtc_project environment should have * infront of it - indicating that its active

## 6. In the conda environment in gitbash
    - Execute the template.py code

    ```python
    python template.py
    ```
    - All folders get created

## 7. Commit changes to github
    
    ```console
    git add .
    ```

    ```console
    git commit -m "folder structure added"
    ```

    ```console
    git push -u origin main
    ```

    OR the same can be done in vscode using the menu to the right side where you see an icon for source control

## 8. In requirements.txt add all the required libraries and save

 pip install -r requirements.txt

 ISSUE: Got resolved by this...
 pip install --upgrade pip setuptools #to upgrade
 pip cache purge

## 9. Add setup.py file

Add the standard code from setup.py.
Enter the right source code name.

## 10. Commit changes to github
    
    ```console
    git add .
    ```

    ```console
    git commit -m "requirements"
    ```

    ```console
    git push -u origin main
    ```

     OR the same can be done in vscode using the menu to the right side where you see an icon for source control

## 11. Implement Logging

Add the standard code from -init_.py file kept in src folder.

Save the file.
This will help in debugging the code

## 12. Set-up of Utils (functionality that we will be using frequently)

Go to common.py file
Past the code and save

## 13. Commit changes to github
    
    ```console
    git add .
    ```

    ```console
    git commit -m 'exception, logger, and utils added"
    ```

    ```console
    git push -u origin main
    ```

     OR the same can be done in vscode using the menu to the right side where you see an icon for source control






