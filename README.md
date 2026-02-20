# 🐱 THE DIVE: Laberinto Minimax 🐭

Un juego de persecución en consola desarrollado en Python. El proyecto simula un escenario de "gato y ratón" dentro de un laberinto y destaca por su implementación de Inteligencia Artificial utilizando el algoritmo **Minimax con Poda Alfa-Beta** para el proceso de toma de decisiones de los agentes.

## ⚙️ Características Principales

- **Modos de Juego:** \* Jugador vs IA (Jugando como Gato).
  - Jugador vs IA (Jugando como Ratón).
  - Modo Espectador (IA vs IA).
- **Inteligencia Artificial Ajustable:** La profundidad del árbol de decisiones (Minimax) varía según la dificultad seleccionada:
  - Fácil: Profundidad 1
  - Medio: Profundidad 3
  - Imposible: Profundidad 6
- **Heurística Avanzada:** La función de evaluación incluye comportamientos específicos. El ratón entra en un "modo pánico" priorizando la huida si el gato está cerca, mientras que el gato incluye un factor de "impaciencia" para evitar bucles de movimientos repetitivos a medida que avanzan los turnos.
- **Interfaz en Terminal:** Renderizado visual fluido utilizando limpieza de consola nativa (`cls`/`clear`) y caracteres Unicode (emojis).

## 📋 Requisitos

- Python 3.x
- Terminal o consola con soporte para codificación UTF-8 (para visualizar los emojis correctamente).
- El archivo `crear_mapa.py` debe estar en el mismo directorio (módulo de configuración de los niveles).

## 🚀 Instalación y Ejecución

1. Descarga los archivos del proyecto en un mismo directorio.
2. Abre una terminal y navega hasta la carpeta del proyecto.
3. Ejecuta el script principal:
   ```bash
   python main.py
   ```
