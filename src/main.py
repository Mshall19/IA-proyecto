import pygame
import sys
import time
from laberinto import Laberinto
from agente import Agente
from buscar_algoritmo import a_estrella

pygame.init()

TAMANO_CELDA = 100
MARGEN = 600
MARGEN_SUPERIOR = 200
ANCHO_VENTANA = 4 * TAMANO_CELDA + 2 * MARGEN
ALTO_VENTANA = 4 * TAMANO_CELDA + MARGEN_SUPERIOR + MARGEN
pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Laberinto IA")

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
VERDE = (100, 200, 100)
AZUL = (70, 130, 180)
ROJO = (255, 50, 50)
MAGENTA = (180, 70, 180)
GRIS = (220, 220, 220)
COLOR_FONDO = (240, 245, 250)
COLOR_PANEL = (255, 255, 255)
COLOR_TEXTO = (60, 60, 60)
COLOR_ACTIVO = (50, 180, 50)
COLOR_INACTIVO = (180, 50, 50)
AZUL_BA = (0, 100, 200)
ROSA_BP = (200, 0, 100)

# Fuentes
try:
    fuente = pygame.font.SysFont('Arial', 28)
    fuente_titulo = pygame.font.SysFont('Arial', 36, bold=True)
except:
    fuente = pygame.font.Font(None, 28)
    fuente_titulo = pygame.font.Font(None, 36)


paso_actual = 0
ultima_actualizacion_animacion = 0
velocidad_animacion = 0.3
pausado = False

def dibujar_panel_superior(mostrar_m, mostrar_e, mostrar_ba, mostrar_bp):
    pygame.draw.rect(pantalla, COLOR_PANEL, (0, 0, ANCHO_VENTANA, MARGEN_SUPERIOR))
    titulo = fuente_titulo.render("Laberinto IA", True, COLOR_TEXTO)
    pantalla.blit(titulo, (ANCHO_VENTANA // 2 - titulo.get_width() // 2, 10))

    controles = [
        {"texto": "1: Manhattan", "color": ROJO, "activo": mostrar_m},
        {"texto": "2: Euclidiana", "color": MAGENTA, "activo": mostrar_e},
        {"texto": "3: BA (Amplitud)", "color": AZUL_BA, "activo": mostrar_ba},
        {"texto": "4: BP (Profundidad)", "color": ROSA_BP, "activo": mostrar_bp},
        {"texto": "ESPACIO: Pausa", "color": AZUL},
        {"texto": "R: Reiniciar", "color": VERDE}
    ]

    espacio_total = ANCHO_VENTANA - 100
    espacio_por_control = espacio_total // len(controles)

    for i, control in enumerate(controles):
        x_pos = 50 + i * espacio_por_control
        y_pos = 70

        texto = fuente.render(control["texto"], True, control["color"])
        pantalla.blit(texto, (x_pos, y_pos))

        if "activo" in control:
            estado = "ON" if control["activo"] else "OFF"
            color_estado = COLOR_ACTIVO if control["activo"] else COLOR_INACTIVO
            texto_estado = fuente.render(estado, True, color_estado)
            pantalla.blit(texto_estado, (x_pos, y_pos + 30))


def dibujar_laberinto(laberinto, camino_m=None, camino_e=None, camino_ba=None, camino_bp=None):
    global paso_actual, ultima_actualizacion_animacion, pausado  
    pantalla.fill(COLOR_FONDO)

    pos_x = (ANCHO_VENTANA - laberinto.ancho * TAMANO_CELDA) // 2
    pos_y = MARGEN_SUPERIOR + (ALTO_VENTANA - laberinto.alto * TAMANO_CELDA - MARGEN_SUPERIOR) // 2

    for y in range(laberinto.alto):
        for x in range(laberinto.ancho):
            rect = pygame.Rect(pos_x + x * TAMANO_CELDA, pos_y + y * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA)
            if laberinto.grid[y][x] == 1:
                pygame.draw.rect(pantalla, NEGRO, rect)
            elif (x, y) == laberinto.pos_agente:
                pygame.draw.rect(pantalla, AZUL, rect)
            elif (x, y) == laberinto.pos_objetivo:
                pygame.draw.rect(pantalla, VERDE, rect)
            else:
                pygame.draw.rect(pantalla, BLANCO, rect)
            pygame.draw.rect(pantalla, GRIS, rect, 1)

    if not pausado and time.time() - ultima_actualizacion_animacion > velocidad_animacion:
        paso_actual += 1
        ultima_actualizacion_animacion = time.time()

    def dibujar_paso(camino, color, forma):
        if not camino:
            return
        camino_sin_agente = [p for p in camino if p != laberinto.pos_agente]
        for i, (x, y) in enumerate(camino_sin_agente[:paso_actual]):
            cx, cy = pos_x + x * TAMANO_CELDA, pos_y + y * TAMANO_CELDA
            if forma == "cuadrado":
                rect = pygame.Rect(cx + 10, cy + 10, TAMANO_CELDA - 20, TAMANO_CELDA - 20)
                pygame.draw.rect(pantalla, color, rect, 5)
            elif forma == "circulo":
                center = (cx + TAMANO_CELDA // 2, cy + TAMANO_CELDA // 2)
                pygame.draw.circle(pantalla, color, center, TAMANO_CELDA // 3)
            elif forma == "triangulo":
                puntos = [(cx + TAMANO_CELDA // 2, cy + 10), (cx + 10, cy + TAMANO_CELDA - 10), (cx + TAMANO_CELDA - 10, cy + TAMANO_CELDA - 10)]
                pygame.draw.polygon(pantalla, color, puntos)
            elif forma == "rombo":
                puntos = [(cx + TAMANO_CELDA // 2, cy + 10), (cx + 10, cy + TAMANO_CELDA // 2),
                          (cx + TAMANO_CELDA // 2, cy + TAMANO_CELDA - 10), (cx + TAMANO_CELDA - 10, cy + TAMANO_CELDA // 2)]
                pygame.draw.polygon(pantalla, color, puntos)

            paso_texto = fuente.render(str(i + 1), True, NEGRO)
            pantalla.blit(paso_texto, (cx + TAMANO_CELDA // 2 - paso_texto.get_width() // 2,
                                       cy + TAMANO_CELDA // 2 - paso_texto.get_height() // 2))

    dibujar_paso(camino_m, ROJO, "cuadrado")
    dibujar_paso(camino_e, MAGENTA, "circulo")
    dibujar_paso(camino_ba, AZUL_BA, "triangulo")
    dibujar_paso(camino_bp, ROSA_BP, "rombo")


def main():
    global paso_actual, pausado

    laberinto = Laberinto()
    agente = Agente(laberinto)

    mostrar_m = True
    mostrar_e = True
    mostrar_ba = False
    mostrar_bp = False

    camino_m = agente.encontrar_camino("Manhattan")
    camino_e = agente.encontrar_camino("Euclidiana")
    camino_ba = None
    camino_bp = None

    reloj = pygame.time.Clock()
    ejecutando = True

    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1:
                    mostrar_m = not mostrar_m
                    paso_actual = 0
                elif evento.key == pygame.K_2:
                    mostrar_e = not mostrar_e
                    paso_actual = 0
                elif evento.key == pygame.K_3:
                    mostrar_ba = not mostrar_ba
                    camino_ba = agente.encontrar_camino_ba() if mostrar_ba else None
                    paso_actual = 0
                elif evento.key == pygame.K_4:
                    mostrar_bp = not mostrar_bp
                    camino_bp = agente.encontrar_camino_bp() if mostrar_bp else None
                    paso_actual = 0
                elif evento.key == pygame.K_r:
                    laberinto = Laberinto()
                    agente = Agente(laberinto)
                    camino_m = agente.encontrar_camino("Manhattan")
                    camino_e = agente.encontrar_camino("Euclidiana")
                    camino_ba = agente.encontrar_camino_ba() if mostrar_ba else None
                    camino_bp = agente.encontrar_camino_bp() if mostrar_bp else None
                    paso_actual = 0
                    pausado = False
                elif evento.key == pygame.K_SPACE:
                    pausado = not pausado

        if not pausado:
            laberinto.actualizar(time.time())
            if any([
                camino_m and camino_m[-1] != laberinto.pos_objetivo,
                camino_e and camino_e[-1] != laberinto.pos_objetivo,
                camino_ba and camino_ba[-1] != laberinto.pos_objetivo,
                camino_bp and camino_bp[-1] != laberinto.pos_objetivo
            ]):
                agente.laberinto = laberinto
                if mostrar_m:
                    camino_m = agente.encontrar_camino("Manhattan")
                if mostrar_e:
                    camino_e = agente.encontrar_camino("Euclidiana")
                if mostrar_ba:
                    camino_ba = agente.encontrar_camino_ba()
                if mostrar_bp:
                    camino_bp = agente.encontrar_camino_bp()
                paso_actual = 0

        dibujar_laberinto(laberinto,
                          camino_m if mostrar_m else None,
                          camino_e if mostrar_e else None,
                          camino_ba if mostrar_ba else None,
                          camino_bp if mostrar_bp else None)
        dibujar_panel_superior(mostrar_m, mostrar_e, mostrar_ba, mostrar_bp)

        if pausado:
            pausa_texto = fuente_titulo.render("PAUSA", True, ROJO)
            pantalla.blit(pausa_texto, (ANCHO_VENTANA // 2 - pausa_texto.get_width() // 2,
                                        ALTO_VENTANA // 2 - pausa_texto.get_height() // 2))

        pygame.display.flip()
        reloj.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
