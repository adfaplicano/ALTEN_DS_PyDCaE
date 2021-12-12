import pandas as pd
import numpy as np

def load_csv(filename, delimiter, encoding):
    return pd.read_csv(filename, delimiter = delimiter, encoding = encoding)

data_df = load_csv("iris_dataset.csv", ",", "ISO-8859-1")
data_df['area_sépalo'] = data_df['longitud_sépalo'] * data_df[' anchura_sépalo'] * np.pi
data_df['area_pétalo'] = data_df['longitud_pétalo'] * data_df['anchura_pétalo'] * np.pi


print(f"¿Cuál es la mediana del área del pétalo?")
print(f"La mediana es {data_df['area_pétalo'].median()}")

print(f"¿Qué valor de área solo es superado por el 10 % de los pétalos?")
print(f"El valor de área {data_df['area_pétalo'].quantile(0.9)}")

print(f"¿Existe correlación entre la longitud y anchura del pétalo?")
print(f"{data_df.corr()}")