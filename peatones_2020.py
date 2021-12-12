import pandas as pd

def load_csv(filename, delimiter, encoding, index_col, nrows):
    return pd.read_csv(filename, delimiter = delimiter, encoding = encoding, index_col = index_col, nrows=nrows)

data_df = load_csv("PEATONES_2020.csv", ";", "ISO-8859-1", 2, 10000)
print(data_df.head())
