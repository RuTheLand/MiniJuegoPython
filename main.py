import pygame
import random
import math
from pygame import mixer
import io

#Problema con las fuentes
def fuente_bytes(fuente):
    with open(fuente, "rb") as f:
        ttf_bytes = f.read()
    return io.BytesIO(ttf_bytes)

#arranque
pygame.init()

#musica
"""Music track: Last Summer by Aylex
Source: https://freetouse.com/music
No Copyright Vlog Music for Videos"""

mixer.music.load("Ayles_Last_Summer.mp3")
mixer.music.set_volume(0.15)
mixer.music.play(-1)

#pantalla
pantalla = pygame.display.set_mode((800,600))

#Cabecera
pygame.display.set_caption("Invasión Espacial")
icono = pygame.image.load("forma-de-juego-pixelada-de-ovni-alienigena.png")
pygame.display.set_icon(icono)

#Hitboxes
def hitbox (x1,y1,x2,y2):
    distancia = math.sqrt(((x2-x1)*(x2-x1))+((y2-y1)*(y2-y1)))
    if distancia < (30 - (dificultad * 0.1)):
        return True
    else:
        return False
#Puntos
puntos=0
f_b= fuente_bytes("freesansbold.ttf")
fuente = pygame.font.Font(f_b, 32)
t_x = 10
t_y = 10
dificultad=0

# Fin
t_end = pygame.font.Font(f_b, 70)

def end():
    te_end=t_end.render("GAME OVER", True, (255,0,0))
    pantalla.blit(te_end, (60,200))

#Mostrar puntos
def mostrar_puntos(x,y):
    texto= fuente.render(f"Puntos: {puntos}", True, (0,0,0))
    pantalla.blit(texto, (x,y))
    return int(puntos * 0.001)

#jugador
actor = pygame.image.load("cohete.png")
actor_x = 400
actor_y = 536
actor_cambio = 0

def actor_posicion(x,y):
    pantalla.blit(actor, (x, y))

#enemigo
def mov_e(n):
    if n == 0:
        return 1
    else:
        return n

e_icono = icono
e_x = []
e_y = []
e_cambio = []
def popeo():
    for e in range(4 + dificultad):
        e_x.append(random.randint(0,736))
        e_y.append(random.randint(20, 150))
        e_cambio.append((0.6 + (dificultad * 0.1)) * (mov_e(random.randint(-1,0))))

popeo()

def e_posicion(x,y):
    pantalla.blit(e_icono,(x,y))

#bala
b_icono = pygame.image.load("bala.png")    
b_x = actor_x
b_y = 500
pium = False

def b_posicion(x,y):
    pantalla.blit(b_icono, (x, y))
    return True

#loop juego
se_ejecuta = True
while se_ejecuta:

    pantalla.fill((155,155,155))

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            se_ejecuta = False
        
        if evento.type== pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                actor_cambio = -0.6
            if evento.key == pygame.K_RIGHT:
                actor_cambio = 0.6
            if evento.key == pygame.K_UP:
                if pium == False:
                    b_x = actor_x
                    pium = b_posicion(b_x,b_y)

        if evento.type== pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                actor_cambio = 0

    #Mov Jugador
    actor_x += actor_cambio
    if actor_x < 0:
        actor_x = 0
    elif actor_x > 736:
        actor_x= 736
    
    actor_posicion(actor_x, actor_y)

    #Mov Enemigo
    for e in range(4 + dificultad):

        #Fin
        if e_y[e] > 450:
            for k in range(4 + dificultad):
                e_y[k]=2000
            end()
            break

        #Movimiento
        e_x[e]+=e_cambio[e]
        if e_x[e] < 0:
            e_cambio[e]=0.6 + (dificultad * 0.1)
            e_y[e] += 16
        elif e_x[e] > 736:
            e_cambio[e]=-0.6 - (dificultad * 0.1)
            e_y[e] += 16
        
        #hiteo
        hit = hitbox(e_x[e],e_y[e],b_x,b_y)
        if hit:
            b_y = 472
            pium = False
            puntos += 100
            e_x[e] = random.randint(0,736)
            e_y[e] = random.randint(20, 150)

        e_posicion(e_x[e],e_y[e])
        if( dificultad > (len(e_x) - 4)):
            popeo()

    #Mov_bala
    if pium == True:
        b_y = b_y - 1 - (dificultad * 0.1)
        b_posicion(b_x,b_y)
        if b_y <= 0:
            pium = False
            b_y = 550


    dificultad = mostrar_puntos(t_x, t_y)
    
    
    

    pygame.display.update()
