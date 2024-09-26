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

Add the research script and test. Here I am implementing a logistic regression and hence the imports and parameters are set accordingly.

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
    git commit -m 'model trainer added"
    ```

    ```console
    git push -u origin main
    ```

     OR the same can be done in vscode using the menu to the right side where you see an icon for source control

## 23. MODEL EVALUATION
    
### A. Link Github repository on Dagshub

    Under Remote --> Experiments, see the URI
    MLFLOW_TRACKING_URI=https://dagshub.com/sure-AI/TGSRTC_Productivity.mlflow
    
    import mlflow with mlflow.start_run(): mlflow.log_param('parameter name', 'value') mlflow.log_metric('metric name', 1)

### B. Run each of the commands in gitbash:

    '''bash

    export MLFLOW_TRACKING_URI=https://dagshub.com/sure-AI/TGSRTC_Productivity.mlflow

    export MLFLOW_TRACKING_USERNAME=sure-AI

    export MLFLOW_TRACKING_PASSWORD=Iwdwis100%


### C. Create a folder called 05_model_evaluation in research folder

Add the research script and test.

### D. Apply modular code

Update config.yaml - DONE
Update schema.yaml - ALREADY DONE
Update params.yaml - DONE (Important)
Update the entity - DONE 
Update the configuration manager in src config - DONE (Sets Paths)
Update the components - DONE 
Update the pipeline - DONE
Update the main.py - DONE
Update the app.py - NA

### E. Delete artifacts folder and run main.py

Python main.py

An artifacts folder should get created and in ML Flow directory the experiment should get recorded

## 24. Commit changes to github
    
    ```console
    git add .
    ```

    ```console
    git commit -m 'model trainer added"
    ```

    ```console
    git push -u origin main
    ```

     OR the same can be done in vscode using the menu to the right side where you see an icon for source control


## 25. Creating the prediction pipeline

### A. Create a folder in pipeline called prediction.py and copy the code

## 26. Creating the app.py

### B. Create the code using streamlit for creating the dashboards

## 27. Create a file called main.yaml in github folder and copy the code

### 28. CI/CD implementation

AWS-CICD-Deployment-with-Github-Actions

1. Login to AWS console.

2. Create IAM user for deployment
#with specific access 

AmazonEC2ContainerRegistryFullAccess
AmazonEC2FullAccess

3. In the user, go to security credentials --> create access key --> command line interface

4. Download the access key .csv file and save it

5. Creating the ECR respository to store the docker image

Got to ECR in AWS -- Create Respository

Name: tgsrtc_prod

enter create respository

6. Copy the URI 

975050311903.dkr.ecr.us-east-1.amazonaws.com/tgsrtc_prod

7. Create the EC2 Ubuntu machine

Go to EC2 service in AWS

Click on launch instance

Instace select 8GB RAM t2. Large

Select key pair, examplekeypair

In instances, click on that instance ID

Click on connect --> Terminal gets launched

run all these commends in the terminal 

sudo apt-get update -y
sudo apt-get upgrade -y
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu
newgrp docker


Check if docker is working by typing 
docker --version

8. Configure EC2 as self-hosted runner

go to github and in the project folder, go to settings

--> actions --> runners --> new self hosted runner

Select Linux format

Execute the commands given there in the EC2 terminal

# Create a folder

$ mkdir actions-runner && cd actions-runner

# Download the latest runner package

$ curl -o actions-runner-linux-x64-2.319.1.tar.gz -L https://github.com/actions/runner/releases/download/v2.319.1/actions-runner-linux-x64-2.319.1.tar.gz

# Optional: Validate the hash

$ echo "3f6efb7488a183e291fc2c62876e14c9ee732864173734facc85a1bfb1744464  actions-runner-linux-x64-2.319.1.tar.gz" | shasum -a 256 -c

# Extract the installer

$ tar xzf ./actions-runner-linux-x64-2.319.1.tar.gz

# Create the runner and start the configuration experience

$ ./config.sh --url https://github.com/sure-AI/TGSRTC_Productivity --token BIBW3STLN546XFYXO2LYHG3G6QPVA

Copied!# Last step, run it!

$ ./run.sh

AWS will show " Listening to jobs'

9. Set up github secrets

Got to github --> settings --> secrets and variables --> New resository secret

AWS_ACCESS_KEY_ID

AWS_SECRET_ACCESS_KEY

AWS_REGION = us-east-1

AWS_ECR_LOGIN_URI = 975050311903.dkr.ecr.us-east-1.amazonaws.com

ECR_REPOSITORY_NAME = tgsrtc_prod

10. In app.py add some code at the end 

11. Commit code in git hub


CI/CD Issues

1. On aws EC2 Ubuntu terminal. keep clearing the images and volumes that are not used.

./run.sh to initiate the runner

df -h -- to get the details of the dockers file

docker image prune -- to prune the images

docker volume prune to prune the volumes

docker stop TGSRTC_prod -- to stop the docker file

docker rm TGSRTC_prod -- to remove the docker file

docker system prune -a --volumes -- to delete volumes


12. Do the security setting to suit the application.

Add a security setting to listen to port 8510 (as the application is streamlit)




