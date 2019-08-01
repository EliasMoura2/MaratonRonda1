#!/usr/bin/env python
#-*- coding: utf-8 -*-
#Inicio Ronda 1 - 2019
#La librería Pygame debe estar instalada junto a Python 2.7.13 para que el código se ejecute. 
#Si no lo está, ir en Windows a la aplicación Símbolo del Sistema y con una conexión activa a Internet ejecutar el comando pip install pygame 

import pygame
import random

#Inicializamos la librería Pygame y demás variables
pygame.init()
pygame.font.init() 
pygame.display.set_caption("Maraton 2019 - Inicio Ronda 1")
pantalla= pygame.display.set_mode((1152,648))
tipografia = pygame.font.SysFont('Comic Sans MS', 18)
tipografiaGanaste=pygame.font.SysFont('Comic Sans MS', 26)

global nivelCompletado
colorVerde,colorAzul,colorBlanco,colorNegro, colorNaranja= (11,102,35),(0,0,255),(255,255,255),(0,0,0),(239,27,126)
cantidadDeCasillasPorLado=8 #Debe ser número par ya que la zona es un cuadrado
cantPixelesPorLadoCasilla=72
salirJuego = False
lstZonasProtegidas=[]

#Cargamos las imágenes
imgSuperTablet=pygame.image.load("supertablet.png")
imgPared=pygame.image.load("pared.png")
listaAmenazas  = ["amenaza1.png","amenaza2.png","amenaza3.png","amenaza4.png"]
imgAmenaza=pygame.image.load(str(random.choice(listaAmenazas)))
imgAreaProtegida=pygame.image.load("areaprotegida.png")

imgSuperTablet=pygame.transform.scale(imgSuperTablet, (cantPixelesPorLadoCasilla, cantPixelesPorLadoCasilla))
imgPared=pygame.transform.scale(imgPared, (cantPixelesPorLadoCasilla, cantPixelesPorLadoCasilla))
imgAmenaza=pygame.transform.scale(imgAmenaza, (cantPixelesPorLadoCasilla, cantPixelesPorLadoCasilla))
imgAreaProtegida=pygame.transform.scale(imgAreaProtegida, (cantPixelesPorLadoCasilla, cantPixelesPorLadoCasilla))

#Creamos el mapa del nivel y algunas operaciones para los elementos que se encuentran dentro de la zona de transporte
def crearZonaDeTransporte():

    zonaDeTransporte = [[0 for x in range(cantidadDeCasillasPorLado+1)] for y in range(cantidadDeCasillasPorLado+1)] 
    
    for i in range(1,cantidadDeCasillasPorLado+1):
        zonaDeTransporte[i][1] = 'pared'  
        zonaDeTransporte[i][cantidadDeCasillasPorLado] = 'pared'   
        zonaDeTransporte[1][i] = 'pared'  
        zonaDeTransporte[cantidadDeCasillasPorLado][i] = 'pared'   

    zonaDeTransporte[3][4] = 'jugador'
    zonaDeTransporte[5][4] = 'virus'      
    
    lstZonasProtegidas.append((7,4))

    return zonaDeTransporte

zonaDeTransporte=crearZonaDeTransporte()

def hayZonaProtegidaEn(x,y):
    punto=(x,y)
    return lstZonasProtegidas.__contains__(punto)

def posicionarElemento(elemento,x,y): 
    zonaDeTransporte[x][y]=elemento

def borrarElemento(x,y):
    zonaDeTransporte[x][y]=0
        
#Dibujamos la zona de transporte, fondo y reglas
def dibujarZonaDeTransporte():     
    cnt = 0
    for i in range(1,cantidadDeCasillasPorLado+1):
        for j in range(1,cantidadDeCasillasPorLado+1):
            if cnt % 2 == 0:
                pygame.draw.rect(pantalla, colorVerde,[cantPixelesPorLadoCasilla*j,cantPixelesPorLadoCasilla*i,cantPixelesPorLadoCasilla,cantPixelesPorLadoCasilla])
            else:
                pygame.draw.rect(pantalla, colorVerde, [cantPixelesPorLadoCasilla*j,cantPixelesPorLadoCasilla*i,cantPixelesPorLadoCasilla,cantPixelesPorLadoCasilla])        

            if (hayZonaProtegidaEn(j,i)==True):
                pantalla.blit(imgAreaProtegida, (cantPixelesPorLadoCasilla*j,cantPixelesPorLadoCasilla*i)) 
            if (zonaDeTransporte[j][i]=='jugador'):
               pantalla.blit(imgSuperTablet, (cantPixelesPorLadoCasilla*j,cantPixelesPorLadoCasilla*i)) 
            if (zonaDeTransporte[j][i]=='pared'):          
               pantalla.blit(imgPared, (cantPixelesPorLadoCasilla*j,cantPixelesPorLadoCasilla*i))
            if (zonaDeTransporte[j][i]=='virus'):
               pantalla.blit(imgAmenaza, (cantPixelesPorLadoCasilla*j,cantPixelesPorLadoCasilla*i))
            cnt +=1
        cnt-=1

    pygame.draw.rect(pantalla,colorBlanco,[cantPixelesPorLadoCasilla,cantPixelesPorLadoCasilla,cantidadDeCasillasPorLado*cantPixelesPorLadoCasilla,cantidadDeCasillasPorLado*cantPixelesPorLadoCasilla],1)       
    pygame.display.update()
    
def dibujarFondo():
    fondo = pygame.image.load("fondo.png")
    pantalla.blit(fondo, (0, 0))
    
def dibujarReglas():

    textoReglas = tipografia.render('Mover a Super Tablet con las flechas del teclado para que lleve los virus a las zonas protegidas.', False, colorBlanco)
    
    ancho=800
    alto=46
    x=350
    y=3
    pygame.draw.rect(pantalla,colorAzul,(x,y,ancho,alto))
    pantalla.blit(textoReglas,(x+5,y,ancho,alto))
    pygame.display.update()


def dibujarFelicitacion():
    global nivelCompletado

    x=50
    y=3
    ancho=240
    alto=46
    
    if (nivelCompletado==True):
        textoFelicitacion = tipografiaGanaste.render('GANASTE :)', False, colorBlanco)
    
    else:
        textoFelicitacion = tipografiaGanaste.render('Juego en curso', False, colorBlanco)
    
    pygame.draw.rect(pantalla,colorAzul,(x,y,ancho,alto))
    pantalla.blit(textoFelicitacion,(x+5,y,ancho,alto))
    pygame.display.update()

def dibujarTodo():
    dibujarFondo()
    dibujarZonaDeTransporte()
    dibujarReglas()
    pygame.display.update()

dibujarTodo()

#Creamos una operación que indique si el nivel fue solucionado
def estaSolucionado():
    global nivelCompletado

    cantvirusesSobreTomas=0

    for punto in lstZonasProtegidas:
        x=punto[0]
        y=punto[1]
        if zonaDeTransporte[x][y]=='virus':
            cantvirusesSobreTomas=cantvirusesSobreTomas+1       

    if (cantvirusesSobreTomas==len(lstZonasProtegidas)):
        nivelCompletado=True
    else:
        nivelCompletado=False

    dibujarFelicitacion()
    dibujarReglas()

#Creamos operaciones para mover a Super Tablet
def irALaDerecha():
    for i in range(1,cantidadDeCasillasPorLado):
        for j in range(1,cantidadDeCasillasPorLado):
            if (zonaDeTransporte[j][i]=='jugador'):
                if (zonaDeTransporte[j+1][i]==0):
                    posicionarElemento('jugador',j+1,i)
                    borrarElemento(j,i)
                    break
                if(zonaDeTransporte[j+1][i]=='virus') and not ((zonaDeTransporte[j+2][i]=='pared') or (zonaDeTransporte[j+2][i]=='virus')):
                    borrarElemento(j,i)
                    posicionarElemento('virus',j+2,i)
                    posicionarElemento('jugador',j+1,i)
                    break

def irALaIzquierda():
    for i in range(1,cantidadDeCasillasPorLado):
        for j in range(1,cantidadDeCasillasPorLado):
            if (zonaDeTransporte[j][i]=='jugador'):
                if (zonaDeTransporte[j-1][i]==0):
                    posicionarElemento('jugador',j-1,i)
                    borrarElemento(j,i)
                    break
                if(zonaDeTransporte[j-1][i]=='virus') and not ((zonaDeTransporte[j-2][i]=='pared') or (zonaDeTransporte[j-2][i]=='virus')):
                    borrarElemento(j,i)
                    posicionarElemento('virus',j-2,i)
                    posicionarElemento('jugador',j-1,i)
                    break
                    
#Creamos el bucle del juego
while not salirJuego:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            salirJuego = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                irALaDerecha()
            elif event.key == pygame.K_LEFT:
                irALaIzquierda()
        dibujarZonaDeTransporte()
        estaSolucionado()
pygame.quit()
quit()
