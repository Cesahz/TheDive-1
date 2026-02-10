import random
import os
import copy
import sys
import time

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
                return

#aca defino la clase mas importante, que seria la del juego o sistema
class Juego:
    #este es como el dios, sabe todo lo que pasa en las ejecuciones, turnos, que hay en el tablero etc
    def __init__(self,ancho,alto,turno_actual,max_turnos):
        self.ancho = ancho
        self.alto = alto
        self.turno = turno_actual
        self.max_turnos = max_turnos
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
        print('----Laberinto del gato y el raton----')
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
            texto_fila = ''.join(fila)
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

#funcion para medir distancia
def calcular_distancia(x1, y1, x2, y2):
    diferencia_x = abs(x1 - x2)
    diferencia_y = abs(y1 - y2)
    distancia_pasos = diferencia_x + diferencia_y
    return distancia_pasos

#funciona para evaluar el tablero
def evaluar_tablero(juego):
    posicion_gato = [juego.peones[0].x, juego.peones[0].y]
    posicion_raton = [juego.peones[1].x, juego.peones[1].y]
    
    if posicion_gato == posicion_raton:
        return 1000
    elif juego.turno >= juego.max_turnos:
        return -1000
    else:
        distancia = calcular_distancia(posicion_gato[0],posicion_gato[1],posicion_raton[0],posicion_raton[1])
        return 100 - distancia


#funcion auxiliar para tener los movimientos posibles
def obtener_movimiento_valido(juego, peon):
    movimientos = []
    direcciones = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    for dx, dy in direcciones:
        nx,ny = peon.x + dx, peon.y + dy
        if juego.es_movimiento_valido(nx,ny):
            movimientos.append((nx,ny))
    return movimientos



#el cerebro de las IAs, la funcion que piensa los movimientos
def minimax(juego_copia, profundidad, es_turno_gato):
    if profundidad == 0 or abs(evaluar_tablero(juego_copia)) == 1000:
        return evaluar_tablero(juego_copia)
    
    #turno del gato (busca maximizar el puntaje)
    if es_turno_gato:
        max_eval = -float('inf') #el peor puntaje posible
        
        #obtener al gato de la copia 
        gato_copia = juego_copia.peones[0]
        posibles_movs = obtener_movimiento_valido(juego_copia,gato_copia)
        
        for mov in posibles_movs:
            #1- clonar: creo un universo paralelo para no romper el actual
            juego_futuro = copy.deepcopy(juego_copia)
            
            #2- simular que muevo al gato en ese futuro
            juego_futuro.peones[0].cambiar_posicion(mov[0],mov[1])
            
            #3- recursividad: que pasa despues? 
            evaluacion = minimax(juego_futuro, profundidad - 1, False)
            
            #4- elegir la mejor opcion
            max_eval = max(max_eval, evaluacion)
        return max_eval
    # turno del raton (minimizar puntaje)
    else:
        min_eval = float('inf') #el mejor puntaje posible
        raton_copia = juego_copia.peones[1]
        posibles_movs = obtener_movimiento_valido(juego_copia, raton_copia)
        
        for mov in posibles_movs:
            #1- clonar
            juego_futuro = copy.deepcopy(juego_copia)
            
            #2- simular
            juego_futuro.peones[1].cambiar_posicion(mov[0], mov[1])
            
            #3- recursividad
            evaluacion = minimax(juego_futuro, profundidad - 1, True)
            
            #4- elegir el menor valor
            min_eval = min(min_eval, evaluacion)
        return min_eval


def mejor_movimiento_gato(juego):
    mejor_puntaje = -float('inf')
    mejor_movimiento = None # luego guardo aca (x,y)
    
    #1- tener el movimiento del gato real
    gato = juego.peones[0]
    movimientos = obtener_movimiento_valido(juego,gato)
    for mov in movimientos:
        #1-clonar
        juego_futuro = copy.deepcopy(juego)
        
        #2-simular
        juego_futuro.peones[0].cambiar_posicion(mov[0],mov[1])
        
        #3- preguntar al cerebro
        puntaje = minimax(juego_futuro,3,False) #el siguiente turno es del raton por eso false
        
        #4- si este puntaje es mejor que el record
        if puntaje > mejor_puntaje:
            mejor_puntaje = puntaje
            mejor_movimiento = mov
    return mejor_movimiento

def mejor_movimiento_raton(juego):
    mejor_puntaje = float('inf')
    mejor_movimiento = None # luego guardo aca (x,y)
    
    #1- tener el movimiento del gato real
    raton = juego.peones[1]
    movimientos = obtener_movimiento_valido(juego,raton)
    for mov in movimientos:
        #1-clonar
        juego_futuro = copy.deepcopy(juego)
        
        #2-simular
        juego_futuro.peones[1].cambiar_posicion(mov[0],mov[1])
        
        #3- preguntar al cerebro
        puntaje = minimax(juego_futuro,3,True) #el siguiente turno es del raton por eso false
        
        #4- si este puntaje es mejor que el record
        if puntaje < mejor_puntaje:
            mejor_puntaje = puntaje
            mejor_movimiento = mov
    return mejor_movimiento

# esta condicional inicial es por si luego quiero importar en otro archivo para hacer pruebas, por ahora
# lo dejo asi y tambien aprendo a trabajar con modulo
if __name__ == "__main__":
    
    #crear juego y definir turno maximo (TEMPORAAAAAAAAAAAAAAAAL_)((**&())))
    # muros temporales para pruebas
    mi_juego = Juego(10, 10, 0 , 50)
    mi_juego.colocar_muro(5, 5)
    mi_juego.colocar_muro(5, 6)
    mi_juego.colocar_muro(5, 7)
    #crear los peones del tablero
    tom = Gato(0, 0)
    jerry = Raton(9, 9)
    #agregar al tablero
    mi_juego.agregar_peon(tom)
    mi_juego.agregar_peon(jerry)
    #renderizar antes del bucle para ver donde tamos
    mi_juego.renderizar()
    print("--- INICIO ---")
    time.sleep(1)
    while True:
        print('El Gato Artificial esta pensando. . .')
        nueva_pos = mejor_movimiento_gato(mi_juego)
        
        if mi_juego.es_movimiento_valido(nueva_pos[0],nueva_pos[1]):
            tom.cambiar_posicion(nueva_pos[0],nueva_pos[1])
            
        if tom.x == jerry.x and tom.y == jerry.y:
            mi_juego.renderizar()
            print("\n" + "="*30)
            print("💀 ¡GAME OVER! El Gato ha cenado.")
            print("="*30)
            break

        #mover aleatoriamente al raton
        jerry.mover_aleatoriamente(mi_juego)
        
        #avisar si jerry se suicida
        if tom.x == jerry.x and tom.y == jerry.y:
            mi_juego.renderizar()
            print("\n💀 ¡El Ratón corrió hacia el Gato! Gana Tom.")
            break
    
        #renderizar el movimiento y sumar turno
        mi_juego.turno += 1
        mi_juego.renderizar()
        
        print(f'Turno {mi_juego.turno}/{mi_juego.max_turnos}')
        #definir la condicion de victoria del raton
        if mi_juego.turno >= mi_juego.max_turnos:
            print('El Raton sobrevivio. . .\n El gato PIERDE. . .')
            break
        time.sleep(0.25)
