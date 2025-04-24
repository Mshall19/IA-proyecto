from buscar_algoritmo import a_estrella
from heuristica import distancia_manhattan, distancia_euclidiana
from buscar_algoritmo import a_estrella, busqueda_amplitud, busqueda_profundidad

class Agente:
    def __init__(self, laberinto):
        self.laberinto = laberinto
        self.camino_actual = []
        self.tipo_heuristica = "Manhattan"  

    def encontrar_camino(self, tipo_heuristica=None):
        """Encuentra camino usando la heurística especificada"""
        if tipo_heuristica is not None:
            self.tipo_heuristica = tipo_heuristica
            
        inicio = self.laberinto.pos_agente
        objetivo = self.laberinto.pos_objetivo
        
        heuristica = distancia_manhattan if self.tipo_heuristica == "Manhattan" else distancia_euclidiana
        self.camino_actual = a_estrella(self.laberinto, inicio, objetivo, heuristica)
        
        return self.camino_actual
    
    def encontrar_camino_ba(self):
        """BA: Usa Búsqueda en Amplitud"""
        self.camino_actual = busqueda_amplitud(self.laberinto, self.laberinto.pos_agente, self.laberinto.pos_objetivo)
        return self.camino_actual

    def encontrar_camino_bp(self):
        """BP: Usa Búsqueda en Profundidad"""
        self.camino_actual = busqueda_profundidad(self.laberinto, self.laberinto.pos_agente, self.laberinto.pos_objetivo)
        return self.camino_actual