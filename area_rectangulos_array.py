import numpy as np

def area_rectangulos_array(bases, alturas):
    areas = bases * alturas / 2
    return [area for area in areas if area > 10]

bases_rec = np.array([5, 2, 4, 7, 8])
alturas_rec = np.array([3, 4, 1, 4, 3])

print(f"Resultados con más de 10 unidades de área para los rectángulos")
print(f"Bases: {bases_rec}")
print(f"Alturas: {alturas_rec}")
print(area_rectangulos_array(bases_rec, alturas_rec))