# Disaster Response Pipeline Project


### Table of Contents

1. [Installation](#installation)
1. [Instructions](#instructions)
2. [Project Motivation](#motivation)
3. [File Descriptions](#files)
5. [Licensing, Authors, and Acknowledgements](#licensing)

## Installation <a name="installation"></a>

There should be no necessary libraries to run the code here beyond the Anaconda distribution of Python.  The code should run with no issues using Python versions 3.*. testtest

### Instructions <a name="instructions"></a>
1. Run the following commands in the project's root directory to set up your database and model.

    - To run ETL pipeline that cleans data and stores in database
        `python data/process_data.py data/disaster_messages.csv data/disaster_categories.csv data/DisasterResponse.db`
    - To run ML pipeline that trains classifier and saves
        `python models/train_classifier.py data/DisasterResponse.db models/classifier.pkl`

2. Run the following command in the app's directory to run your web app.
    `python run.py`

3. Go to http://0.0.0.0:3001/

## Project Motivation<a name="motivation"></a>

For this project, I was interestested in using Stack Overflow data from 2017 to better understand:

1.) In which countries are the developers most happy?

2.) Does the provided equipment seem to influence the job satisfaction?

3.) Are developers that are able to invest a lot of time in improving their tooling more happy than the average developers?

The full set of files related to this course are owned by Udacity, so they are not publicly available here.  However, you can see pieces of the analysis here.  

## File Descriptions <a name="files"></a>

There is a notebooks available here to showcase work related to the above questions.  The notebooks is exploratory in searching through the data pertaining to the questions showcased by the section for each question.  Markdown cells were used to assist in walking through the thought process for individual steps.  

## Results<a name="results"></a>

The main findings of the code can be found at the post available [here](https://medium.com/@dan.gunnarsson/factors-for-developer-job-satisfaction-c2865e6c4373).

## Licensing, Authors, Acknowledgements<a name="licensing"></a>

I give credit to Stack Overflow for the data.  You can find the Licensing for the data and other descriptive information at the Kaggle link available [here](https://www.kaggle.com/stackoverflow/so-survey-2017/data).  Otherwise, feel free to use the code here as you would like! 


