import pandas as pd

def load_csv(filename, delimiter, encoding, index_col):
    return pd.read_csv(filename, delimiter = delimiter, encoding = encoding, index_col = index_col)

data_df = load_csv("PEATONES_2020_mod.csv", ";", "ISO-8859-1", 2)

print(f"VALORES ERRONEOS")
print(f"La siguiente tabla muestra los valores NaN dentro de cada columna en el DF")
print(f"{data_df.isna().sum()}")

print(f"MEDIA DE PEATONES")
print(f"La media es: {data_df['PEATONES'].mean()}")

print(f"RANGO DE FECHAS")
print(f"El rango de fechas va del {data_df['FECHA'].min()} al {data_df['FECHA'].max()}")

print(f"SUMA ACUMULADA")
data_df['PEATONES_cumsum'] = data_df['PEATONES'].cumsum()
print(data_df[['PEATONES', 'PEATONES_cumsum']])