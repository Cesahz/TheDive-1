from crear_mapa import configurar_nivel
import random
import os
import copy
import sys
import time

# -1

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

# -2

#aca defino la clase mas importante, que seria la del juego o sistema
class Juego:
    #este es como el dios, sabe todo lo que pasa en las ejecuciones, turnos, que hay en el tablero etc
    def __init__(self,ancho,alto,turno_actual,max_turnos):
        self.ancho = ancho
        self.alto = alto
        self.turno = turno_actual
        self.max_turnos = max_turnos
        self.tablero = []
        self.queso = None
        #lista para saber que criaturas esta en el tablero
        self.peones = []
        self.generar_tablero_vacio()
    
    def generar_tablero_vacio(self):
        #llenar el tablero con valores limpias como '.' para que sea el tablero base
        #lo hago con bucles normales para que se entienda mejor y sea mas visual
        self.tablero = []
        for _ in range(self.alto):
            fila = []
            for _ in range(self.ancho):
                fila.append(SIMBOLO_VACIO)
            self.tablero.append(fila)
    
    def agregar_peon(self, peon):
        #recibe el tipo de peon: gato o raton y agrega a la lista
        self.peones.append(peon)
    
    def colocar_muro(self,x,y):
        #coloca un obstaculo (muro) en una coord especifica
        #verifico que este dentro de los limites antes de colocar
        if x >= 0 and x < self.ancho:
            if y >= 0 and y < self.alto:
                self.tablero[y][x] = SIMBOLO_MURO

    def colocar_queso(self,x,y):
        if x >= 0 and x < self.ancho:
            if y >= 0 and y < self.alto:
                self.tablero[y][x] = SIMBOLO_QUESO
                self.queso = (x,y)


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
            if px >= 0 and px < self.ancho:
                if py >= 0 and py < self.alto:
                    tablero_visual[py][px] = peon.simbolo
                
        for fila in tablero_visual:
            #uno los elementos de la fila en un solo texto de forma tradicional
            texto_fila = ""
            for elemento in fila:
                texto_fila = texto_fila + elemento
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

# -3

#funcion para evaluar el tablero (version ajustada)
def evaluar_tablero(juego):
    gato = juego.peones[0]
    raton = juego.peones[1]
    
    #condiciones de victoria/derrota
    if gato.x == raton.x and gato.y == raton.y:
        return 1000 #el gato gana
    
    if juego.queso and raton.x == juego.queso[0] and raton.y == juego.queso[1]:
        return -1000 #el raton gana
    
    if juego.turno >= juego.max_turnos:
        return -1000 #el raton por tiempo

    #calculo de distancias
    dist_gato_raton = calcular_distancia(gato.x, gato.y, raton.x, raton.y)
    
    dist_raton_queso = 0
    dist_gato_queso = 0
    if juego.queso:
        dist_raton_queso = calcular_distancia(raton.x, raton.y, juego.queso[0], juego.queso[1])
        dist_gato_queso = calcular_distancia(gato.x, gato.y, juego.queso[0], juego.queso[1])

    #PENSAMIENTO DEL GATO (MAXIMIZAR)
    #acercarse al raton
    score_gato = (30 - dist_gato_raton) * 4
    
    #si esta muy cerca le premiamos
    if dist_gato_raton <= 2:
        score_gato = score_gato + 20 

    #si el raton esta cerca del gato el gato intercepta
    if dist_raton_queso < 5:
        score_gato = score_gato + (30 - dist_gato_queso) * 5

    #PENSAMIENTO DEL RATON (MINIMIZAR)
    score_raton = 0
    
    #logica nueva: si el raton tiene ventaja de distancia y no esta en peligro inmediato
    tengo_ventaja = dist_raton_queso < dist_gato_queso
    estoy_seguro = dist_gato_raton > 2
    
    if tengo_ventaja and estoy_seguro:
        #ignora al gato y corre al queso
        #puntaje alto para dar prioridad
        score_raton = (30 - dist_raton_queso) * 10
        
    elif dist_gato_raton <= 2:
        #modo panico, retirada
        score_raton = dist_gato_raton * 8
        
    else:
        #modo normal
        score_raton = (30 - dist_raton_queso) * 4

    #PENSAMIENTOS EXTRA
    #impaciencia del gato, cuando mas temprano el turno mejor el puntaje a favor del gato
    impaciencia = juego.turno * 0.5

    #ruido para romper empates y evitar bucles tontos
    ruido = random.uniform(-0.5, 0.5)

    #formula final
    return score_gato - score_raton - impaciencia + ruido

# -4

#funcion auxiliar para tener los movimientos posibles
def obtener_movimiento_valido(juego, peon):
    movimientos = []
    direcciones = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    for d in direcciones:
        dx = d[0]
        dy = d[1]
        n_x = peon.x + dx
        n_y = peon.y + dy
        if juego.es_movimiento_valido(n_x,n_y):
            movimientos.append((n_x,n_y))
    return movimientos



#el cerebro de las IAs, la funcion que piensa los movimientos
def minimax(juego_copia, profundidad, es_turno_gato, alpha, beta):
    if profundidad == 0:
        return evaluar_tablero(juego_copia)
    
    valor_tablero = evaluar_tablero(juego_copia)
    if abs(valor_tablero) == 1000:
        return valor_tablero
    
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
            evaluacion = minimax(juego_futuro, profundidad - 1, False,alpha,beta)
            
            #4- elegir la mejor opcion
            if evaluacion > max_eval:
                max_eval = evaluacion
            
            #PODA (corte)
            if evaluacion > alpha:
                alpha = evaluacion
            if beta <= alpha:
                break
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
            evaluacion = minimax(juego_futuro, profundidad - 1, True, alpha, beta)
            
            #4- elegir el menor valor
            if evaluacion < min_eval:
                min_eval = evaluacion
            
            #PODA (corte)
            if evaluacion < beta:
                beta = evaluacion
            if beta <= alpha:
                break #cortar porque el gato no deja que llegue a ese estado tan bueno

        return min_eval

# -5

def mejor_movimiento_gato(juego,profundidad):
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
        puntaje = minimax(juego_futuro,profundidad,False,-float('inf'), float('inf')) #el siguiente turno es del raton por eso false
        
        #4- si este puntaje es mejor que el record
        if puntaje > mejor_puntaje:
            mejor_puntaje = puntaje
            mejor_movimiento = mov
    return mejor_movimiento

def mejor_movimiento_raton(juego,profundidad):
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
        puntaje = minimax(juego_futuro,profundidad,True,-float('inf'), float('inf')) #el siguiente turno es del raton por eso false
        
        #4- si este puntaje es mejor que el record
        if puntaje < mejor_puntaje:
            mejor_puntaje = puntaje
            mejor_movimiento = mov
    return mejor_movimiento

def obtener_movimiento_humano(juego, peon):
    #pide input al usuario hasta que ingrese un movimiento legal
    direcciones = {
        'w': (0, -1),
        's': (0, 1),
        'a': (-1, 0),
        'd': (1, 0)
    }
    while True:
        try:
            tecla = input(f"Tu turno ({peon.simbolo}): Usa W, A, S, D: ").lower()
            if tecla in direcciones:
                d = direcciones[tecla]
                dx = d[0]
                dy = d[1]
                n_x = peon.x + dx
                n_y = peon.y + dy
                
                if juego.es_movimiento_valido(n_x, n_y):
                    return (n_x, n_y) #retornar la coord valida
                else:
                    print("¡Movimiento inválido! (Muro o Borde)")
            else:
                print("Tecla desconocida. Solo W, A, S, D.")
        except KeyboardInterrupt:
            print("\nSaliendo del juego...")
            sys.exit()

# -6

# -7
# esta condicional inicial es por si luego quiero importar en otro archivo para hacer pruebas, por ahora
# lo dejo asi y tambien aprendo a trabajar con modulos
if __name__ == "__main__":
    #configuracion del menu
    
    os.system('cls' if os.name == 'nt' else 'clear')
    print("="*30)
    print("🐱 THE DIVE: LABERINTO MINIMAX 🐭")
    print("="*30)
    print("1. Jugar como GATO (Cazar al ratón)")
    print("2. Jugar como RATÓN (Huir y comer queso)")
    print("3. Modo ESPECTADOR (IA vs IA)")
    print("="*30)
    
    modo = input("Elige una opción (1-3): ")
    PROFUNDIDAD_IA = 6
    if modo == "1" or modo == "2":
        dificultad = input("Elige dificultad (1=Fácil, 2=Medio, 3=Imposible): ")
        if dificultad == "1":
            PROFUNDIDAD_IA = 1
        elif dificultad == "2":
            PROFUNDIDAD_IA = 3
        elif dificultad == "3":
            PROFUNDIDAD_IA = 6
        else:
            print('Tecla no valida\nSaliendo del juego. . .')
            sys.exit()
            
        
    #iniciar el juego
    mi_juego = Juego(16,9,0,120) 
    
    #generar tablero segun dificultad
    if modo == "1" or modo == "2":
        dificultad_mapa = dificultad
    else:
        dificultad_mapa = "3"

    configurar_nivel(mi_juego, dificultad_mapa)
    
    #los peones (gato :3 y raton)
    tom = Gato(0, 0)
    jerry = Raton(15,7)
    mi_juego.agregar_peon(tom)
    mi_juego.agregar_peon(jerry)
    
    mi_juego.renderizar()
    print("--- INICIO ---")
    time.sleep(1)

    #bucle del juego
    while True:
        #turno del GATO
        if modo == '1':
            #humano
            nx, ny = obtener_movimiento_humano(mi_juego, tom)
            tom.cambiar_posicion(nx, ny)
        else:
            #IA
            print('🐱 El Gato Artificial está pensando...')
            nueva_pos = mejor_movimiento_gato(mi_juego,PROFUNDIDAD_IA)
            if nueva_pos:
                tom.cambiar_posicion(nueva_pos[0], nueva_pos[1])
        
        #verificar la condicion de victoria del gato
        if tom.x == jerry.x and tom.y == jerry.y:
            mi_juego.renderizar()
            print("\n" + "💀"*10)
            print(" ¡GAME OVER! El Gato ha cenado.")
            print("💀"*10)
            break

        #turno del RATON
        #renderizar para actualizar tablero
        mi_juego.renderizar() 
        
        if modo == '2':
            #humano
            nx, ny = obtener_movimiento_humano(mi_juego, jerry)
            jerry.cambiar_posicion(nx, ny)
        else:
            #IA
            #el raton es tonto por 4 turnos, luego es inteligente
            if mi_juego.turno < 4: 
                print("🐭 El Ratón se mueve aleatoriamente (en panico)...")
                jerry.mover_aleatoriamente(mi_juego)
            else:
                print("🐭 El Ratón calcula su escape...")
                nueva_pos = mejor_movimiento_raton(mi_juego,PROFUNDIDAD_IA)
                if nueva_pos:
                    jerry.cambiar_posicion(nueva_pos[0], nueva_pos[1])
                else:
                    print("🐭 ¡Ratón acorralado!")

        #verificar victoria por comer queso
        if mi_juego.queso and jerry.x == mi_juego.queso[0] and jerry.y == mi_juego.queso[1]:
            mi_juego.renderizar()
            print("\n" + "🧀"*10)
            print(" ¡VICTORIA! El Ratón se comió el queso.")
            print("🧀"*10)
            break
            
        #verificar si el raton se suicida (muy poco probable)
        if tom.x == jerry.x and tom.y == jerry.y:
            mi_juego.renderizar()
            print("\n💀 ¡El Ratón corrió hacia el Gato! Gana Tom.")
            break

        #final del turno actual
        mi_juego.turno += 1

        mi_juego.renderizar()
        
        if mi_juego.turno >= mi_juego.max_turnos:
            print("\n Tiempo agotado. El Ratón sobrevive.")
            break
            
        #pausa para ver la pelea de las IAs :3
        if modo == '3':
            time.sleep(0.5)
