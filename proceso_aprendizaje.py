# inicio el proyecto aprendiendo del tablero

def Crear_tablero(fila,columna):
    tablero = []
    for i in range(fila):
        tablero.append(['.']*columna)
    return tablero

tablero = Crear_tablero(5,5)
tablero[3][2] = 'G'
tablero[1][3] = 'R'
#para este metodo accedemos al indice de la lista y luego al indice de los elementos de esa fila


# en python al multiplicar una lista por tal numero, agrega a esa lista el mismo elemento tal cantidad de veces

def Mostrar_tablero():
    for i in range(len(tablero)):
        print(tablero[i])
Mostrar_tablero()