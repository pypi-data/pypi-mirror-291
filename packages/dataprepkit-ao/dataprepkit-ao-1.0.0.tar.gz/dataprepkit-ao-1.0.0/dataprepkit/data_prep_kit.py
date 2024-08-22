from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import SimpleImputer, KNNImputer, IterativeImputer
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, OrdinalEncoder, StandardScaler, MinMaxScaler, RobustScaler, Normalizer
import pandas as pd
import numpy as np

class DataPrepKit:
    """
    A toolkit for common data preprocessing tasks in machine learning.

    This class simplifies data loading, exploration, cleaning, transformation, 
    and preparation for use in machine learning models.
    """
    def __init__(self, data=None, file_path=None, file_type='csv'):
        """
        Initializes DataPrepKit with either a DataFrame or data from a file.

        Args:
            data (pd.DataFrame, optional): The input DataFrame. Defaults to None.
            file_path (str, optional): Path to the data file. Defaults to None.
            file_type (str, optional): Type of data file ('csv', 'excel', 'json'). 
                                        Defaults to 'csv'.

        Raises:
            ValueError: If an unsupported file type is provided.
        """
        if data is not None:
            self.data = data
        elif file_path is not None:
            self.read_data(file_path, file_type)

    def read_data(self, file_path, file_type):
        """
        Reads data from a file and stores it in the 'data' attribute.

        Args:
            file_path (str): The path to the data file.
            file_type (str): The type of the data file ('csv', 'excel', 'json').

        Raises:
            ValueError: If an unsupported file type is provided.
        """
        if file_type == "csv":
            self.data = pd.read_csv(file_path)
        elif file_type == "excel":
            self.data = pd.read_excel(file_path)
        elif file_type == "json":
            self.data = pd.read_json(file_path)
        else:
            raise ValueError("Unsupported file type. Please provide a CSV, Excel, or JSON file.")
        
    def data_summary(self, include_missing=True, include_unique=True, include_stats=True):
        """
        Prints a comprehensive summary of the DataFrame.

        The summary includes:
            - Shape (rows, columns)
            - Missing value counts per column
            - Unique value counts per column
            - Column statistics (mean, median, mode, std, min, max) for numerical columns
            - Value counts for non-numerical columns

        Args:
            include_missing (bool, optional): Whether to include missing value counts. 
                                            Defaults to True.
            include_unique (bool, optional): Whether to include unique value counts. 
                                            Defaults to True.
            include_stats (bool, optional): Whether to include column statistics. 
                                            Defaults to True.
        """
        print("Data Summary")
        print("=" * 30)
        print(f"Shape: {self.data.shape}")
        
        if include_missing:
            print("\nMissing Values:")
            print(self.data.isnull().sum())

        if include_unique:
            print("\nUnique Values:")
            print(self.data.nunique())

        if include_stats:
            print("\nColumn Statistics:")
            for col in self.data.columns:
                if pd.api.types.is_numeric_dtype(self.data[col]) and self.data[col].dtype != bool: 
                    print(f"\nColumn: {col}")
                    print(f"  Mean: {self.data[col].mean():.2f}")
                    print(f"  Median: {self.data[col].median():.2f}")
                    mode = self.data[col].mode()
                    if not mode.empty:
                        print(f"  Mode: {mode[0]:.2f}")
                    print(f"  Standard Deviation: {self.data[col].std():.2f}")
                    print(f"  Minimum Value: {self.data[col].min():.2f}")
                    print(f"  Maximum Value: {self.data[col].max():.2f}")
                else:
                    print(f"\nColumn: {col}")
                    mode = self.data[col].mode()
                    if not mode.empty:
                        print(f"  Most Frequent Value: {mode[0]}")
                    print(f"  Value Counts:")
                    for value, count in self.data[col].value_counts().items():
                        print(f"    {value}: {count}")
                        
    def encode_categorical(self, columns, method):
        """
        Encodes categorical columns using the specified method.

        Args:
            columns (list): A list of column names to encode.
            method (str): The encoding method ('label', 'ordinal', 'one-hot').

        Raises:
            KeyError: If any specified column is not found in the DataFrame.
            ValueError: If an invalid encoding method is provided.
        """
        if not set(columns).issubset(self.data.columns):
            raise KeyError(f"The following columns are missing from the DataFrame: {', '.join(columns)}")
        if method == "label":
            encoder = LabelEncoder()
            for column in columns:
                self.data[column] = encoder.fit_transform(self.data[column]).astype('int64')
        elif method == "ordinal":
            encoder = OrdinalEncoder()
            self.data[columns] = encoder.fit_transform(self.data[columns])
        elif method == "one-hot":
            encoder = OneHotEncoder(sparse_output=False)
            encoded_data = encoder.fit_transform(self.data[columns])
            encoded_df = pd.DataFrame(encoded_data, columns=encoder.get_feature_names_out(columns))
            self.data = pd.concat([self.data.drop(columns, axis=1), encoded_df], axis=1)
        else:
            raise ValueError("The encoding method specified is not valid. Please choose from 'label', 'ordinal', or 'one-hot'.")
            
    def drop_duplicates(self):
        """
        Drops duplicate rows from the DataFrame (in-place).
        """
        self.data.drop_duplicates(inplace=True)

    def scale_data(self, columns, method):
        """
        Scales numerical columns using the specified method.

        Args:
            columns (list): A list of numerical column names to scale.
            method (str): The scaling method ('standard', 'min-max', 'robust', 'normalizer').

        Raises:
            KeyError: If any specified column is missing from the DataFrame.
            ValueError: If an invalid scaling method is provided or if missing values 
                        are present in the columns to be scaled. 
        """
        if not set(columns).issubset(self.data.columns):
            raise KeyError(f"The following columns are missing from the DataFrame: {', '.join(columns)}")

        if self.data[columns].isnull().values.any():
            raise ValueError("Missing values present in scaling columns. Impute them first.")

        if method == "standard":
            scaler = StandardScaler()
        elif method == "min-max":
            scaler = MinMaxScaler()
        elif method == "robust":
            scaler = RobustScaler()
        elif method == "normalizer":
            scaler = Normalizer()
        else:
            raise ValueError("The scaling method provided is not recognized. Please choose from 'standard', 'min-max', 'robust', or 'normalizer'.")

        self.data[columns] = scaler.fit_transform(self.data[columns])
            
    def impute_data(self, columns=None, method='mean', fill_value=None):
        """
        Imputes missing values in specified or numerical columns.

        Args:
            columns (list, optional): List of columns to impute. If None, imputes all 
                                     numerical columns. Defaults to None.
            method (str, optional): Imputation method ('dropna', 'mean', 'median', 
                                    'most-frequent', 'constant', 'knn', 'iterative').
                                    Defaults to 'mean'.
            fill_value (int/float, optional): Value to use for 'constant' imputation. 
                                            Defaults to None.

        Raises:
            ValueError: 
                - If an invalid imputation method is provided.
                - If 'constant' imputation is selected and 'fill_value' is not provided. 
        """
        imputer = None
        if columns is None:
            columns = self.data.select_dtypes(include=[np.number]).columns

        if method == "dropna":
            self.data.dropna(subset=columns, inplace=True)
        elif method == "mean":
            imputer = SimpleImputer(strategy="mean")
        elif method == "median":
            imputer = SimpleImputer(strategy="median")
        elif method == "most-frequent":
            imputer = SimpleImputer(strategy="most_frequent")
        elif method == "constant":
            if fill_value is None:
                raise ValueError("fill_value must be specified for constant imputation.")
            imputer = SimpleImputer(strategy="constant", fill_value=fill_value)
        elif method == "knn":
            imputer = KNNImputer()
        elif method == "iterative":
            imputer = IterativeImputer()
        else:
            raise ValueError(f"Invalid imputation method '{method}'. Please choose from 'dropna', 'mean', 'median', 'most-frequent', 'constant', 'knn', or 'iterative'.")

        if imputer is not None:
            self.data[columns] = imputer.fit_transform(self.data[columns])
            
    def drop(self, rows=None, columns=None):
        """
        Drops specified rows or columns from the DataFrame.

        Args:
            rows (list, optional): List of row indices to drop. Defaults to None.
            columns (list, optional): List of column names to drop. Defaults to None.

        Raises:
            KeyError: If any specified column is not found in the DataFrame.
        """
        if rows is not None:
            if not set(rows).issubset(self.data.index):
                print(f"Warning: The following rows are not present in the DataFrame: {', '.join(map(str, rows))}") 
            else:
                self.data.drop(rows, inplace=True)
        
        if columns is not None:
            if not set(columns).issubset(self.data.columns):
                raise KeyError(f"The following columns are not present in the DataFrame: {', '.join(columns)}")
            self.data.drop(columns, axis=1, inplace=True)