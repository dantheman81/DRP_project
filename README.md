# Disaster Response Pipeline Project


### Table of Contents

1. [Installation](#installation)
2. [Instructions](#instructions)
3. [File Descriptions](#files)
5. [Licensing, Authors, and Acknowledgements](#licensing)

## Installation <a name="installation"></a>

The basis for running this code is the Anaconda distribution of Python.  The code should run with no issues using Python versions 3.*.

Dependencies:
Machine Learning Libraries: NumPy, SciPy, Pandas, Sciki-Learn
Natural Language Process Libraries: NLTK
SQLlite Database Libraqries: SQLalchemy
Web App and Data Visualization: Flask, Plotly

### Instructions <a name="instructions"></a>
1. Run the following commands in the project's root directory to set up your database and model.

    - To run ETL pipeline that cleans data and stores in database
        `python data/process_data.py data/disaster_messages.csv data/disaster_categories.csv data/DisasterResponse.db`
    - To run ML pipeline that trains classifier and saves
        `python models/train_classifier.py data/DisasterResponse.db models/classifier.pkl`

2. Run the following command in the app's directory to run your web app.
    `python run.py`

3. Go to http://0.0.0.0:3001/

## File Descriptions <a name="files"></a>

There is notebooks available here to showcase the work how to find .  The notebooks is exploratory in searching through the data pertaining to the questions showcased by the section for each question.  Markdown cells were used to assist in walking through the thought process for individual steps.  

- app
| - template
| |- master.html  # main page of web app
| |- go.html  # classification result page of web app
|- run.py  # Flask file that runs app

- data
|- disaster_categories.csv  # data to process 
|- disaster_messages.csv  # data to process
|- process_data.py # python program to load and process the input data
|- InsertDatabaseName.db   # database to save clean data to

- models
|- train_classifier.py # python program to build and train a pipeline to predict which categories are matched by one message.
|- classifier.pkl  # saved model 

## Licensing, Authors, Acknowledgements<a name="licensing"></a>

I give credit to Figure 8 for the data and Udacity for the project description and ideas.  Otherwise, feel free to use the code here as you would like! 
