import random
import os
import copy
import sys


#configuracion de variables y configuraciones globales

SIMBOLO_VACIO = '.'
SIMBOLO_MURO = '#'
SIMBOLO_GATO = 'G'
SIMBOLO_RATON = 'R'
SIMBOLO_QUESO = 'Q'

#definir las clases
#una clase para cualquier cosa que viva en el tablero, peon me parecio adecuado
class Peon:
    def __init__(self, x, y, simbolo):
        self.x = x
        self.y = y
        self.simbolo = simbolo
    def cambiar_posicion(self,nueva_x,nueva_y):
        #actualizamos las coordenadas
        self.x = nueva_x
        self.y = nueva_y

class Gato(Peon):
    #gato malo, tiene que atrapar al raton para poder ganar
    def __init__(self, x, y):
        super().__init__(x, y, SIMBOLO_GATO)
        
class Raton(Peon):
    #sera la presa, su objetivo es comer queso y tambien maximizar distancia
    def __init__(self, x, y):
        super().__init__(x, y, SIMBOLO_RATON)

#aca defino la clase mas importante, que seria la del juego o sistema
class Juego:
    #este es como el dios, sabe todo lo que pasa en las ejecuciones, turnos, que hay en el tablero etc
    def __init__(self,ancho,alto):
        self.ancho = ancho
        self.alto = alto
        self.tablero = []
        #lista para saber que criaturas esta en el tablero
        self.peones = []
        self.generar_tablero_vacio()
    
    def generar_tablero_vacio(self):
        #llenar el tablero con valores limpias como '.' para que sea el tablero base
        self.tablero = [[SIMBOLO_VACIO for i in range(self.ancho)] for i in range(self.alto)]
    
    def agregar_peon(self, peon):
        #recibe el tipo de peon: gato o raton y agrega a la lista
        self.peones.append(peon)
    
    def colocar_muro(self,x,y):
        #coloca un obstaculo (muro) en una coord especifica
        if 0 <= x < self.ancho and 0 <= y < self.alto:
            self.tablero[y][x] = SIMBOLO_MURO

    def renderizar(self):
        #este dibuja el estado de la consola en el presente de su ejecucion
        comando = "cls" if os.name == "nt" else 'clear'
        os.system(comando)
        print('---- EL LABERINTO ----')
        #una copia de seguridad
        #nota : deepcopy crea una clon independiente que no toca al original
        tablero_visual = copy.deepcopy(self.tablero)
        
        #ahora pinto los peones encima del tablero copiado
        for peon in self.peones:
            #guardar las coordenadas
            px = peon.x
            py = peon.y
            
            #controlar que no este fuera del tablero
            if 0 <= px < self.ancho and 0 <= py < self.alto:
                tablero_visual[py][px] = peon.simbolo
                
        for fila in tablero_visual:
            texto_fila = ' '.join(fila)
            print(texto_fila)
    
    def es_movimiento_valido(self,x,y):
        #no salir del tablero
        if x < 0:
            return False
        if y < 0:
            return False
        if x >= self.ancho:
            return False
        if y >= self.alto:
            return False
        #no chocar con el muro
        if self.tablero[y][x] == SIMBOLO_MURO:
            return False
        
        #si pasa todas la pruebas me devuelve true
        return True






if __name__ == "__main__":
    # Crear juego y muro
    mi_juego = Juego(10, 10)
    mi_juego.colocar_muro(1, 0) # Ponemos un muro a la derecha de Tom (en x=1, y=0)
    
    # Crear peones
    tom = Gato(0, 0)
    jerry = Raton(9, 9)
    
    mi_juego.agregar_peon(tom)
    mi_juego.agregar_peon(jerry)
    
    print("--- INICIO ---")
    mi_juego.renderizar()
    
    # --- PRUEBA MANUAL DE MOVIMIENTO ---
    input("Presiona Enter para intentar mover al Gato...")

    # Intento 1: Mover a la derecha (x=1, y=0) -> ¡HAY UN MURO!
    siguiente_x = 1
    siguiente_y = 0
    
    if mi_juego.es_movimiento_valido(siguiente_x, siguiente_y):
        print("Moviendo gato a la derecha...")
        tom.cambiar_posicion(siguiente_x, siguiente_y)
    else:
        print("¡GOLPE! El gato chocó con un muro en (1, 0)")

    # Intento 2: Mover hacia abajo (x=0, y=1) -> ESTÁ LIBRE
    siguiente_x = 0
    siguiente_y = 1
    
    if mi_juego.es_movimiento_valido(siguiente_x, siguiente_y):
        print("Moviendo gato hacia abajo...")
        tom.cambiar_posicion(siguiente_x, siguiente_y)
    else:
        print("¡GOLPE! El gato no pudo bajar")
        
    mi_juego.renderizar()