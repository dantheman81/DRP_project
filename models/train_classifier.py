"""
Script to create a ML pipeline to create a classifier for classifying
messages during a distaster.

Sample script execution:
python train_classifier.py DisasterResponse.db classifier.pkl

Arguments:
    1) SQL Database with pre-processed data (DisasterResponse.db)
    2) Model file to save model pipeline (classifier.pkl)
"""

# import libraries
import sys
import nltk
nltk.download(['punkt', 'wordnet', 'averaged_perceptron_tagger'])

import pandas as pd
import numpy as np
import sqlite3
from sqlalchemy import create_engine
import re
import pickle

from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.metrics import make_scorer, accuracy_score, f1_score, fbeta_score, classification_report, multilabel_confusion_matrix
from sklearn.model_selection import GridSearchCV

def load_data(database_filepath):
    """Loads the messages and categories data from SQLlite database

    Parameters
    ----------
    database_filepath : str
        The message file including path

    Returns
    -------
    X : DataFrame
        Pandas DataFrame containing the features
    Y : DataFrame
        Pandas DataFrame containing the labels
    category_names : List
        Category names
    """
    engine = create_engine('sqlite:///'+ database_filepath)
    df = pd.read_sql_table('InsertTableName',engine)
    X = df['message']
    Y = df.iloc[:,4:]
    category_names = Y.columns
    return X, Y, category_names

def tokenize(text):
    """Tokenize a sentence into word tokens and cleaning up URLs

    Parameters
    ----------
    text : str
        The message as text

    Returns
    -------
    clean_tokes : list
        List with the individual words
    """
    url_regex = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    detected_urls = re.findall(url_regex, text)
    for url in detected_urls:
        text = text.replace(url, "urlplaceholder")

    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()

    clean_tokens = []
    for tok in tokens:
        clean_tok = lemmatizer.lemmatize(tok).lower().strip()
        clean_tokens.append(clean_tok)

    return clean_tokens

class StartingVerbExtractor(BaseEstimator, TransformerMixin):
    """
    Starting Verb Extractor class re-used from Udacity Program Data Scientist

    """

    def starting_verb(self, text):
        sentence_list = nltk.sent_tokenize(text)
        for sentence in sentence_list:
            pos_tags = nltk.pos_tag(tokenize(sentence))
            first_word, first_tag = pos_tags[0]
            if first_tag in ['VB', 'VBP'] or first_word == 'RT':
                return True
        return False

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X_tagged = pd.Series(X).apply(self.starting_verb)
        return pd.DataFrame(X_tagged)

def build_model():
    """Build a ML Pipline for messages classification

    Returns
    -------
    pipeline : Pipeline
        ML Pipline for messages classification
    """
    pipeline = Pipeline([
        ('features', FeatureUnion([

            ('text_pipeline', Pipeline([
                ('vect', CountVectorizer(tokenizer=tokenize)),
                ('tfidf', TfidfTransformer())
            ])),

            ('starting_verb', StartingVerbExtractor())
        ])),

        ('clf', MultiOutputClassifier(AdaBoostClassifier()))
    ])

    parameters = {
        'features__text_pipeline__vect__ngram_range': ((1, 1), (1, 2)),
        'features__text_pipeline__vect__max_df': (0.75, 1.0),
        'features__text_pipeline__vect__max_features': (None, 5000),
        'features__text_pipeline__tfidf__use_idf': (True, False)
    }

    cv = GridSearchCV(pipeline, param_grid=parameters)
    return cv


def evaluate_model(model, X_test, Y_test, category_names):
    """Perform predictions using test data and calculate overall accuracy

    Parameters
    ----------
    model : Pipeline
        ML Pipline for messages classification
    X_test : DataFrame
        Pandas DataFrame containing the features from the test set
    Y_test : DataFrame
        Pandas DataFrame containing the labels from the test set
    category_names : List
        Category names
    """
    Y_pred = model.predict(X_test)

    Y_pred_data_frame = pd.DataFrame(Y_pred, columns = Y_test.columns)
    for column in Y_test.columns:
        print('Feature: {}\n'.format(column))
        print(classification_report(Y_test[column],Y_pred_data_frame[column]))

    overall_accuracy = (Y_pred == Y_test).mean().mean()
    print(overall_accuracy)

def save_model(model, model_filepath):
    """Save the model to a pickle file.

    Parameters
    ----------
    model : Pipeline
        ML Pipline for messages classification
    model_filepath : str
        File name for the pickle file to save the model
    """
    filename = model_filepath
    pickle.dump(model, open(filename, 'wb'))


def main():
    """
    Main function

    1) Read command line arguments
    2) Load data and split into training and test sets
    3) Build model
    4) Train model
    5) Evaluate model
    6) Save model
    """
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, Y, category_names = load_data(database_filepath)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)

        print('Building model...')
        model = build_model()

        print('Training model...')
        model.fit(X_train, Y_train)

        print('Evaluating model...')
        evaluate_model(model, X_test, Y_test, category_names)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database '\
              'as the first argument and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()
