import numpy as np

def dist_gaus(x, std, cant):
    return np.random.normal(x, std, cant)

# x media
x = 3
std = 1.5
cant = 10000

distribucion = dist_gaus(x, std, cant)
media = np.mean(distribucion)
desviacion = np.std(distribucion)
print(f"La distribución es: {distribucion}")
print(f"Media de distribución: {media}")
print(f"Desviación de la distribución: {desviacion}")
print(f"El 95% de los valores están entre:")
print(f"{[media - 2*desviacion, media + 2*desviacion]}")