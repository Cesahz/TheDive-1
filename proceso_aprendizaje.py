# # inicio el proyecto aprendiendo del tablero
# def Crear_tablero(fila,columna):
#     tablero = []
#     for i in range(fila):
#         tablero.append(['.']*columna)
#     return tablero

# tablero = Crear_tablero(5,5)
# tablero[3][2] = 'G'
# tablero[1][3] = 'R'
# #para este metodo accedemos al indice de la lista y luego al indice de los elementos de esa fila


# # en python al multiplicar una lista por tal numero, agrega a esa lista el mismo elemento tal cantidad de veces

# def Mostrar_tablero():
#     for i in range(len(tablero)):
#         print(tablero[i])
# Mostrar_tablero()


#=====Optimizacion de tablero=====
def Crear_tablero(fila,columna):
    return [['.']*columna for i in range(fila)]


def Mostrar_tablero(tablero_a_mostrar):
    print('Tablero del juego: ')
    # join une los elementos de la lista usando un espacio en el medio
    for fila in tablero_a_mostrar:
        fila_texto = " ".join(fila)
        print(fila_texto)
    print('='*20)

# zona de ejecucion

TABLERO = Crear_tablero(12,12)
TABLERO[3][8] = 'G'
TABLERO[11][3] = 'R'
Mostrar_tablero(TABLERO)
