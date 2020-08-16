# Overview

Solutions using multiprocessing and asyncio are provided.


## multiprocessing

High level overview:

![ScreenShot](https://raw.githubusercontent.com/aronayne/data-engineer-technical-test/master/readme-images/multiprocessing.png)


## asycnio

High level overview:

![ScreenShot](https://raw.githubusercontent.com/aronayne/data-engineer-technical-test/master/readme-images/asyncio.png)

# Installation

* git clone
* Navigate to project home
* Issue command (replace ENVIRONMENT_NAME with your environment) 'conda create --name ENVIRONMENT_NAME --file requirements.txt'

# Running the files

## asyncio solution

Issue command (replace PROJECT_PARENT_DIR with parent dir of project):
  'PYTHONPATH=PROJECT_PARENT_DIR/data-engineer-technical-test python app/src/solutions/SolutionMultiProcessing.py'

## multiprocessing solution

Issue command (replace PROJECT_PARENT_DIR with parent dir of project):
  'PYTHONPATH=PROJECT_PARENT_DIR/data-engineer-technical-test python app/src/solutions/SolutionAsyncio.py'

## IDE

If running solutions from IDE such as PyCharm ensure working directory is set to PROJECT_PARENT_DIR/data-engineer-technical-test/
where PROJECT_PARENT_DIR is the dir project is contained.

# Testing

Navigate to cloned app dir and run 'python -m unittest' to run all tests.

# Watching for DB collection changes

Project contains utility script CollectionWatchUtility.py to watch the collection.
As items are added to the mongoDB collection CollectionWatchUtility.py will print
added items to console.

Issue command (replace PROJECT_PARENT_DIR with parent dir of project)
PYTHONPATH=PROJECT_PARENT_DIR/data-engineer-technical-test python app/CollectionWatchUtility.py

# Database

Utilises cloud mongoDB (https://www.mongodb.com/) .
Database credenitals are stored in AppConfig.py

mongo_db_username = ****

mongo_db_password = ****

Send e-mail to adrian.ronayne@gmail.com for login credentials.

# Improvments


