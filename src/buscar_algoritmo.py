import heapq
from collections import deque
from heuristica import distancia_manhattan 

def a_estrella(laberinto, inicio, objetivo, heuristica):
    abiertos = []
    

    if heuristica.__name__ == "distancia_manhattan":
        h = lambda a, b: distancia_manhattan(a, b, laberinto)
    else:
        h = heuristica
    
    heapq.heappush(abiertos, (0 + h(inicio, objetivo), inicio, [inicio]))
    visitados = set([inicio])
    
    while abiertos:
        _, (x, y), camino = heapq.heappop(abiertos)
        if (x, y) == objetivo:
            return camino
        
        for dx, dy in [(0,1),(1,0),(0,-1),(-1,0)]:
            nx, ny = x + dx, y + dy
            
        
            if not (0 <= nx < laberinto.ancho and 0 <= ny < laberinto.alto):
                continue
                
        
            if laberinto.grid[ny][nx] == 1:
                if heuristica.__name__ == "distancia_manhattan":
                    
                    if abs(nx - x) > 1 or abs(ny - y) > 1:
                        continue  
                else:
        
                    continue
            
            if (nx, ny) not in visitados:
                visitados.add((nx, ny))
                nuevo_costo = len(camino) + 1
                heapq.heappush(abiertos, 
                             (nuevo_costo + h((nx, ny), objetivo), 
                             (nx, ny), 
                             camino + [(nx, ny)]))
    return None

def busqueda_amplitud(laberinto, inicio, objetivo):
    """BA: Búsqueda en Amplitud (sin heurística)"""
    cola = deque([(inicio, [inicio])])
    visitados = set([inicio])
    
    while cola:
        (x, y), camino = cola.popleft()
        if (x, y) == objetivo:
            return camino
        
        for dx, dy in [(0,1),(1,0),(0,-1),(-1,0)]:
            nx, ny = x + dx, y + dy
            if (0 <= nx < laberinto.ancho and 0 <= ny < laberinto.alto and 
                laberinto.grid[ny][nx] != 1 and (nx, ny) not in visitados):
                visitados.add((nx, ny))
                cola.append(((nx, ny), camino + [(nx, ny)]))
    return None

def busqueda_profundidad(laberinto, inicio, objetivo):
    """BP: Búsqueda en Profundidad (sin heurística)"""
    pila = [(inicio, [inicio])]
    visitados = set([inicio])
    
    while pila:
        (x, y), camino = pila.pop()
        if (x, y) == objetivo:
            return camino
        
        for dx, dy in [(0,1),(1,0),(0,-1),(-1,0)]:
            nx, ny = x + dx, y + dy
            if (0 <= nx < laberinto.ancho and 0 <= ny < laberinto.alto and 
                laberinto.grid[ny][nx] != 1 and (nx, ny) not in visitados):
                visitados.add((nx, ny))
                pila.append(((nx, ny), camino + [(nx, ny)]))
    return None