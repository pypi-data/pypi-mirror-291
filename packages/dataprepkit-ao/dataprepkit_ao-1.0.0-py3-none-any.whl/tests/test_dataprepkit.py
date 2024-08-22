import os
import unittest
import pandas as pd
import numpy as np
from dataprepkit.data_prep_kit import DataPrepKit

class TestDataPrepKit(unittest.TestCase):
    """
    A suite of tests to validate the functionality of the DataPrepKit class.
    
    These tests cover data loading, summary generation, encoding, scaling,
    imputation, and dropping of data within a Pandas DataFrame. 
    """

    def setUp(self):
        """Setup method to create a test DataFrame before each test."""
        data = {
            'EmployeeID': [101, 102, 103, 104, 104, 105, 106, 104],  # Contains duplicates
            'Name': ['Alice', 'Bob', 'Charlie', 'David', 'David', 'Eve', 'Frank', 'David'], # Contains duplicates
            'Salary': [70000, 80000, 90000, 100000, 100000, 110000, 120000, 100000], # Contains duplicates
            'Department': ['HR', 'IT', 'Finance', 'IT', 'IT', 'Marketing', 'IT', 'IT'] # Contains duplicates
        }
        self.df = pd.DataFrame(data)
        self.data_prep = DataPrepKit(data=self.df)

    def test_read_data(self):
        """Verify that the read_data method can load data from a CSV file."""
        self.df.to_csv('test_data.csv', index=False)
        self.data_prep.read_data('test_data.csv', 'csv')
        self.assertIsInstance(self.data_prep.data, pd.DataFrame, "Data should be a Pandas DataFrame")
        os.remove('test_data.csv') 

    def test_data_summary(self):
        """Check if the data_summary method executes without errors."""
        try:
            self.data_prep.data_summary()
        except Exception as e:
            self.fail(f"data_summary() raised an exception: {str(e)}")

    def test_encode_categorical_label(self):
        """Test that label encoding converts a column to integer data type."""
        self.data_prep.encode_categorical(columns=['Name'], method='label')
        self.assertTrue(pd.api.types.is_integer_dtype(self.data_prep.data['Name']), "Name column should be encoded as integers")

    def test_encode_categorical_one_hot(self):
        """Test one-hot encoding by checking for the presence of new columns."""
        self.data_prep.encode_categorical(columns=['Department'], method='one-hot')
        self.assertIn('Department_HR', self.data_prep.data.columns, "Missing one-hot encoded column: Department_HR")
        self.assertIn('Department_IT', self.data_prep.data.columns, "Missing one-hot encoded column: Department_IT")
        self.assertIn('Department_Finance', self.data_prep.data.columns, "Missing one-hot encoded column: Department_Finance")
        self.assertIn('Department_Marketing', self.data_prep.data.columns, "Missing one-hot encoded column: Department_Marketing")

    def test_drop_duplicates(self):
        """Ensure that the drop_duplicates method removes duplicate rows."""
        initial_length = len(self.data_prep.data)
        self.data_prep.drop_duplicates()
        final_length = len(self.data_prep.data)
        self.assertLessEqual(final_length, initial_length, "Number of rows should not increase after dropping duplicates.")
        self.assertEqual(len(self.data_prep.data), len(self.data_prep.data.drop_duplicates()), "Duplicate rows are still present.")

    def test_scale_data(self):
        """
        Verify the min-max scaling by ensuring values fall within 0 and 1.
        This test includes introducing a missing value and imputing it before scaling.
        """
        self.data_prep.data.loc[0, 'Salary'] = np.nan
        self.data_prep.impute_data(columns=['Salary'], method='mean')
        self.data_prep.scale_data(columns=['Salary'], method='min-max')
        salary_max = self.data_prep.data['Salary'].max()
        salary_min = self.data_prep.data['Salary'].min()
        self.assertTrue(salary_max <= 1, f"Maximum salary value after min-max scaling should be <= 1. Found: {salary_max}")
        self.assertTrue(salary_min >= 0, f"Minimum salary value after min-max scaling should be >= 0. Found: {salary_min}")

    def test_impute_data_mean(self):
        """Check mean imputation by inserting a missing value and verifying it's filled."""
        self.data_prep.data.loc[0, 'Salary'] = np.nan
        self.data_prep.impute_data(columns=['Salary'], method='mean')
        self.assertFalse(self.data_prep.data['Salary'].isnull().any(), "Missing values should be imputed with the mean.")

    def test_impute_data_knn(self):
        """Check KNN imputation by introducing a missing value and verifying it's filled."""
        self.data_prep.data.loc[0, 'Salary'] = np.nan
        self.data_prep.impute_data(columns=['Salary'], method='knn')
        self.assertFalse(self.data_prep.data['Salary'].isnull().any(), "Missing values should be imputed using KNN.")

    def test_drop_columns(self):
        """Confirm that dropping columns removes the specified column from the DataFrame."""
        self.data_prep.drop(columns=['EmployeeID'])
        self.assertNotIn('EmployeeID', self.data_prep.data.columns, "The 'EmployeeID' column should be dropped.")

    def test_drop_rows(self):
        """Confirm that specified rows are no longer present in the DataFrame."""
        self.data_prep.drop(rows=[0, 1])
        self.assertNotIn(0, self.data_prep.data.index, "Row 0 should be dropped.")
        self.assertNotIn(1, self.data_prep.data.index, "Row 1 should be dropped.")

if __name__ == '__main__':
    unittest.main()
    