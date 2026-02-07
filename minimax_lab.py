import random
import os
import copy
import sys


#configuracion de variables y configuraciones globales

SIMBOLO_VACIO = '⬜' 
SIMBOLO_MURO = '🧱'
SIMBOLO_GATO = '🐱'
SIMBOLO_RATON = '🐭'
SIMBOLO_QUESO = '🧀'

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


    def mover_aleatoriamente(self,juego):
        #definir las posibles opciones de movimiento con tuplas
        opciones = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        random.shuffle(opciones)
        for d in opciones:
            nueva_x = self.x + d[0]
            nueva_y = self.y + d[1]
            if juego.es_movimiento_valido(nueva_x,nueva_y):
                self.cambiar_posicion(nueva_x,nueva_y)
                print('El raton se ha movido')
                return

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
        print('----Laberinto----')
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



# esta condicional inicial es por si luego quiero importar en otro archivo para hacer pruebas, por ahora
# lo dejo asi y tambien aprendo a trabajar con modulo
if __name__ == "__main__":
    #crear juego
    mi_juego = Juego(10, 10)
    
    #crear los peones del tablero
    tom = Gato(0, 0)
    jerry = Raton(9, 9)
    #agregar al tablero
    mi_juego.agregar_peon(tom)
    mi_juego.agregar_peon(jerry)
    #renderizar antes del bucle para ver donde tamos
    mi_juego.renderizar()
    
    print("--- INICIO ---")
    while True:
    # --- PRUEBA MANUAL DE MOVIMIENTO ---
        direccion = input("Presiona (WASD) para mover al gato: ").lower()
        siguiente_x = tom.x
        siguiente_y = tom.y

        if direccion == 'w':
            siguiente_y -= 1

        elif direccion == "s":
            siguiente_y += 1

        elif direccion == "a":
            siguiente_x -= 1

        elif direccion == "d":
            siguiente_x += 1
    
        else:
            print("Tecla no válida. Usa W, A, S, D. (minusculas)")
            continue
        
        if mi_juego.es_movimiento_valido(siguiente_x,siguiente_y):
            tom.cambiar_posicion(siguiente_x,siguiente_y)
            print(f'Tom se movio a {siguiente_x}, {siguiente_y}')
        else:
            print('Golpe, no se puede pasar por ahi')
        jerry.mover_aleatoriamente(mi_juego)
        #renderizar el movimiento
        mi_juego.renderizar()