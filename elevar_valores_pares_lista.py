def elevar_pares(lista):
    return [elemento ** 2 if elemento % 2 == 0 else elemento for elemento in lista]

lista = [1, 2, 3, 4, 5, 6, 7, 8, 9]
print(f"La lista original es {lista}")
print(f"Elevando los elementos al cuadrado el resultado es {elevar_pares(lista)}")