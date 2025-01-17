"""
Script to load and pre-process data

Sample script execution:
python process_data.py disaster_messages.csv disaster_categories.csv DisasterResponse.db

Arguments:
    1) Messages file (disaster_messages.csv)
    2) Categories file (disaster_categories.csv)
    3) SQL Database to output the pre-processed data (DisasterResponse.db)
"""

import sys
import pandas as pd
import numpy as np
import sqlite3
from sqlalchemy import create_engine

def load_data(messages_filepath, categories_filepath):
    """Loads the messages and categories data

    Parameters
    ----------
    messages_filepath : str
        The message file including path
    categories_filepath : str
        The categories file including path

    Returns
    -------
    df : DataFrame
        The loaded message and categories data merged to a Pandas DataFrame
    """
    messages = pd.read_csv(messages_filepath)
    categories = pd.read_csv(categories_filepath)
    df = pd.merge(messages,categories,on='id')
    return df

def clean_data(df):
    """Clean the DataFrame by dividing categories in to separate columns,
    removing duplicates and removing colums and rows with NaN values.

    Parameters
    ----------
    df : DataFrame
        The loaded message and categories data merged to a Pandas DataFrame

    Returns
    -------
    df : DataFrame
        The cleaned data frame with loaded message and categories data
    """
    # create a dataframe of the 36 individual category columns
    categories = df.categories.str.split(";",expand=True)

    # select the first row of the categories dataframe
    row = categories.iloc[0,:]

    # use this row to extract a list of new column names for categories.
    # one way is to apply a lambda function that takes everything
    # up to the second to last character of each string with slicing
    category_colnames = row.apply(lambda x: x[:-2])

    # rename the columns of `categories`
    categories.columns = category_colnames

    # convert category values to just numbers 0 and 1
    for column in categories:
        # set each value to be the last character of the string
        categories[column] = categories[column].str[-1]
        # convert column from string to numeric
        categories[column] = categories[column].astype(np.int)

    # merge datasets messages and categories
    df = df.drop('categories',axis=1)
    df = pd.concat([df,categories],axis=1)

    # remove duplicates
    df = df.drop_duplicates()

    # drop column original since it contains many contains NaNs
    df = df.drop('original', axis=1)

    # drop rows with NaNs
    df = df.dropna()
    return df

def save_data(df, database_filename):
    """Save the dataframe with messages and categories data to a SQLlite
    database.

    Parameters
    ----------
    df : DataFrame
        The loaded message and categories data merged to a Pandas DataFrame
    database_filename : str
        The loaded message and categories data merged to a Pandas DataFrame
    """
    engine = create_engine('sqlite:///'+ database_filename)
    df.to_sql('InsertTableName', engine, index=False)

def main():
    """
    Main function

    1) Read command line arguments
    2) Load data
    3) Clean data
    4) Save data to SQLite database
    """
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)

        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)

        print('Cleaned data saved to database!')

    else:
        print('Please provide the filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db')


if __name__ == '__main__':
    main()
