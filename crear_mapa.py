def configurar_nivel(juego,dificult):
    #colocar muro y queso segun la diuficultad
    #modo facil
    if dificult == "1":
        # Solo un par de piedras para molestar, pero mucho espacio libre
        juego.colocar_queso(10, 1)
        muros = [(3,3), (3,5), (8,3), (8,5), (5,2), (5,6)]
        for x, y in muros:
            juego.colocar_muro(x, y)
            
        for x in range(1, 4):
            juego.colocar_muro(x, 2)
            
        for x in range(8, 11):
            juego.colocar_muro(x, 6)

        juego.colocar_muro(0, 5)
        juego.colocar_muro(11, 3)
        print("Mapa cargado: LA ZONA URBANA (Medio)")
        
    #para el nivel medio
    elif dificult == "2":
        juego.colocar_queso(0, 8)
        for y in range(3, 6):
            juego.colocar_muro(5, y)
            juego.colocar_muro(6, y)
        print("Mapa cargado: EL BOSQUE (Medio)")
    #para el nivel dificil
    elif dificult == "3":
        juego.colocar_queso(3,2)
        juego.colocar_muro(1,1)
        juego.colocar_muro(2,1)
        juego.colocar_muro(3,1)
        juego.colocar_muro(2,3)
        juego.colocar_muro(3,3)
        juego.colocar_muro(4,3)
        juego.colocar_muro(5,3)
        juego.colocar_muro(6,3)
        juego.colocar_muro(6,4)
        juego.colocar_muro(6,5)
        juego.colocar_muro(4,5)
        juego.colocar_muro(3,5)
        juego.colocar_muro(2,5)
        juego.colocar_muro(1,5)
        juego.colocar_muro(3,6)
        juego.colocar_muro(3,7)
        juego.colocar_muro(2,7)
        juego.colocar_muro(5,7)
        juego.colocar_muro(6,7)
        juego.colocar_muro(7,7)
        juego.colocar_muro(8,7)
        juego.colocar_muro(8,6)
        juego.colocar_muro(8,5)
        juego.colocar_muro(6,0)
        juego.colocar_muro(6,1)
        juego.colocar_muro(6,1)
        juego.colocar_muro(9,1)
        juego.colocar_muro(11,0)
        juego.colocar_muro(11,1)
        juego.colocar_muro(11,3)
        juego.colocar_muro(11,4)
        juego.colocar_muro(11,5)
        juego.colocar_muro(10,6)
        
        
        print("Mapa cargado: EL LABERINTO (Difícil)")