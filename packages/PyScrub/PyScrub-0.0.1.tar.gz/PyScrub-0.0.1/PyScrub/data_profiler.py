"""
data_profiler.py

This module contains functions for profiling, summarizing, and exploring structured datasets.
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


def describe(data=None, name='', show_categories=False, plot_missing=False):
    """
    Provides a summary of the dataset, including shape, data types, and basic statistics.

    Parameters:
    - data (pd.DataFrame): The dataset to describe.
    - name (str): Optional dataset name for display.
    - show_categories (bool): Display unique values for categorical features.
    - plot_missing (bool): Plot a heatmap of missing values.
    """
    if data is None:
        raise ValueError("Expected a DataFrame, got 'None'")

    print(f"Summary of {name} Dataset")
    print(f"Shape: {data.shape}")
    print(f"Size: {data.size}")
    print(f"\nData Types:\n{data.dtypes}")

    num_features = data.select_dtypes(include=[np.number]).columns
    cat_features = data.select_dtypes(include=['object']).columns

    print("\nNumerical Features:", list(num_features))
    print("\nCategorical Features:", list(cat_features))

    print("\nStatistics for Numerical Columns:")
    print(data.describe())

    if show_categories and not cat_features.empty:
        print("\nUnique Value Counts for Categorical Features:")
        for col in cat_features:
            print(f"\n{col}:")
            print(data[col].value_counts())

    if plot_missing:
        plot_missing_values(data)


def plot_missing_values(data=None):
    """Plots a heatmap of missing values in the dataset."""
    if data is None:
        raise ValueError("Expected a DataFrame, got 'None'")

    if data.isnull().sum().sum() > 0:
        plt.figure(figsize=(10, 6))
        sns.heatmap(data.isnull(), cmap='viridis', cbar=False)
        plt.title("Missing Values Heatmap")
        plt.show()
    else:
        print("No missing values found.")


def get_cat_feats(data=None):
    """Returns a list of categorical features in the dataset."""
    if data is None:
        raise ValueError("Expected a DataFrame, got 'None'")
    return list(data.select_dtypes(include=['object']).columns)


def get_num_feats(data=None):
    """Returns a list of numerical features in the dataset."""
    if data is None:
        raise ValueError("Expected a DataFrame, got 'None'")
    return list(data.select_dtypes(include=[np.number]).columns)


def get_unique_counts(data=None):
    """Returns a DataFrame with unique value counts of categorical features."""
    if data is None:
        raise ValueError("Expected a DataFrame, got 'None'")
    
    cat_feats = get_cat_feats(data)
    unique_counts = {col: data[col].nunique() for col in cat_feats}
    return pd.DataFrame(list(unique_counts.items()), columns=['Feature', 'Unique Count'])


def display_missing(data=None):
    """Displays a DataFrame of missing values and their percentage in each column."""
    if data is None:
        raise ValueError("Expected a DataFrame, got 'None'")

    missing = data.isnull().sum()
    missing_percent = (missing / len(data)) * 100
    return pd.DataFrame({'Missing Count': missing, 'Missing Percent': missing_percent})


def detect_outliers(data=None, features=None, threshold=1.5):
    """
    Detects rows with outliers using the IQR method.

    Parameters:
    - data (pd.DataFrame): Dataset to check for outliers.
    - features (list): List of numerical columns to check.
    - threshold (float): Multiplier for the IQR to detect outliers (default is 1.5).

    Returns:
    - List of row indices containing outliers.
    """
    if data is None or features is None:
        raise ValueError("Expected a DataFrame and feature list")

    outlier_indices = []
    for col in features:
        Q1 = data[col].quantile(0.25)
        Q3 = data[col].quantile(0.75)
        IQR = Q3 - Q1
        outliers = data[(data[col] < Q1 - threshold * IQR) | (data[col] > Q3 + threshold * IQR)].index
        outlier_indices.extend(outliers)

    return list(set(outlier_indices))


def plot_categorical_distribution(data=None, column=None, hue=None):
    """
    Plots the distribution of a categorical column.

    Parameters:
    - data (pd.DataFrame): Dataset to plot.
    - column (str): Column to visualize.
    - hue (str): Optional column for grouping.
    """
    if data is None or column is None:
        raise ValueError("Expected a DataFrame and column to plot")
    
    sns.countplot(x=column, hue=hue, data=data, palette='Set1')
    plt.title(f"Distribution of {column}")
    plt.show()
