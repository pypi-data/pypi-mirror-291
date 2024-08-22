"""
PyScrub Visualization Module

This module contains all functions related to data visualization for PyScrub.
"""

# visualization.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from PyScrub import data_profiler
from sklearn.metrics import confusion_matrix, roc_curve, auc
from sklearn.utils.multiclass import unique_labels

sns.set(style="whitegrid")


def plot_missing(data):
    """
    Visualizes missing values in the dataset using a heatmap.
    """
    if data is None:
        raise ValueError("Expected a DataFrame, got 'None'")

    plt.figure(figsize=(12, 8))
    sns.heatmap(data.isnull(), cbar=True, cmap='viridis')
    plt.title("Missing Values Heatmap")
    plt.show()


def countplot(data, features=None, separate_by=None, fig_size=(6, 6), save_fig=False):
    """
    Creates bar plots for categorical features to display their counts.
    """
    if data is None:
        raise ValueError("Expected a DataFrame, got 'None'")

    if features is None:
        features = data_profiler.get_cat_feats(data)

    for feature in features:
        if len(data[feature].unique()) <= 30:
            plt.figure(figsize=fig_size)
            sns.countplot(x=feature, hue=separate_by, data=data)
            plt.xticks(rotation=90)
            plt.title(f"Count plot for {feature}")
            if save_fig:
                plt.savefig(f'Countplot_{feature}.png')
            plt.show()


def boxplot(data, num_features=None, target=None, fig_size=(8, 8), large_data=False, save_fig=False):
    """
    Creates box plots for numerical features against a specified categorical target column.
    If target is None, it will plot box plots for the numerical features individually.
    """
    if data is None:
        raise ValueError("Data cannot be None")
    
    if num_features is None:
        # Automatically detect numerical features
        num_features = data_profiler.get_num_feats(data)
    
    if target is None:
        # If no target is provided, plot the box plots for each numerical feature individually
        for feature in num_features:
            plt.figure(figsize=fig_size)
            sns.boxplot(data=data[feature])
            plt.title(f"Box plot of {feature}")
            if save_fig:
                plt.savefig(f'Boxplot_{feature}.png')
            plt.show()
    else:
        # Ensure that the target column has 10 or fewer unique categories
        if len(data[target].unique()) > 10:
            raise ValueError("Target categories must be 10 or fewer")
        
        plot_func = sns.boxenplot if large_data else sns.boxplot
        for feature in num_features:
            plt.figure(figsize=fig_size)
            plot_func(x=target, y=feature, data=data)
            plt.xticks(rotation=90)
            plt.title(f"Box plot of {feature} vs. {target}")
            if save_fig:
                plt.savefig(f'Boxplot_{feature}_vs_{target}.png')
            plt.show()



def violinplot(data, num_features=None, target=None, fig_size=(6, 6), save_fig=False):
    """
    Creates violin plots for numerical features against a specified categorical target column.
    """
    if data is None or target is None:
        raise ValueError("Data and target cannot be None")

    if len(data[target].unique()) > 10:
        raise ValueError("Target categories must be 10 or fewer")

    if num_features is None:
        num_features = data_profiler.get_num_feats(data)

    for feature in num_features:
        plt.figure(figsize=fig_size)
        sns.violinplot(x=target, y=feature, data=data)
        plt.xticks(rotation=90)
        plt.title(f"Violin plot of {feature} vs. {target}")
        if save_fig:
            plt.savefig(f'Violinplot_{feature}_vs_{target}.png')
        plt.show()


def histogram(data, num_features=None, bins=10, fig_size=(8, 8), save_fig=False):
    """
    Creates histogram plots for numerical features.
    """
    if data is None:
        raise ValueError("Expected a DataFrame, got 'None'")

    if num_features is None:
        num_features = data_profiler.get_num_feats(data)

    for feature in num_features:
        plt.figure(figsize=fig_size)
        sns.histplot(data[feature], bins=bins, kde=True)
        plt.title(f"Histogram of {feature}")
        if save_fig:
            plt.savefig(f'Histogram_{feature}.png')
        plt.show()


def scatterplot(data, num_features=None, target=None, separate_by=None, fig_size=(10, 10), save_fig=False):
    """
    Creates scatter plots of numerical features against a numerical target.
    """
    if data is None or target is None:
        raise ValueError("Data and target cannot be None")

    if num_features is None:
        num_features = data_profiler.get_num_feats(data)

    for feature in num_features:
        plt.figure(figsize=fig_size)
        sns.scatterplot(x=feature, y=target, hue=separate_by, data=data)
        plt.title(f"Scatter plot of {feature} vs. {target} separated by {separate_by}")
        if save_fig:
            plt.savefig(f'Scatterplot_{feature}_vs_{target}.png')
        plt.show()

def plot_confusion_matrix(y_true, y_pred, classes, normalize=False, cmap=plt.cm.Blues):
    """
    Prints and plots the confusion matrix.
    """
    cm = confusion_matrix(y_true, y_pred)
    classes = classes[unique_labels(y_true, y_pred)]
    cm_norm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis] if normalize else cm

    plt.figure(figsize=(10, 7))
    sns.heatmap(cm_norm, annot=True, fmt=".2f" if normalize else "d", cmap=cmap, xticklabels=classes,
                yticklabels=classes)
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.title('Normalized Confusion Matrix' if normalize else 'Confusion Matrix')
    plt.show()

def plot_auc(labels, predictions):
    """
    Computes and plots the ROC curve and AUC.
    """
    fpr, tpr, _ = roc_curve(labels, predictions)
    roc_auc = auc(fpr, tpr)

    plt.figure(figsize=(10, 7))
    plt.plot(fpr, tpr, color='orange', lw=2, label=f'AUC = {roc_auc:.2f}')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic')
    plt.legend(loc='lower right')
    plt.show()

def autoviz(data):
    """
    Automatically visualize a dataset using AutoViz.
    """
    import importlib.util
    package_name = 'autoviz'
    if importlib.util.find_spec(package_name) is None:
        raise ImportError(f"{package_name} is not installed. Install using 'pip install autoviz'.")

    from autoviz.AutoViz_Class import AutoViz_Class  # type: ignore
    AV = AutoViz_Class()
    AV.AutoViz(filename='', dfte=data, max_cols_analyzed=50)
