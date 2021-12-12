import pandas as pd
import requests

url = "https://www.worldometers.info/gdp/gdp-by-country/"

## Obteniendo la respuesta
r = requests.get(url)       ## Obteniendo lista de dataframes de la página
df_lista = pd.read_html(r.text)     ## Dataframes leídos
df = df_lista[0]

## Obteniendo los dataframes correspondientes
df_ventas = pd.read_excel("Ventas.xlsx")
df_clientes = pd.read_excel("Clientes.xlsx")
df_productos = pd.read_excel("Productos.xlsx")
df_pob = df[['Country', 'Population (2017)']]
db_pib = df[['Country', 'GDP (nominal, 2017)']]
df_rpc = df[['Country', 'GDP per capita']]
merge_web_scrappiing = df[['Country', 'Population (2017)', 'GDP (nominal, 2017)', 'GDP per capita']]

dataframes = {
    "Ventas": df_ventas,
    "Clientes": df_clientes,
    "Productos": df_productos,
    "Poblacion": df_pob,
    "PIB": db_pib,
    "Renta per capita": df_rpc
}

## MODIFICANDO ALGUNOS CARACTERES
dataframes['Ventas']['Precio unitario'] = dataframes['Ventas']['Precio unitario'].str.replace(",",".").astype(float)
dataframes['PIB']['GDP (nominal, 2017)'] = dataframes['PIB']['GDP (nominal, 2017)'].str.replace("$","").str.replace(",","").astype(float)
dataframes['Renta per capita']['GDP per capita'] = dataframes['Renta per capita']['GDP per capita'].str.replace("$","").str.replace(",","").astype(int)

### COMPLETANDO FECHA DE ENVIO
mediana = (dataframes['Ventas']['Fecha envío'] - dataframes['Ventas']['Fecha compra']).median()
print("###########################", mediana)
dataframes['Ventas']['Fecha envío'] = dataframes['Ventas']['Fecha compra'] + mediana

for key, df in dataframes.items():
  print(key)
  print(df.shape)
  print(df.dtypes)
  print(df)

## REVISIÓN DE VALORES NULL
for key, df in dataframes.items():
  print(key)
  print(df.isnull().sum(), "\n")

## LIMPIANDO DATOS
for key, df in dataframes.items():
  dataframes[key] = df.dropna()

## LIMPIEZA DE REGISTROS DUPLICADOS
for key, df in dataframes.items():
  dataframes[key] = df.drop_duplicates()

######## DESCRIBE
for key, df in dataframes.items():
    print(key)
    print(df.describe(), "\n")

## QUITAR REGISTROS DONDE EL NÚMERO DE PEDIDOS EXCEDE A 13
print("PEDIDOS QUE EXCEDEN LAS CANTIDADES DE 13")
pedidos_exceden_13 = dataframes['Ventas'][dataframes['Ventas']['Cantidad'] > 13]
print(pedidos_exceden_13.shape)
print(pedidos_exceden_13.dtypes)
print(pedidos_exceden_13)

# Solo quedarnos con menores o iguales a 13
dataframes['Ventas'] = dataframes['Ventas'][dataframes['Ventas']['Cantidad'] <= 13]
print("Nueva dimensiónd el DF", dataframes['Ventas'].shape)

################### COMBINACIÓN DE LAS TABLAS INDEPENDIENTES

dataframes['GLOBAL'] = dataframes['Ventas'].merge(dataframes['Clientes'], on = 'ID Cliente', how = 'inner')\
    .merge(dataframes['Productos'], on = 'ID Producto', how = 'inner')
print("\n", dataframes['GLOBAL'])

print("PAIS CON EL MAYOR NUMERO DE VENTAS")
gb_country = dataframes['GLOBAL'].groupby(['País']).size().reset_index(name = 'ventas').sort_values('ventas', ascending=False)
print(gb_country)

print("AÑO CON MAYOR NUMERO DE VENTAS")
gb_country = dataframes['GLOBAL'].groupby([dataframes['GLOBAL']['Fecha compra'].dt.year]).size().reset_index(name = 'ventas').sort_values('ventas', ascending=False)
print(gb_country)

print("PRODUCTO CON MAYOR BENEFICIO")
dataframes['GLOBAL']['Beneficio'] = dataframes['GLOBAL']['Cantidad']*(dataframes['GLOBAL']['Precio unitario'] - dataframes['GLOBAL']['Coste Producción'])

gb_country = dataframes['GLOBAL'].groupby(['Nombre Producto']).agg({'Beneficio':sum}).reset_index().sort_values('Beneficio', ascending=False)
print(gb_country)

## RELACION PER CAPITA Y BENEFICIO OBTENIDO POR PAIS
gb_country = dataframes['GLOBAL'].groupby(['País']).agg({'Beneficio':sum}).reset_index().sort_values('Beneficio', ascending=False)
relation_df = gb_country.merge(dataframes['Renta per capita'], how = 'inner', left_on = 'País', right_on='Country')
print(relation_df)

## REVISIÓN DE RELACION ENTRE DATOS DE WEBSCRAPPING
merge_web_scrappiing['GDP (nominal, 2017)'] = merge_web_scrappiing['GDP (nominal, 2017)'].str.replace("$","").str.replace(",","").astype(float)
merge_web_scrappiing['GDP per capita'] = merge_web_scrappiing['GDP per capita'].str.replace("$","").str.replace(",","").astype(int)
print(merge_web_scrappiing.dtypes)
print(merge_web_scrappiing.corr())

## PAIS CON MAS DIFERNCIA DE ENVIO
print("PAÍS CON MAS DIFERENCIA DE ENVIO")
dataframes['GLOBAL']['diferencia envio'] = dataframes['GLOBAL']['Fecha envío'] - dataframes['GLOBAL']['Fecha compra']
max_differencia = dataframes['GLOBAL']['diferencia envio'].max()
print(dataframes['GLOBAL'][dataframes['GLOBAL']['diferencia envio'] == max_differencia]['País'].unique().tolist())

## EXPORTAR FICHERO
dataframes['GLOBAL'].to_excel("Reporte Beneficios.xlsx")