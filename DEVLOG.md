# 🐱 The Dive: Challenge Minimax 🐭

**Cesar Espinola** - 10/02/2026 -- 22:59
Finalmente terminé el challenge, al menos la primera versión funcional y bonita.

## ¿Qué construí?

### Un simulador de persecución en Python puro

Sin librerías externas que facilitan el trabajo.

- Mi mayor problema al inicio fue qué tan complicado lo podría hacer. Me gusta complicar las cosas, pero también desconocía los límites que tenía el algoritmo de Minimax con el tiempo de "pensamiento".
- Primero lo hice en `5x5`, luego a `10x10` y después `12x9`.
- También me gustó la forma de hacer el tablero con las listas vacías. Hasta ahora me sigue confundiendo un poco la forma de ubicar las coordenadas porque estoy acostumbrado a las matemáticas, pero nada del otro mundo.

### Implementé el algoritmo de Minimax con Poda Alfa-Beta

Al principio me intimidaba, pero luego de practicar un par de veces entendí bien el concepto y se me hizo fácil, creativo y también divertido.

- **La Poda:** Lo que más me costó entender fue la Poda. La forma de descartar la entendía, pero se me complicaba visualizar los cortes sin mirar los otros; poniéndolo en práctica, obviamente, también me adapté.
- **El Código:** Fue más complejo de entender estos conceptos, más que nada porque era algo nuevo para mí. No sabía si Minimax era una librería o "algo"; resultó que yo lo tenía que armar de 0.
- **Rendimiento:** Logré que la IA piense hasta **6 turnos en el futuro** sin que el juego se congele gracias a la poda. Pude poner más, pero para este tipo de juego me pareció innecesario agregar tantos; probé con 15 y se quedó pensando un montón. Si la cosa se hubiera puesto mucho más compleja, me daría algunos problemas.

### El entorno

Para la dificultad se me ocurrió cambiar tanto el mapa como la cantidad de turnos que puede ver la IA. Como me sobra mucho tiempo, me gustaría pulir mejor eso porque no noté tantos cambios en la estrategia.

- Mi peor reto de todo el Challenge fue hacer el mapa. Mi objetivo era que en el modo **IA vs IA**, el mapa sea un factor importante a la hora de conseguir la victoria. Al menos con el mapa del Nivel 3 me salió algo interesante con ese concepto.

---

## ¿Qué me funcionó bien?

### La Heurística Bipolar

Una de las cosas que caracteriza al ratón es que puede pasar de "miedo" a "codicia", dependiendo de la distancia.

- Con el gato no estoy del todo satisfecho aún, aunque ya terminé la primera versión y funciona perfecto, me gustaría hacer al gato más inteligente y con más "estados".
- Pero viendo el lado positivo, el gato intenta ser bastante agresivo e interceptar el queso, no solamente busca al ratón.

---

## ¿Qué fue un desastre (al principio)?

### El baile infinito

Cuando el gato y el ratón estaban cerca y simplemente subían y bajaban sin sentido en bucle hasta que termine el límite de rondas que puse.

- Entendí matemáticamente cómo funcionaba eso, pero resultaba feo a la vista y no se me hacía presentable.
- Con el tiempo entendí que si las 2 IAs son inteligentes, la mayoría de veces va a terminar por límite de rondas, ya que ninguno es tan tonto como para regalarse, o al menos Minimax no permite eso sin ponerle margen de error.

### El gato campero

También en las primeras pruebas el gato quedaba a mitad del mapa esperando el movimiento del ratón, no progresaban nunca y terminaba por límite de rondas. Esto tiene sentido según la matemática, pero tampoco me gustaba la idea de que fuera así.

---

## Mi mejor "jaja"

Al inicio el movimiento del ratón era aleatorio y no se basaba en el algoritmo de Minimax, por lo que el ratón solía regalarse al gato.

No soy amargado, pero no hubo mucho "jaja" en este challenge, pero me divertí mucho. Me costó mucho ganarle al ratón en la dificultad "Imposible".

---

## 🔮 Cosas que me gustaría agregar

Probablemente el día de mi presentación ya estén implementadas, pero hago una lista para no olvidar las cosas que me gustaría agregar:

1.  **2 Gatos vs 1 Ratón:** Como siento que el ratón es más inteligente que el gato, me gustaría probar con 2 gatos y un ratón, al menos en el modo IA. En el modo de Jugador vs IA sería muy difícil, pero debería de probarlo.
2.  **Generador de mapa aleatorio:** Se me ocurren muchas cosas para esto, pero también me limito para no hacer mucho más de lo necesario, al menos para THE DIVE. SI VEO que mi esfuerzo extra es valorado, seguiré agregando cosas hasta que se me acaben las ideas.
3.  **Diferentes modos (Competitivo):** Como tener en la consola 2 tableros iguales: en uno jugamos nosotros como jugador y en el otro la IA. El objetivo sería capturar la mayor cantidad de ratones en cierta cantidad de tiempo. Básicamente competir con la IA pero en diferentes tableros y con ratones que aparecen al azar, poder visualizar qué hace la IA como gato mientras yo juego. Al final del tiempo, si consigo más puntos que la IA, gano yo.
4.  **Sistema de ELO:** Guardar registro de cada partida y puntuar según nuestro desempeño, tener como una cantidad de trofeos que sube si ganamos y baja si perdemos. Aunque no lo veo muy útil para este juego, pero sería divertido ver cómo alguien tiene 0% de win rate jeje.

---

## Conclusión y Futuro

Este desafío ha sido más que escribir código; ha sido una revelación. Pasar de no saber qué era Minimax a ver a mi IA tomar decisiones "humanas" me ha hecho darme cuenta de algo importante: **me encanta esto**.

Disfruto analizando los "estados de pensamiento" de la máquina, entendiendo por qué decide huir o atacar, y traduciendo lógica pura en comportamiento. He aprendido muchísimo en tiempo récord y tengo claro que mi camino está en la **Inteligencia Artificial**. Quiero dedicarme a crear sistemas que piensen, reten y sorprendan. Esto es solo el comienzo.
