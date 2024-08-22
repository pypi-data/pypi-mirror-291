# DataPrepKit_AO_v1.0

`DataPrepKit_AO_v1.0` is a Python library designed for efficient data preprocessing. It provides a comprehensive set of tools to clean, transform, and prepare your data for machine learning or analysis. This kit allows you to understand your dataset better and get it ready for modeling.

## Features

- **Data Summary (`data_summary`)**:  Get a detailed overview of your dataset:
    - Shape (rows, columns)
    - Missing value counts per column
    - Unique value counts per column
    - Descriptive statistics (mean, median, mode, standard deviation, minimum, maximum) for numerical columns
    - Value counts for non-numerical columns
- **Encoding Categorical Features (`encode_categorical`):**
    - **Label Encoding:** Convert categorical values into numerical labels.
    - **Ordinal Encoding:**  Encode categories in a specific order (if an order is inherent in your data).
    - **One-Hot Encoding:** Create dummy variables for each category.
- **Scaling Numerical Features (`scale_data`):**
    - **Standard Scaling:** Center data around mean 0 with standard deviation 1.
    - **Min-Max Scaling:** Rescale features to a range of 0 to 1. 
    - **Robust Scaling:** Scaling less affected by outliers, using median and IQR.
    - **Normalization:** Scale each sample (row) to have unit norm (length of 1). 
- **Imputation of Missing Values (`impute_data`):**
    - **Dropping Missing Values:** Remove rows with missing values.
    - **Mean/Median/Most Frequent Imputation:** Fill missing values using central tendency measures.
    - **Constant Value Imputation:** Fill with a user-specified constant. 
    - **K-Nearest Neighbors (KNN) Imputation:** Use the values of nearest neighbors to fill in missing data.
    - **Iterative Imputation:** A more advanced method that models each feature with missing values as a function of other features.
- **Dropping Rows and Columns (`drop`):** Remove specified rows or columns from your DataFrame.

## Installation

```bash
pip install pandas numpy scikit-learn
```

## Usage

```python
import pandas as pd
from dataprepkit.data_prep_kit import DataPrepKit

# Load data
data = pd.read_csv('your_data.csv') 
data_prep = DataPrepKit(data=data)

# Data understanding
data_prep.data_summary()

# Encoding 
data_prep.encode_categorical(columns=['your_categorical_column'], method='one-hot')

# Scaling
data_prep.scale_data(columns=['your_numerical_column'], method='standard')

# Imputation
data_prep.impute_data(columns=['column_with_missing_values'], method='mean')

# Dropping data
data_prep.drop(columns=['unwanted_column'])
data_prep.drop(rows=[0, 5]) # Drop specific rows 

# Access the processed data
processed_df = data_prep.data
```

## Error Handling

The library includes checks for:
- Missing columns:  `KeyError` is raised if you try to operate on columns not in your DataFrame.
- Invalid method names: `ValueError` if you specify an incorrect encoding, scaling, or imputation method. 

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

For any questions, please contact [abdalrahman.osama01@gmail.com](mailto:abdalrahman.osama01@gmail.com). 