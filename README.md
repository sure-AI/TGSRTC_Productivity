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
Paste the code and save.
Make sure the project folder is named correctly 'TGSRTC_Productivity'

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


## 14. Note the workflow for updating the files

Update config.yaml
Update schema.yaml
Update params.yaml
Update the entity
Update the configuration manager in src config
Update the components
Update the pipeline
Update the main.py
Update the app.py 


## 15. DATA INGESTION

First in the research folder build a prototype of the code and then implement it in a modular format

### A. Create a file called 01_data_ingestion.ipynb

### B. Open the file config/config.yaml

Add the standard code from github
Set the right address of the zip file stored on github
It should by saved as .zip file

### C. Schema.yaml no changes

### D. Params.yaml no changes

### E. Complete the code in the 01_data_ingestion file

### F. Add the code to constants/__init__.py file

### G. Dont keen the schema.yaml file empty. Add some dummy code

### H. Run the 01_data_ingestion file

Huge issues with the zip file being correct. Not sure how this got resolved. Used a different download function.


## 16. Converting the notebook experiment to modular coding

### A. Update the entity file with the code

### B. Update the src/config/configuration file

### C. Within components add a file data_ingestion.py

### D. Add the code and change the project name

### E. Create a new file in pipeline called stage_01_data_ingestion.py

Copy the code. Change the project name

Note: Look at making the project name generic so that there is only one place it gets changed

### F. Now in main.py enter the code and save

### G. Run the main.py code in git bas terminal

python main.py

Note: Delete the artifacts folder before running this.
Upon successful execution the artifacts gets created

## 17. Data Validation

### A. First do the notebook research

Create a new file in the research folder called 02_data_validation.ipynb

### B. Update config.yaml

### C. Update schema.yaml

### D. Run the .ipynb file

Artifacts should now have a folder 'data_validation'
This should have a file called status.txt which will store True or False

### E. NOW do the modular coding

Update config.yaml - DONE
Update schema.yaml - ALREADY DONE
Update params.yaml - NA
Update the entity - DONE 
Update the configuration manager in src config - DONE (Sets Paths)
Update the components - DONE (Does the real validation)
Update the pipeline - DONE
Update the main.py - DONE
Update the app.py 

### F. Delete artifacts folder and run main.py

Python main.py

An artifacts folder should get created and in the data_validation folder the file called status.txt should get store with a value "True" in it


## 18. Commit changes to github
    
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


## 19. DATA TRANSFORMATION

### A. Create a folder called 03_data_transformation in research folder

Add the research script. HEre I am seleting only the relevant columns and doing one-hot coding and test train split

### B. Apply modular code

Update config.yaml - DONE
Update schema.yaml - ALREADY DONE
Update params.yaml - NA
Update the entity - DONE 
Update the configuration manager in src config - DONE (Sets Paths)
Update the components - DONE (Does the real validation)
Update the pipeline - DONE
Update the main.py - DONE
Update the app.py 

### C. Delete artifacts folder and run main.py

Python main.py

An artifacts folder should get created and in the data_transformation folder the test.csv and train.csv will get stored

## 20. Commit changes to github
    
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


## 21. MODEL TRAINING
    
### A. Create a folder called 04_model_training in research folder

Add the research script. Here I am implementing a logistic regression and hence the imports and parameters are set accordingly.

### B. Apply modular code

Update config.yaml - DONE
Update schema.yaml - ALREADY DONE
Update params.yaml - DONE (Important)
Update the entity - DONE 
Update the configuration manager in src config - DONE (Sets Paths)
Update the components - DONE 
Update the pipeline - DONE
Update the main.py - DONE
Update the app.py - NA

### C. Delete artifacts folder and run main.py

Python main.py

An artifacts folder should get created and in the model_training folder the .pkl file will get stored  

## 22. Commit changes to github
    
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


