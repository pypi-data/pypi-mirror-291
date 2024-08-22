# data_cleaning/data_cleaning.py

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler

def handle_missing_values(data, method='mean'):
    ''' Impute or remove missing values '''
    if method == 'mean':
        # Apply mean only to numeric columns
        numeric_data = data.select_dtypes(include=[np.number])
        data[numeric_data.columns] = numeric_data.fillna(numeric_data.mean())
        return data
    elif method == 'median':
        numeric_data = data.select_dtypes(include=[np.number])
        data[numeric_data.columns] = numeric_data.fillna(numeric_data.median())
        return data
    elif method == 'mode':
        return data.fillna(data.mode().iloc[0])
    elif method == 'ffill':
        return data.fillna(method='ffill')
    elif method == 'bfill':
        return data.fillna(method='bfill')
    elif method == 'drop':
        return data.dropna()
    else:
        raise ValueError("Method should be 'mean', 'median', 'mode', 'ffill', 'bfill', or 'drop'")

def remove_duplicates(data):
    ''' Remove duplicate rows '''
    return data.drop_duplicates()

def detect_outliers(data, method='zscore', threshold=3):
    ''' Detect outliers in the dataset '''
    if method == 'zscore':
        z_scores = np.abs((data - data.mean()) / data.std())
        return data[(z_scores > threshold).any(axis=1)]
    elif method == 'iqr':
        Q1 = data.quantile(0.25)
        Q3 = data.quantile(0.75)
        IQR = Q3 - Q1
        return data[((data < (Q1 - 1.5 * IQR)) | (data > (Q3 + 1.5 * IQR))).any(axis=1)]
    else:
        raise ValueError("Method should be 'zscore' or 'iqr'")

def treat_outliers(data, method='zscore', threshold=3, treatment='remove'):
    ''' Treat outliers in the dataset '''
    if method == 'zscore':
        z_scores = np.abs((data - data.mean()) / data.std())
        if treatment == 'remove':
            return data[(z_scores < threshold).all(axis=1)]
        elif treatment == 'cap':
            capped_data = data.copy()
            capped_data[z_scores > threshold] = np.sign(data) * threshold
            return capped_data
    elif method == 'iqr':
        Q1 = data.quantile(0.25)
        Q3 = data.quantile(0.75)
        IQR = Q3 - Q1
        if treatment == 'remove':
            return data[((data >= (Q1 - 1.5 * IQR)) & (data <= (Q3 + 1.5 * IQR))).all(axis=1)]
        elif treatment == 'cap':
            capped_data = data.copy()
            capped_data[data < (Q1 - 1.5 * IQR)] = Q1 - 1.5 * IQR
            capped_data[data > (Q3 + 1.5 * IQR)] = Q3 + 1.5 * IQR
            return capped_data
    else:
        raise ValueError("Method should be 'zscore' or 'iqr' and treatment should be 'remove' or 'cap'")

def correct_data_types(data):
    ''' Convert data to appropriate types with a check for potential date columns '''
    for col in data.columns:
        # Check if the column is numeric or can be converted to numeric
        if data[col].dtype == 'object':
            try:
                # First attempt to convert to numeric
                data[col] = pd.to_numeric(data[col])
            except ValueError:
                # Then try to convert to datetime if it looks like a date column
                try:
                    # Adding a more conservative check for date-like strings
                    if any(data[col].str.match(r'\d{4}-\d{2}-\d{2}') | data[col].str.match(r'\d{2}/\d{2}/\d{4}')):
                        data[col] = pd.to_datetime(data[col], errors='raise')
                except ValueError:
                    pass  # If it's not numeric or date-like, keep it as an object (string)
        elif data[col].dtype == 'int64' or data[col].dtype == 'float64':
            data[col] = pd.to_numeric(data[col])
    
    return data

def clean_strings(data):
    ''' Clean string columns '''
    for col in data.select_dtypes(include=['object']).columns:
        data[col] = data[col].str.strip().str.lower().str.replace('[^a-zA-Z0-9 ]', '')
    return data

def handle_inconsistent_data(data, column, mappings):
    ''' Standardize categorical values '''
    data[column] = data[column].replace(mappings)
    return data

def handle_invalid_data(data, column, valid_values):
    ''' Identify and correct invalid data entries '''
    data.loc[~data[column].isin(valid_values), column] = np.nan
    return data

# Strip Whitespace Function
def strip_whitespace(data, columns=None):
    """
    Strips leading and trailing whitespace from all string columns in the DataFrame.
    Also replaces multiple spaces with a single space.

    Parameters:
    - data: pandas DataFrame
    - columns: list or None, specify particular columns to clean, if None, cleans all string columns.
    """
    # If no specific columns are provided, operate on all string columns
    if columns is None:
        columns = data.select_dtypes(include=['object']).columns
    
    # Strip whitespace from the specified columns
    for column in columns:
        if column in data.columns and pd.api.types.is_string_dtype(data[column]):
            data[column] = data[column].str.strip().str.replace(r'\s+', ' ', regex=True)
    
    return data
