def distancia_manhattan(a, b, laberinto=None):
    """
    Versión mejorada de Manhattan que puede saltar obstáculos adyacentes
    cuando recibe el objeto laberinto
    """
    distancia_base = abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    if laberinto is not None:
        if a[1] == b[1]:  
            step = 1 if b[0] > a[0] else -1
            for x in range(a[0], b[0], step):
                if laberinto.grid[a[1]][x] == 1:
                    
                    if abs(x - a[0]) <= 1 or abs(x - b[0]) <= 1:
                        return distancia_base
                    return distancia_base + 10  

        elif a[0] == b[0]:  
            step = 1 if b[1] > a[1] else -1
            for y in range(a[1], b[1], step):
                if laberinto.grid[y][a[0]] == 1:
                    if abs(y - a[1]) <= 1 or abs(y - b[1]) <= 1:
                        return distancia_base
                    return distancia_base + 10
    
    return distancia_base

def distancia_euclidiana(a, b):
    """
    Versión estándar que nunca salta obstáculos
    """
    return ((a[0] - b[0])**2 + (a[1] - b[1])**2)**0.5