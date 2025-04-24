import numpy as np
import random
import os
from buscar_algoritmo import a_estrella
from heuristica import distancia_manhattan

class Laberinto:
    def __init__(self, archivo_config="assets/configuraciones/laberinto.txt"):
        self.ancho = 0
        self.alto = 0
        self.grid = None
        self.pos_agente = (0, 0)
        self.pos_objetivo = (0, 0)
        self.tiempo_ultima_actualizacion = 0
        self.intervalo_actualizacion = 10  

        if not os.path.exists(archivo_config):
            raise FileNotFoundError(f"No se encontró el archivo de configuración: {archivo_config}")
        
        self.cargar_desde_archivo(archivo_config)
        self.validar_camino()  

    def cargar_desde_archivo(self, ruta):
        """Carga el laberinto desde un archivo de texto"""
        with open(ruta, 'r') as f:
            lineas = [linea.strip() for linea in f if linea.strip() and not linea.strip().startswith('#')]
            
            if not lineas:
                raise ValueError("El archivo está vacío o solo contiene comentarios")
            
            dimensiones = lineas[0].split()
            if len(dimensiones) != 2:
                raise ValueError("La primera línea debe contener dos números (ancho y alto)")
            
            try:
                self.ancho, self.alto = map(int, dimensiones)
            except ValueError:
                raise ValueError("Las dimensiones deben ser números enteros")
            
            self.grid = np.zeros((self.alto, self.ancho), dtype=int)
            
            for y, linea in enumerate(lineas[1:self.alto + 1]):
                celdas = linea.split()
                if len(celdas) != self.ancho:
                    raise ValueError(f"La línea {y+2} no tiene {self.ancho} celdas")
                
                for x, char in enumerate(celdas):
                    if char == '1':
                        self.grid[y][x] = 1
                    elif char == 'A':
                        self.pos_agente = (x, y)
                    elif char == 'Q':
                        self.pos_objetivo = (x, y)
                    elif char != '0':
                        raise ValueError(f"Carácter no reconocido: '{char}' en posición ({x}, {y})")

    def es_movimiento_valido(self, x, y):
        """Verifica si (x, y) es una posición válida."""
        return (0 <= x < self.ancho and 
                0 <= y < self.alto and 
                self.grid[y][x] != 1)

    def actualizar(self, tiempo_actual):
        """Actualiza el laberinto dinámicamente"""
        if tiempo_actual - self.tiempo_ultima_actualizacion > self.intervalo_actualizacion:
            self.tiempo_ultima_actualizacion = tiempo_actual
            self.mover_objetivo()
            self.modificar_paredes()

    def mover_objetivo(self):
        """Mueve el objetivo a una posición aleatoria válida"""
        posiciones_validas = []
        for y in range(self.alto):
            for x in range(self.ancho):
                if self.grid[y][x] == 0 and (x, y) != self.pos_agente:
                    posiciones_validas.append((x, y))
        if posiciones_validas:
            self.pos_objetivo = random.choice(posiciones_validas)

    def modificar_paredes(self):
        """Cambia aleatoriamente algunas paredes"""
        for _ in range(2):
            x, y = random.randint(0, self.ancho - 1), random.randint(0, self.alto - 1)
            if (x, y) not in [self.pos_agente, self.pos_objetivo]:
                self.grid[y][x] = 1 - self.grid[y][x]

    def validar_camino(self):
        intentos = 0
        while True:
            camino = a_estrella(self, self.pos_agente, self.pos_objetivo, distancia_manhattan)
            if camino:
                break
            else:
                intentos += 1
                print(f"[Laberinto] Intento {intentos}: no se encontró camino, regenerando laberinto...")

        
                self.cargar_desde_archivo("assets/configuraciones/laberinto.txt")