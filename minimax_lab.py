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
            self.tablero[x][y] = SIMBOLO_MURO

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
                tablero_visual[px][py] = peon.simbolo
                
        for fila in tablero_visual:
            texto_fila = ' '.join(fila)
            print(texto_fila)
                
        
        
        