
# data_transformation/data_transformation.py

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, OneHotEncoder, LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer


def normalize(data):
    """
    Normalize numerical features in the dataset to range [0, 1].

    Parameters:
    data (DataFrame): The dataset with numerical features.

    Returns:
    DataFrame: The dataset with normalized values.
    """
    scaler = MinMaxScaler()
    numerical_data = data.select_dtypes(include=[np.number])
    scaled_data = scaler.fit_transform(numerical_data)

    return pd.DataFrame(scaled_data, columns=numerical_data.columns, index=data.index)


def standardize(data):
    """
    Standardize numerical features in the dataset to have mean 0 and variance 1.

    Parameters:
    data (DataFrame): The dataset with numerical features.

    Returns:
    DataFrame: The dataset with standardized values.
    """
    scaler = StandardScaler()
    numerical_data = data.select_dtypes(include=[np.number])
    scaled_data = scaler.fit_transform(numerical_data)

    return pd.DataFrame(scaled_data, columns=numerical_data.columns, index=data.index)


def encode_onehot(data, columns):
    """
    Encode categorical features using one-hot encoding.

    Parameters:
    data (DataFrame): The dataset with categorical features.
    columns (list): List of columns to encode.

    Returns:
    DataFrame: The dataset with one-hot encoded values.
    """
    encoder = OneHotEncoder(sparse_output=False, drop='first')
    encoded_data = encoder.fit_transform(data[columns])
    encoded_df = pd.DataFrame(encoded_data, columns=encoder.get_feature_names_out(columns), index=data.index)

    return pd.concat([data.drop(columns, axis=1), encoded_df], axis=1)


def encode_label(data, columns):
    """
    Encode categorical features using label encoding.

    Parameters:
    data (DataFrame): The dataset with categorical features.
    columns (list): List of columns to encode.

    Returns:
    DataFrame: The dataset with label encoded values.
    """
    for col in columns:
        encoder = LabelEncoder()
        data[col] = encoder.fit_transform(data[col])

    return data


def aggregate(data, groupby_column, agg_dict):
    """
    Aggregate the dataset based on a grouping column and aggregation functions.

    Parameters:
    data (DataFrame): The dataset to aggregate.
    groupby_column (str): The column to group by.
    agg_dict (dict): Dictionary of columns and aggregation functions.

    Returns:
    DataFrame: The aggregated dataset.
    """
    return data.groupby(groupby_column).agg(agg_dict).reset_index()


def summarize(data):
    """
    Provide summary statistics of the dataset.

    Parameters:
    data (DataFrame): The dataset to summarize.

    Returns:
    DataFrame: The summary statistics.
    """
    return data.describe()


def extract_features(data, text_column, max_features=100):
    """
    Extract TF-IDF features from a text column.

    Parameters:
    data (DataFrame): The dataset containing the text column.
    text_column (str): The name of the text column.
    max_features (int): The maximum number of features to extract.

    Returns:
    DataFrame: The dataset with added TF-IDF features.
    """
    tfidf = TfidfVectorizer(max_features=max_features)
    tfidf_matrix = tfidf.fit_transform(data[text_column].fillna(''))
    tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=tfidf.get_feature_names_out(), index=data.index)

    return pd.concat([data, tfidf_df], axis=1)
