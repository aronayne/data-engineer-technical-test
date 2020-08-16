# Overview

Solutions using multiprocessing and asyncio are provided.


## multiprocessing solution

High level overview:

![ScreenShot](https://raw.githubusercontent.com/aronayne/data-engineer-technical-test/master/readme-images/multiprocessing.png)


## asycnio solution

High level overview:

![ScreenShot](https://raw.githubusercontent.com/aronayne/data-engineer-technical-test/master/readme-images/asyncio.png)

# Installation

* git clone https://github.com/aronayne/data-engineer-technical-test.git
* Navigate to project home
* Issue command (replace ENVIRONMENT_NAME with your environment) 'conda create --name ENVIRONMENT_NAME --file requirements.txt'

Activate the newly created environment: ' conda activate ENVIRONMENT_NAME '
# Testing

To run all tests navigate to data-engineer-technical-test dir and run 

'python -m unittest' .

# Running the solution files

Run below commands from dir of cloned project.

## asyncio solution

Issue command (replace PROJECT_PARENT_DIR with parent dir of project):
  
'PYTHONPATH=PROJECT_PARENT_DIR/data-engineer-technical-test python src/app/solutions/SolutionAsyncIO.py'

For example on MacOS if cloned project into ~ dir use:

PYTHONPATH=~/data-engineer-technical-test python src/app/solutions/SolutionAsyncIO.py

## multiprocessing solution

Issue command (replace PROJECT_PARENT_DIR with parent dir of project):

'PYTHONPATH=PROJECT_PARENT_DIR/data-engineer-technical-test python src/app/solutions/SolutionMultiProcessing.py'

For example on MacOS if cloned project into ~ dir use:

PYTHONPATH=~/data-engineer-technical-test python src/app/solutions/SolutionMultiProcessing.py

# Watching for DB collection changes

Project contains utility script CollectionWatchUtility.py to watch the collection.
As items are added to the mongoDB collection CollectionWatchUtility.py will print
added items to console.

Issue command (replace PROJECT_PARENT_DIR with parent dir of project)
PYTHONPATH=PROJECT_PARENT_DIR/data-engineer-technical-test python src/CollectionWatchUtility.py

For example on MacOS if cloned project into ~ dir use:

PYTHONPATH=~/data-engineer-technical-test python src/CollectionWatchUtility.py


## IDE

If running scripts or tests from an IDE such as PyCharm ensure working directory is set to PROJECT_PARENT_DIR/data-engineer-technical-test/
where PROJECT_PARENT_DIR is the dir project is contained.

# Database

Utilises cloud mongoDB (https://www.mongodb.com/) .
Database credentials are stored in AppConfig.py

mongo_db_username = ****

mongo_db_password = ****

Send e-mail to adrian.ronayne@gmail.com for login credentials.
