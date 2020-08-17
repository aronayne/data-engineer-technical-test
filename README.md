# Overview

Provided are solutions using multiprocessing and asyncio Python libraries.

## Multiprocessing solution

High-level overview:

![ScreenShot](https://raw.githubusercontent.com/aronayne/data-engineer-technical-test/master/readme-images/multiprocessing.png)

## AsycnIO solution

High-level overview:

![ScreenShot](https://raw.githubusercontent.com/aronayne/data-engineer-technical-test/master/readme-images/asyncio.png)

# Installation

Download and install Anaconda from https://docs.conda.io/projects/conda/en/latest/user-guide/install/download.html

* git clone https://github.com/aronayne/data-engineer-technical-test.git
* Navigate to project home
* Issue command (replace ENVIRONMENT_NAME with your environment) 'conda create --name ENVIRONMENT_NAME --file requirements.txt'

Activate the newly created environment: ' conda activate ENVIRONMENT_NAME '

## Database connection setup

Utilises cloud mongoDB (https://www.mongodb.com/) .
Database credentials are stored in src/app/config/AppConfig.py

mongo_db_username = ****

mongo_db_password = ****

Send e-mail to adrian.ronayne@gmail.com for login credentials.

# Running Tests

To run all tests navigate to data-engineer-technical-test dir and run 

'python -m unittest' .

# Running the solution files

Run below commands from dir of cloned project.

## Running AsyncIO solution

Issue command (replace PROJECT_PARENT_DIR with parent dir of the cloned project):
  
'PYTHONPATH=PROJECT_PARENT_DIR/data-engineer-technical-test python src/app/solutions/SolutionAsyncIO.py'

For example, on macOS if cloned project into ~ dir use:

PYTHONPATH=~/data-engineer-technical-test python src/app/solutions/SolutionAsyncIO.py

## Running Multiprocessing solution

Issue command (replace PROJECT_PARENT_DIR with parent dir of project):

'PYTHONPATH=PROJECT_PARENT_DIR/data-engineer-technical-test python src/app/solutions/SolutionMultiProcessing.py'

For example, on macOS if cloned project into ~ dir use:

PYTHONPATH=~/data-engineer-technical-test python src/app/solutions/SolutionMultiProcessing.py

# Watching for DB collection changes

A utility script CollectionWatchUtility.py has been created to watch the DB collection for changes.
As items are added to the mongoDB collection, CollectionWatchUtility.py will print added items to console.

Issue command (replace PROJECT_PARENT_DIR with parent dir of project)
PYTHONPATH=PROJECT_PARENT_DIR/data-engineer-technical-test python src/CollectionWatchUtility.py

For example, on macOS if cloned project into ~ dir use:

PYTHONPATH=~/data-engineer-technical-test python src/CollectionWatchUtility.py

## IDE

If running scripts or tests from an IDE such as PyCharm ensure working directory is set to PROJECT_PARENT_DIR/data-engineer-technical-test/
where PROJECT_PARENT_DIR is the dir project is contained.