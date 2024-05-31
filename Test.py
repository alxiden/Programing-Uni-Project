import pandas as pd

# Specify the file path of the dataset
file_path = "/c:/Users/danie/OneDrive - University of Gloucestershire/Year 1/CT4029/Assignment/Test.csv"

# Read the dataset into a pandas DataFrame
df = pd.read_csv(file_path)

# Print the first few rows of the DataFrame
print(df.head())