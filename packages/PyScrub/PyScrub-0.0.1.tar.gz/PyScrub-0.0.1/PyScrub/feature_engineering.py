# feature_engineering/feature_engineering.py

import pandas as pd
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.stats import boxcox

def create_polynomial_features(data, degree=2):
    """
    Create polynomial features for numerical columns in the dataset.

    Parameters:
    data (DataFrame): The dataset with numerical features.
    degree (int): The degree of the polynomial features.

    Returns:
    DataFrame: The dataset with added polynomial features.
    """
    poly = PolynomialFeatures(degree)
    poly_features = poly.fit_transform(data)
    feature_names = poly.get_feature_names_out(data.columns)  # Ensure correct feature names
    return pd.DataFrame(poly_features, columns=feature_names, index=data.index)

def create_interaction_features(data):
    """
    Create interaction features by multiplying pairs of features.

    Parameters:
    data (DataFrame): The dataset with numerical features.

    Returns:
    DataFrame: The dataset with added interaction features.
    """
    interaction_features = pd.DataFrame()
    for i in range(len(data.columns)):
        for j in range(i + 1, len(data.columns)):
            interaction_features[f'{data.columns[i]}_x_{data.columns[j]}'] = data.iloc[:, i] * data.iloc[:, j]
    return interaction_features

def log_transform(data):
    """
    Apply log transformation to numerical features in the dataset.

    Parameters:
    data (DataFrame): The dataset with numerical features.

    Returns:
    DataFrame: The dataset with log-transformed features.
    """
    return data.apply(lambda x: np.log1p(x) if np.issubdtype(x.dtype, np.number) else x)

def boxcox_transform(data):
    """
    Apply Box-Cox transformation to numerical features in the dataset.

    Parameters:
    data (DataFrame): The dataset with numerical features.

    Returns:
    DataFrame: The dataset with Box-Cox transformed features.
    """
    transformed_data = data.apply(lambda x: boxcox(x + 1)[0] if np.issubdtype(x.dtype, np.number) else x)
    return transformed_data

def apply_pca(data, n_components=2):
    """
    Apply Principal Component Analysis (PCA) for dimensionality reduction.

    Parameters:
    data (DataFrame): The dataset with numerical features.
    n_components (int): The number of principal components to extract.

    Returns:
    DataFrame: The dataset with principal components.
    """
    pca = PCA(n_components=n_components)
    principal_components = pca.fit_transform(data)
    return pd.DataFrame(principal_components, columns=[f'PC{i + 1}' for i in range(n_components)])

def select_best_features(data, labels, k=10):
    """
    Select the best features using ANOVA F-test.

    Parameters:
    data (DataFrame): The dataset with numerical features.
    labels (array-like): The target variable for supervised learning.
    k (int): The number of top features to select.

    Returns:
    DataFrame: The dataset with the best k features.
    """
    selector = SelectKBest(score_func=f_classif, k=k)
    selected_data = selector.fit_transform(data, labels)
    selected_columns = data.columns[selector.get_support(indices=True)]
    return pd.DataFrame(selected_data, columns=selected_columns)

def bin_features(data, column, bins, labels):
    """
    Bin a numerical feature into discrete intervals.

    Parameters:
    data (DataFrame): The dataset with numerical features.
    column (str): The name of the column to bin.
    bins (list): The bin edges.
    labels (list): The labels for the bins.

    Returns:
    DataFrame: The dataset with the binned feature.
    """
    data[f'{column}_binned'] = pd.cut(data[column], bins=bins, labels=labels)
    return data

def create_tfidf_features(text_data, max_features=1000):
    """
    Create TF-IDF features from text data.

    Parameters:
    text_data (Series): The text data to transform.
    max_features (int): The maximum number of features to extract.

    Returns:
    DataFrame: The dataset with TF-IDF features.
    """
    vectorizer = TfidfVectorizer(max_features=max_features)
    tfidf_matrix = vectorizer.fit_transform(text_data)
    return pd.DataFrame(tfidf_matrix.toarray(), columns=vectorizer.get_feature_names_out())

def create_time_series_features(data, lag=1):
    """
    Create lag features for time series data.

    Parameters:
    data (Series): The time series data.
    lag (int): The number of lag features to create.

    Returns:
    DataFrame: The dataset with lag features.
    """
    time_series_data = pd.DataFrame()
    for i in range(1, lag + 1):
        time_series_data[f'lag_{i}'] = data.shift(i)
    return time_series_data.fillna(0)  # Replace NaN values with 0 for the first few rows
