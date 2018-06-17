#   Proyecto de Laboratorio de Algoritmos 1
#   Entrega 1
#   Autores:
#   Gustavo Castellanos 14-10192
#   Yuni Quintero       14-10880

import pygame, sys
from pygame.locals import *
from copy import deepcopy

# colors
CHIFFON = (255, 250, 205)
BROWN = (139, 69, 19)
GRAY = (190, 190, 190)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
VEN = (50, 0 , 0)
WHITE = (255, 255, 255)
TAN = (210, 180, 140)
GOLD = (255, 215, 0)

#constant strings
MAIN = "Menu Principal"
INGAME = "Menu de Juego"
START = "Pantalla de Inicio"
OPTION = "Menu de opcion de carga"
NEW = "Partida Nueva"   
LOAD = "Cargar Partida"
SAVE = "Guardar Partida para regresar al menu principal" 
CHESS = "Cargar tablero"
ON = "on"
OFF = "off"
INVALID = "Entrada invalida."
WIN = "HAS GANADO \o/"
LOSE = "HAS PERDIDO :/"
LEAVE = "Confirmar salida del juego"

#bounds
Wth = 600 #width
Hht = 650 #height
lowMenu = (0, 440, 600, 160)
leftMenu = (0, 0, 160, 440)
frame = (160, 0, 440, 440)
board = (180, 20, 400, 400)
boxSize = 100

minuto = 60
FPS = 60
fpsClock = pygame.time.Clock()

assert lowMenu[0]+lowMenu[2] == 600 and lowMenu[1] + lowMenu[3] == 600, "Dimensiones de lowMenu malas"

def main():

    #Funcion principal del juego

    pygame.init()

    global count, piezas, textMode, movement, window, dispSurf, font, font2, getuser, userName, TEXTRECT, option, \
    level, animation, chess, grid, contD, contR, contP, contA, contT, contC, cont, FINISHED, TIMER, sec, states

    jugar = False

    states = []

    FINISHED = False

    TIMER = 0
    sec = 0

    count = 0
    piezas = 0
    movement = ""
    chess = ""
    textMode = OFF

    grid = []
    count = 1
    for i in range(4):
        grid.append([])
        for j in range(4):
            grid[i].append("Z")

    animation = 0
    
    window = START
    getuser = False
    userName = ""
    option = None
    dispSurf = pygame.display.set_mode((Wth, Hht))
    font = pygame.font.Font("freesansbold.ttf", 14)
    font2 = pygame.font.Font("freesansbold.ttf", 27)
    pygame.display.set_caption("Solitaire Chess")

    while True:
        #background
        dispSurf.fill(TAN)
        
        if window == MAIN:
            genMain()

        elif window == LEAVE:
        	genLeave()

        elif window == OPTION:
            genOption()

        elif window == NEW:
            genNew()
            
        elif window == CHESS:
            genNew()
            printInBox2(chess)

        elif window == LOAD:
            genLoad()
            
        elif window == INGAME:
            genGame(level)

            if jugar == True:
                printBoard()
                printInBox(movement)
                if cont == 1:
                    genFinish(WIN)
                    FINISHED = True
                elif TIMER == 0:
                    genFinish(LOSE)
                    FINISHED = True

            
        elif window == START:
            genStart()
            getUser(None)

        elif window == SAVE:
            genSave()

        # Events    
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if FINISHED == True:
                continue

            # KEYDOWN
            elif event.type == KEYDOWN:
                #START MENU
                if (window == START):
                    getUser(event)

                #MAIN MENU
                elif (window == MAIN):
                    if event.key == K_1:
                        window = OPTION
                    elif event.key == K_2:

                        print("Esta opcion aun no esta disponible.")
                        continue

                        window = LOAD
                    elif event.key == K_3:
                        window = LEAVE
                    elif event.key == K_0: 
                        userName = ""
                        window = START
                    elif event.key == K_4:
                    	print("Esta opcion aun no esta disponible")
                    	continue

                #LEAVE MENU
            	elif (window == LEAVE):
            		if event.key == K_0 or event.key == K_2:
            			window = MAIN
            		elif event.key == K_1:
            			pygame.quit()
                		sys.exit()

                #LOAD MENU 
                elif (window == LOAD):
                    if event.key == K_0:
                        window = MAIN

                # OPTION MENU
                elif (window == OPTION):
                    if event.key == K_1:

                        print("Esta opcion aun no esta disponible.")
                        continue

                        option = "random"
                        window = NEW
                        
                    elif event.key == K_2:

                        option = "user"
                        window = NEW

                    elif event.key == K_0:
                        window = MAIN

                # NEW GAME MENU
                elif (window == NEW):
                    if event.key == K_1:

                        print("Esta opcion aun no esta disponible.")
                        continue

                        level = 1
                        TIMER = -1
                        if option == "user":
                            window = CHESS
                        else:
                            window = INGAME
                    elif event.key == K_2:
                        level = 2
                        TIMER = 3*minuto
                        if option == "user":
                            window = CHESS
                        else:
                            window = INGAME
                    elif event.key == K_3:
                        level = 3
                        TIMER = 3*minuto/2
                        if option == "user":
                            window = CHESS
                        else:
                            window = INGAME
                    elif event.key == K_4:

                        print("Esta opcion aun no esta disponible.")
                        continue

                        level = 4
                        TIMER = 2*minuto
                        if option == "user":
                            window = CHESS
                        else:
                            window = INGAME
                    elif event.key == K_0:
                        window = OPTION

                #CHESS:
                elif window == CHESS:
                    if event.key != K_RETURN:
                        if event.key == K_BACKSPACE:
                            if len(chess) > 0 and chess != INVALID: 
                                chess = chess[:-1]

                        elif event.key == K_0:
                            window = NEW
                            chess = ""

                        else:
                            if event.unicode not in "ATCDRabcd1234-":
                                continue
                            if chess == INVALID:
                                chess = ""
                            chess += event.unicode
                        printInBox2(chess)
                    elif len(chess) > 0:
                        try:
                            genBoard()
                        except:
                            chess = INVALID
                            contD, contR, contP, contA, contT, contC, cont = 0,0,0,0,0,0,0
                            emptyBoard()
                            continue

                        window = INGAME
                        grid2 = deepcopy(grid)
                        states.append(grid2)
                        genGame(level)
                        printBoard()

                #INGAME MENU
                elif (window == INGAME):
                    if textMode == ON:
                        if event.key != K_RETURN:
                            if event.key == K_6:
                                movement = ""
                                textMode = OFF
                                continue
                            if event.key == K_BACKSPACE:
                                if len(movement) > 0 and movement != INVALID: 
                                    movement = movement[:-1]
                            else:
                                if event.unicode not in "abcd1234-" or (len(movement) >= 5 and movement != INVALID):
                                    continue
                                if movement == INVALID:
                                    movement = ""
                                movement += event.unicode
                            printInBox(movement)

                        elif len(movement) > 0:
                            getMovement()

                    elif event.key == K_6:
                        textMode = ON
                        movement = ""

                    elif event.key == K_4:
                        if (level == 2 or level == 3):
                            window = SAVE
                        else:
                            window = MAIN
                        emptyBoard()

                    elif event.key == K_1 and jugar == False:
                        jugar = True


                    #NUEVO
                    elif event.key == K_3 and (level == 1 or level == 2) and len(states) > 1:
                        states = states[:-1]
                        grid = states[len(states) - 1]
                        cont += 1




                #SAVE
                elif (window == SAVE):
                    if event.key == K_1:
                        #si decide guardar(poner una confirmacion)
                        print("Esta opcion aun no esta disponible.")
                        continue
                        chess = ""
                        window = MAIN
                    elif event.key == K_2:
                        #se decide no guardar
                        chess = ""
                        window = MAIN
                    elif event.key == K_0: 
                        window = INGAME


        pygame.display.update()

        fpsClock.tick(FPS)
        animation = (animation+1)%(2*FPS)

        if window == INGAME and FINISHED == False and jugar == True:
            sec = (sec+1)%FPS
            if sec == 0:
                TIMER -= 1

        if FINISHED == True:
            count = (count+1)%300
            if count == 0:
                emptyBoard()
                movement = ""
                chess = ""
                window = MAIN
                FINISHED = False
                count = 0
                states = []
                textMode = OFF
                jugar = False



def emptyBoard():

    #Funcion que inicializa la matriz global Grid en todas sus casillas con el caracter Z
    #que representa a una casilla sin pieza colocada por el usuario en el tablero

    global grid
    for i in range(4):
        for j in range(4):
            grid[i][j] = "Z"

def getAnim():

    # Funcion que genera las listas a utilizar para la animacion de la pantalla de inicio


    global animation, animations

    animations = []
    animations.append([])
    animations.append([])
    
    #animation I
    img = pygame.image.load("wpawn45.png")
    animations[0].append(img)
    
    img = pygame.image.load("brook45.png")
    animations[0].append(img)

    img = pygame.image.load("wqueen45.png")
    animations[0].append(img)
    
    img = pygame.image.load("bknight45.png")
    animations[0].append(img)

    img = pygame.image.load("wbishop45.png")
    animations[0].append(img)

    img = pygame.image.load("bking45.png")
    animations[0].append(img)

    #animation II
    
    img = pygame.image.load("bpawn45.png")
    animations[1].append(img)
    
    img = pygame.image.load("wrook45.png")
    animations[1].append(img)

    img = pygame.image.load("bqueen45.png")
    animations[1].append(img)
    
    img = pygame.image.load("wknight45.png")
    animations[1].append(img)

    img = pygame.image.load("bbishop45.png")
    animations[1].append(img)

    img = pygame.image.load("wking45.png")
    animations[1].append(img)


def genAnim():

    #Funcion que genera la animacion presente al inicio del juego en la ventana START, permite que las
    #imagenes se intercambien cada segundo

    global animation, animations
    if animation < 60:
        k = 0
    else:
        k = 1
    x = 90
    y = 300
    for i in range(6):
        img = animations[k][i]
        imgRect = img.get_rect()
        imgRect.center = (x,y)
        dispSurf.blit(img, imgRect)
        if i == 0:
            y -= 150
        elif i == 1:
            x = Wth/2
            y = 50
        elif i == 2:
            x = Wth - 90
            y = 150
        elif i == 3:
            y = 300
        else:
            x = Wth/2
            y = 390
            
        
      
def genStart():

    #Funcion que imprime en la ventana START/Inicio el icono y titulo del juego, la animacion presente
    #y un cuadro de texto para que el usuario pueda ingresar su nombre y asi iniciar sesion

    global TEXTRECT, animation

    #Animation
    genAnim()
    
    #LOGO
    logox = Wth/2
    logoy = Hht/2 - 100 
    logo = pygame.image.load('logo.png')
    logoRect = logo.get_rect()
    logoRect.center = (logox, logoy)
    dispSurf.blit(logo, logoRect)

    #TITLE
    ffont = pygame.font.Font("freesansbold.ttf", 50)
    textSurf = ffont.render("Solitaire Chess", True, WHITE)
    textRect = textSurf.get_rect()
    textRect.center = (logox, logoy)
    dispSurf.blit(textSurf, textRect)

    #Fill name
    ffont = pygame.font.Font("freesansbold.ttf", 20)
    textSurf = ffont.render("Ingrese nombre para iniciar sesion", True, WHITE)
    textRect = textSurf.get_rect()
    textRect.center = (logox, logoy + 230)
    dispSurf.blit(textSurf, textRect)

    #TextBox
    tBoxRect = textRect
    tBoxRect.centery += 30
    tBoxRect.width += 10 
    tBoxRect.height += 10
    pygame.draw.rect(dispSurf, BLACK, tBoxRect)
    tBoxRect.centery += 3
    tBoxRect.width -=5
    tBoxRect.height -=5
    tBoxRect.left += 2
    TEXTRECT = tBoxRect #Para que la variable global TEXTRECT mantenga las dimensiones y asi usarlas en otra funcion
    pygame.draw.rect(dispSurf, WHITE, tBoxRect)

def getUser(event):

    #Funcion que permite al usuario ingresar por teclado su nombre en la pantalla START/Inicio 

    global TEXRECT, userName, window
    try:
        if event != None and len(userName) > 0 and event.key == K_RETURN:
            window = MAIN
            return
        elif (event != None and event.key == K_BACKSPACE and len(userName) > 0):
            userName = userName[:-1]
        elif event != None and event.key != K_RETURN and event.key != K_BACKSPACE and len(userName) < TEXTRECT.width/8 - 4:
            userName += event.unicode
            if len(userName) == 0:
                return
    except:
        return
    ffont = pygame.font.Font("freesansbold.ttf", 16)
    textSurf = ffont.render(userName, True, BLACK)
    textRect = textSurf.get_rect()
    textRect.center = TEXTRECT.center
    dispSurf.blit(textSurf, textRect)


def genReturn():

    #Funcion que genera un cuadro de texto en la esquina inferior izquierda de una ventana. Indica al usuario
    #la tecla a presionar para regresar a la ventana anterior, siendo esta "0"

    x = 20
    y = 590
    pygame.draw.rect(dispSurf, VEN, (x, y, 120, 50))
    pygame.draw.rect(dispSurf, WHITE, (x + 10, y+10, 100, 30))
    textSurf = font.render("0. REGRESAR", True, BLACK, WHITE)
    textRect = textSurf.get_rect()
    textRect.topleft = (x+15, y+15)
    dispSurf.blit(textSurf, textRect)

def genSave():

    #Funcion que imprime en la ventana Save cuadros de texto que indican al usuario que
    #teclas presionar para decidir si guardar o no una partida antes de terminarla por completo y
    #regresar al menu principal

    boundUD = 200
    pygame.draw.rect(dispSurf, VEN, (0, boundUD, Wth, Hht - 2*boundUD))
    x = 40
    y = boundUD + 20
    #gen boxes
    #ffont = pygame.font.Font("freesansbold.ttf", 30)
    for i in range(2):
        pygame.draw.rect(dispSurf, WHITE, (x, y, 220, 210))

        if i == 0:
            genTitle3("1. Guardar Partida", x+110, Hht/2 - 30)
            
        elif i == 1:
            genTitle3("2. No Guardar", x+110, Hht/2 - 30)
            genTitle3("Partida", x+110, Hht/2)
            
        x += 300

    genReturn()

def genLeave():

    #Funcion que imprime en la ventana LEAVE cuadros de texto que indican al usuario que
    #teclas presionar para decidir si salir completamente o no del juego
    global font2
    boundUD = 200
    pygame.draw.rect(dispSurf, VEN, (0, boundUD, Wth, Hht - 2*boundUD))
    x = 40
    y = boundUD + 20
    #gen boxes
    for i in range(2):
        pygame.draw.rect(dispSurf, WHITE, (x, y, 220, 210))

        if i == 0:
            genTitle2("1. Si :(", x+110, Hht/2 - 15)
            
        elif i == 1:
            genTitle2("2. No :)", x+110, Hht/2 - 15)
            
        x += 300

    textSurf = font2.render("Desea salir de Solitaire Chess?",True, BLACK)
    textRect = textSurf.get_rect()
    textRect.left = 100
    textRect.top = 100
    dispSurf.blit(textSurf, textRect)

    genReturn()


def genMain():

    #Funcion que imprime en la ventana MAIN/Menu Principal cuadros de texto que indican al usuario que
    #teclas presionar para escoger si jugar una partida nueva, cargar una partida pasada, mostrar records o salir del juego.

    boundUD = 200
    pygame.draw.rect(dispSurf, VEN, (0, boundUD, Wth, Hht - 2*boundUD))
    x = 20
    y = boundUD + 20
    #gen boxes
    for i in range(3):
        pygame.draw.rect(dispSurf, WHITE, (x, y, 160, 210))

        if i == 0:
            genTitle2("1. Nueva", x+80, Hht/2 - 30)
            genTitle2("Partida", x+80, Hht/2)
            genImg("wking45.png", x+80, Hht/2 + 35)
            
        elif i == 1:
            genTitle2("2. Cargar", x+80, Hht/2 - 30)
            genTitle2("Partida", x+80, Hht/2)
            genImg("bqueen45.png", x+80, Hht/2 + 35)
        else:
            genTitle2("3. Salir", x+80, Hht/2 - 15)
            genImg("wunicorn45.png", x+80, Hht/2 + 35)
            
        x += 200

    x = 370
    y = 590
    pygame.draw.rect(dispSurf, VEN, (x, y, 200, 50))
    pygame.draw.rect(dispSurf, WHITE, (x + 10, y+10, 180, 30))
    textSurf = font.render("4. MOSTRAR RECORDS", True, BLACK, WHITE)
    textRect = textSurf.get_rect()
    textRect.topleft = (x+15, y+15)
    dispSurf.blit(textSurf, textRect)

    genReturn()


def genImg(image, x, y):

    #Funcion que permite insertar una imagen en la pantalla, recibiendo como parametros
    #el string que contiene el nombre del archivo de la imagen y sus coordenadas cartesianas x e y
    #para posicionar la imagen
    try:
        assert(type(image)==str and type(x)==int and type(y)==int and 0<=x<=600 and 0<=y<=650)
        img = pygame.image.load(image)
        imgRect = img.get_rect()
        imgRect.centerx = x
        imgRect.top = y
        dispSurf.blit(img, imgRect)
    except:
        print("Parametro invalido")
        sys.exit()

def genOption():

    #Funcion que imprime en la ventana OPTION cuadros de texto que indican al usuario que
    #teclas presionar para escoger el modo de carga de tablero, si se genera un tablero aleatorio
    #o permitir al usuario cargar su propio tablero para juagr una partida nueva.

    boundUD = 200
    pygame.draw.rect(dispSurf, VEN, (0, boundUD, Wth, Hht - 2*boundUD))
    x = 40
    y = boundUD + 20
    #gen boxes
    #ffont = pygame.font.Font("freesansbold.ttf", 30)
    for i in range(2):
        pygame.draw.rect(dispSurf, WHITE, (x, y, 220, 210))

        if i == 0:
            genTitle3("1. Generar tablero", x+110, Hht/2 - 30)
            genTitle3("aleatorio", x+110, Hht/2)
            genImg("wking45.png", x+110, Hht/2 + 35)
            
        elif i == 1:
            genTitle3("2. Cargar tablero", x+110, Hht/2 - 30)
            genTitle3("desde teclado", x+110, Hht/2)
            genImg("bqueen45.png", x+110, Hht/2 + 35)
            
        x += 300

    genReturn()

def genNew():

    #Funcion que imprime en la ventana NEW/Partida Nueva cuadros de texto que indican al 
    #usuario que teclas presionar para elegir la dificultad de la partida a jugar y donde se
    #cargara el tablero por teclado

    global font, font2, option, window
    boundUD = 150
    pygame.draw.rect(dispSurf, VEN, (0, boundUD, Wth, Hht - 2*boundUD))
    
    x = 20
    y = boundUD + 20
    #gen boxes
    for i in range(2):
        pygame.draw.rect(dispSurf, WHITE, (x, y, 260, 135))
        pygame.draw.rect(dispSurf, WHITE, (x, y + 175, 260, 135))
        
        if i == 0:
            genTitle2("1. Entrenamiento", x+130, y + 135/2 - 13)
            genTitle2("3. Dificil", x+130, y + 175 + 135/2 - 13)
            
        elif i == 1:
            genTitle2("2. Facil", x+130, y + 135/2 - 13)
            genTitle2("4. Muy dificil", x+130, y + 175 + 135/2 - 13)
        
        x += 300
    y = Hht - boundUD
    if option == "user" and window == CHESS:
        textSurf = font.render("Ingrese tablero: ", True, BLACK)
        textRect = textSurf.get_rect()
        textRect.top = y
        textRect.centerx = Wth/2
        dispSurf.blit(textSurf, textRect)

    genReturn()

def printInBox2(word):

    #Funcion que imprime en pantalla el tablero que el usuario carga por teclado, el cual es el parametro
    #de tipo string que recibe la funcion 

    global font2
    y = Hht - 130
    textSurf = font2.render(word, True, BLACK)
    textRect = textSurf.get_rect()
    textRect.top = y
    textRect.centerx = Wth/2
    dispSurf.blit(textSurf, textRect)

def getNumber(a):

    '''
    Funcion que le asigna a las letras en el conjunto A = {a,b,c,d} un entero del intervalo [1, 4].
    Si la letras no esta en A, aborta, i.e, bad := True
    '''

    global bad
    bad = False
    if a not in "abcd":
        bad = True
        return
    if a == "a":
        return 1
    elif a == "b":
        return 2
    elif a == "c":
        return 3
    elif a == "d":
        return 4

def genBoard():

    #Funcion que a partir de un string ingresado por el usuario que contiene las piezas a cargar y sus
    #respectivas posiciones en el tablero, modifica la matriz "grid" inicializada con caracteres Z e
    #inserta los caracteres P,D,R,A,T,C en las posiciones respectivas de la matriz donde no haya sido modificada
    #anteriormente, esto permite que la funcion verifique que no se introduzca mas de una pieza en una misma posicion.
    #Ademas, la funcion verifica la cantidad de piezas necesarias y suficientes para que el tablero cargado sea valido 
    #y que el string ingresado sea valido en cuanto al formato de entrada para el tablero

    global chess, option, grid, window, contD, contR, contP, contA, contT, contC, cont
    contD, contR, contP, contA, contT, contC, cont = 0,0,0,0,0,0,0
    if option == "user":
        piezas = chess.split("-")
        for p in piezas:
            if p[0] == 'a' or p[0] == "b" or p[0] == "c" or p[0] == "d":
                if grid[int(p[1])-1][getNumber(p[0])-1] != "Z" or len(p) != 2: 
                    5/0
                grid[int(p[1])-1][getNumber(p[0])-1] = "P"
                contP+=1
                cont+=1
            else:
                if (int(p[2]) == 0 or grid[int(p[2])-1][getNumber(p[1])-1] != "Z") or len(p) != 3:
                    5/0
                grid[int(p[2])-1][getNumber(p[1])-1] = p[0]
                if p[0]=='D':
                    contD+=1
                elif p[0]=='R':
                    contR+=1
                elif p[0]=='A':
                    contA+=1
                elif p[0]=='T':
                    contT+=1
                elif p[0]=='C':
                    contC+=1
                else:
                    5/0
                cont+=1
        if contD>1 or contR >1 or contP>2 or contA>2 or contT>2 or contC>2 or cont<2 or cont>10:
            5/0
                
        
    window = INGAME

def printBoard():

    #Funcion que imprime en pantalla el tablero cargado por el usuario mediante la matriz grid, el cual
    #indica en sus casillas que tipo de pieza se encuentra en una posicion determinada del tablero.
    #Iterando sobre la matriz, la funcion inserta una imagen que tiene por nombre de archivo el caracter distinto de Z presente en la 
    #casilla de la matriz en la posicion correspondiente segun los pixeles y la casilla de la matriz

    global grid
    for i in range(4):
        for j in range(4):
            if grid[i][j] != "Z":
                posx = getX(j)
                posy = getY(i)
                img = pygame.image.load("pieces/" + grid[i][j] + ".png")
                imgRect = img.get_rect()
                imgRect.center = (posx, posy)
                dispSurf.blit(img, imgRect)

def getX (n):

    #Funcion que devuelve en formato de pixeles la coordenada en el eje x para la imagen ij-esima de la funcion printBoard

    try:
        assert(type(n)==int and 0<=n<=600)
        borde = 230
        return borde + (boxSize)*n
    except:
        print("Parametro invalido")
        sys.exit()

def getY (n):

    #Funcion que devuelve en formato de pixeles la coordenada en el eje y para la imagen ij-esima de la funcion printBoard

    try:
        assert(type(n)==int and 0<=n<=650)
        borde = 370
        return borde - (boxSize)*n
    except:
        print("Parametro invalido")
        sys.exit()


def genLoad():

    #Funcion que inserta en la ventana LOAD un cuadro de texto que indica al usuario que 
    #esa herramienta no esta disponible

    global window
    textSurf = font2.render("Oops, " + window + " aun no esta disponible", True, RED)
    textRect = textSurf.get_rect()
    textRect.center = (Wth/2, Hht/2)
    dispSurf.blit(textSurf, textRect)
    genReturn()
        

def genGame(level):

    #Funcion que imprime en la ventana INGAME/menu de juego cuadros de texto e imagenes que indican al 
    #usuario que teclas presionar para habilitar cargar movimientos por teclado, jugar, Pausar el juego, 
    #deshacer jugadas y terminar la partida, indicadores del nombre del jugador, el nivel que se esta 
    #jugando y el tiempo disponible para jugar
    try:
        assert(type(level) == int and (level==1 or level==2 or level==3 or level==4))
        global option, textMode
        getBoard()
        pygame.draw.rect(dispSurf, VEN, (0, 440, 600, 150))
        corner=20
        for i in range(4):
            pygame.draw.rect(dispSurf, WHITE, (corner, 460, 110, 110))
            corner+=150
        
        font2 = pygame.font.Font("freesansbold.ttf", 18)

        # 1. JUGAR
        #JUGAR
        genTitle("1. JUGAR",75,470)
        genIcon('play.png',75,525)

        # 2. PAUSAR
        #PAUSAR
        genTitle("2. PAUSAR",75+150,470)
        genIcon('pause.png',225,528)

        # 3. DESHACER
        #DESHACER
        genIcon('deshacer.jpg',375,525)
        genTitle("3. DESHACER",375,470)

        # 4. TERMINAR
        #TERMINAR
        genTitle("4. TERMINAR",75+450,470)
        genIcon('end.png',525,529)

        #Left Menu
        boundUD = 70
        boundLR = 20
        y = boundUD
        for i in range(3):
            pygame.draw.rect(dispSurf, VEN, (boundLR, y, 120, 100))
            pygame.draw.rect(dispSurf, WHITE, (boundLR + 10, y+10, 100, 80))
            if i==0:
                genTitle("PARTIDA DE",80,y+15)
            if i==1:
                genTitle("NIVEL",80,y+15)
            if i==2:
                genTitle("TIEMPO",80,y+15)
            y += 120

            
        printName(80, 125)
            
        if level == 1:
            genTrain()
        elif level == 2:
            genEasy()
        elif level == 3:
            genHard()
        else:
            genVHard()

        genTimer()

        textSurf = font.render("Formato: posInicial-posFinal",True, BLACK)
        textRect = textSurf.get_rect()
        textRect.left = 370
        textRect.top = 597
        dispSurf.blit(textSurf, textRect)
        
        if textMode == OFF:
            textSurf = font.render("Ingrese 6 para entrar en modo de Ingreso de Jugada.", True, BLACK)
            textRect = textSurf.get_rect()
            textRect.left = 3
            textRect.top = 597
            dispSurf.blit(textSurf, textRect)
        else:
            textSurf = font.render("Ingrese 6 para salir del modo de Ingreso de Jugada.", True, BLACK)
            textRect = textSurf.get_rect()
            textRect.left = 3
            textRect.top = 597
            dispSurf.blit(textSurf, textRect)
    except:
        print("Parametro invalido")
        sys.exit()



def genTimer():

    #Funcion que genera un temporizador o reloj en cuenta regresiva en la ventana INGAME/menu de juego
    #que le indica al usuario el tiempo disponible para resolver el juego, convirtiendose el texto que 
    #indica el tiempo en rojo cuando este es menor a 30 segundos

    global TIMER
    x = 80
    y = 350
    timer = ""
    if TIMER/60 < 10:
        timer += "0"
    timer += str(TIMER/60) + ":"

    if TIMER%60 < 10:
        timer += "0"
    timer += str(TIMER%60)

    if TIMER > 30:
        color = BLACK

    else:
        color = RED

    textSurf = font2.render(timer, True, color, WHITE)
    textRect = textSurf.get_rect()
    textRect.centerx = x
    textRect.top = y
    dispSurf.blit(textSurf, textRect)


def getMovement():

    #Funcion que valida, apoyandose en la funcion valid, si la jugada ingresada por el usuario es correcta; de serlo, actualiza la matriz
    #segun la jugada

    global movement, bad, grid, cont, states
    boxes = movement.split("-")

    try:
        pos1 = (int(boxes[0][1]) - 1, getNumber(boxes[0][0]) - 1)
        pos2 = (int(boxes[1][1]) - 1, getNumber(boxes[1][0]) - 1)
    except:
        movement = INVALID
        return

    if (grid[pos1[0]][pos1[1]] == "Z" or grid[pos2[0]][pos2[1]] == "Z") or (not valid(pos1,pos2)) or\
    bad == True or pos1 == pos2 or len(boxes[0]) != 2 or len(boxes[1]) != 2 or len(movement) < 5:
        movement = INVALID
        return

    grid[pos2[0]][pos2[1]] = grid[pos1[0]][pos1[1]]
    grid[pos1[0]][pos1[1]] = "Z"
    movement = ""
    cont -= 1

    grid2 = deepcopy(grid)
    states.append(grid2)


def printInBox(word):

    #Funcion que imprime en pantalla los movimientos de las piezas que el usuario carga por teclado, el cual es el parametro
    #de tipo string que recibe la funcion 

    global font2
    textSurf = font2.render(word, True, BLACK)
    textRect = textSurf.get_rect()
    textRect.bottom = Hht - 3
    textRect.left = 3
    dispSurf.blit(textSurf, textRect)


def valid(pos1, pos2):

    #Funcion que valida las jugadas de cada pieza presente en el tablero de acuerdo a las reglas del Ajedrez Solitario

    p1 = grid[pos1[0]][pos1[1]]
    p2 = grid[pos2[0]][pos2[1]]

    ret = True

    # 0 is Y, 1 is X
    if p2 == "R":
        return False
    if p1 == "A":
        return abs(pos1[0]-pos2[0]) == abs(pos1[1] - pos2[1])
    if p1 == "T":

        # Para ver si no hay una pieza entre p1 y p2

        if pos2[0] != pos1[0]:
            if pos2[0] > pos1[0]: 
                add = 1
            else:
                add = -1
            i = pos1[0] + add

            # {inv: ret == no (Existe i | pos1[0] < i < pos2[0] or pos1[0] > i > pos2[0]: grid[i][pos1[1]] != "Z")}
            while i != pos2[0] and i < 4 and i >= 0: # {Cota: |pos2[0] - i|}
                if grid[i][pos1[1]] != "Z":
                    ret =  False
                i += add

        elif pos2[1] != pos1[1]:
            if pos2[1] > pos1[1]:
                add = 1
            else:
                add = -1
            i = pos1[1] + add

            # {inv: ret == no (Existe i | pos1[1] < i < pos2[1] or pos1[1] > i > pos2[1] : grid[pos1[0]][i != "Z")}
            while i != pos2[1] and i < 4 and i >= 0: # {Cota: |pos2[1] - i|}
                if grid[pos1[0]][i] != "Z":
                    ret =  False
                i += add

        return (pos1[0] == pos2[0] or pos1[1] == pos2[1]) and ret

    if p1 == "P":
        return pos2[0] == pos1[0] + 1 and abs(pos2[1] - pos1[1]) == 1
    if p1 == "D":
        return (abs(pos1[0]-pos2[0]) == abs(pos1[1] - pos2[1])) or (pos1[0] == pos2[0] or pos1[1] == pos2[1])
    if p1 == "R":
        return (abs(pos1[0] - pos2[0]) == 1 and pos1[1] == pos2[1]) or (pos1[0] == pos1[0] and abs(pos1[1] - pos2[1]) == 1)
    if p1 == "C":
        return (abs(pos1[1] - pos2[1]) == 1 and abs(pos1[0] - pos2[0]) == 2) or \
        (abs(pos1[1] - pos2[1]) == 2 and abs(pos1[0] - pos2[0]) == 1)


        

def genIcon(pic,x,y):

    #Funcion que permite insertar una imagen en la pantalla, recibiendo como parametros
    #el string que contiene el nombre del archivo de la imagen y sus coordenadas cartesianas x e y
    #para posicionar la imagen
    try:
        assert(type(x) == int and type(y) == int and type(pic) == str and 0<=x<=600 and 0<=y<=650)
        icon=pygame.image.load(pic)
        r=icon.get_rect()
        r.center=(x,y)
        dispSurf.blit(icon,r)
    except:
        print("Parametro invalido")
        sys.exit()

def genTitle(title,x,y):

    #Funcion que permite insertar un cuadro de texto en la pantalla, recibiendo como parametros
    #el string que contiene el texto a mostrar y las coordenadas cartesianas x e y
    #para posicionar el cuadro de texto. Esta funcion imprime un mensaje con un tamano de fuente de 27
    #mediante la variable global font
    try:
        assert(type(x) == int and type(y) == int and type(title) == str and 0<=x<=600 and 0<=y<=650)
        textSurf = font.render(title, True, BLACK, WHITE)
        textRect = textSurf.get_rect()
        textRect.centerx = x
        textRect.top = y
        dispSurf.blit(textSurf, textRect)
    except:
        print("Parametro invalido")
        sys.exit()

def genTitle2(title,x,y):

    #Funcion que permite insertar un cuadro de texto en la pantalla, recibiendo como parametros
    #el string que contiene el texto a mostrar y las coordenadas cartesianas x e y
    #para posicionar el cuadro de texto. Esta funcion imprime un mensaje con un tamano de fuente de 27
    #mediante la variable global font2
    try:
        assert(type(x) == int and type(y) == int and type(title) == str and 0<=x<=600 and 0<=y<=650)
        textSurf = font2.render(title, True, BLACK, WHITE)
        textRect = textSurf.get_rect()
        textRect.centerx = x
        textRect.top = y
        dispSurf.blit(textSurf, textRect)
    except:
        print("Parametro invalido")
        sys.exit()

def genTitle3(title, x, y):

    #Funcion que permite insertar un cuadro de texto en la pantalla, recibiendo como parametros
    #el string que contiene el texto a mostrar y las coordenadas cartesianas x e y
    #para posicionar el cuadro de texto. Esta funcion imprime un mensaje con un tamano de fuente de 27
    #mediante la variable local font3
    try:
        assert(type(x) == int and type(y) == int and type(title) == str and 0<=x<=600 and 0<=y<=650)
        font3 = pygame.font.Font("freesansbold.ttf", 23)
        textSurf = font3.render(title, True, BLACK, WHITE)
        textRect = textSurf.get_rect()
        textRect.centerx = x
        textRect.top = y
        dispSurf.blit(textSurf, textRect)
    except:
        print("Parametro invalido")
        sys.exit()


def genTrain():

    #Funcion que inserta en la ventana de juego del nivel Entrenamiento tres cuadros de texto que indican 
    #al usuario la tecla a presionar para revelar la solucion del tablero, el tiempo disponible y el nivel de 
    #la partida

    tumblr=(50,70,105)
    pygame.draw.rect(dispSurf, tumblr, (20, 10, 120, 50))
    pygame.draw.rect(dispSurf, WHITE, (30, 20, 100, 30))
    textSurf = font.render("0. SOLUCION", True, BLACK, WHITE)
    textRect = textSurf.get_rect()
    textRect.topleft = (35, 25)
    dispSurf.blit(textSurf, textRect)
    genIcon('inf.jpg',80,365)
    genTitle2("TRAIN",80,230)

def printName(x,y):

    #Funcion que imprime en la ventana INGAME/menu de juego un cuadro de texto 
    #que contiene el nombre que cargo el usuario al inicio del juego y asi este poder visualizar 
    #su nombre durante la partida
    try:
        assert(type(x) == int and type(y) == int and 0<=x<=600 and 0<=y<=650)
        ffont = pygame.font.Font("freesansbold.ttf", 18)
        name = userName
        if len(userName) >= 8:
            name = userName[0:6] + "..." 
        textSurf = ffont.render(name, True, BLACK, WHITE)
        textRect = textSurf.get_rect()
        textRect.center = (x,y)
        dispSurf.blit(textSurf, textRect)
    except:
        print("Parametro invalido")
        sys.exit()
    
def genEasy():

    #Funcion que inserta en la ventana de juego del nivel Facil un cuadro de texto que indica 
    #al usuario el nivel de la partida

    genTitle2("FACIL",80,230)

def genHard():

    #Funcion que inserta en la ventana de juego del nivel Dificil un cuadro de texto que indica 
    #al usuario el nivel de la partida y una imagen que indica al usuario que no puede deshacer jugadas

    genTitle2("DIFICIL",80,230)
    genIcon('undone.png',375,525)

def genVHard():

    #Funcion que inserta en la ventana de juego del nivel Muy Dificil un cuadro de texto que indica 
    #al usuario que esa dificultad aun no esta disponible para ser jugado

    global window
    textSurf = font2.render("Oops, esta dificultad aun no esta disponible", True, RED)
    textRect = textSurf.get_rect()
    textRect.center = (Wth/2, Hht/2)
    dispSurf.blit(textSurf, textRect)
    
def getBoard():

    #Funcion que imprime la estructura de un tablero de ajedrez de dimension 4x4 en la ventana INGAME/menu de juego
    #y los indicadores de las posiciones de cada fila y columna

    x = board[0]
    y = board[1]
    for i in range(4):
        textSurf = font.render(str(4-i), True, VEN, TAN)
        textRect = textSurf.get_rect()
        textRect.topleft = (165, y+45)
        dispSurf.blit(textSurf, textRect)
        for j in range(4):
            if i%2 == 0:
                if j%2 == 0:
                    pygame.draw.rect(dispSurf, BROWN, (x,y, boxSize, boxSize))
                else:
                    pygame.draw.rect(dispSurf, CHIFFON, (x,y, boxSize, boxSize))
            else:
                if j%2 == 0:
                    pygame.draw.rect(dispSurf, CHIFFON, (x,y, boxSize, boxSize))
                else:
                    pygame.draw.rect(dispSurf, BROWN, (x,y, boxSize, boxSize))
            x += boxSize
        x = board[0]
        y += boxSize

    letras=['a','b','c','d']

    x=180

    for i in range(4):
        textSurf = font.render(letras[i], True, VEN, TAN)
        textRect = textSurf.get_rect()
        textRect.topleft = (x+45, 420)
        dispSurf.blit(textSurf, textRect)
        x+=100
        

def genFinish(word): 

    #Funcion que indica al usuario si gano o perdio la partida, mostrando un cuadro de texto en la 
    #ventana INGAME/menu de juego con el mensaje HAS GANADO si quedo una pieza en el tablero
    #y cuando ocurre lo contrario, se muestra el mensaje HAS PERDIDO cuando haya finalizado el tiempo.
    #Recibe como parametro un string que contiene el mensaje a mostrar en pantalla
    try:
        assert(type(word) == str)
        global count
        boundUD = 70
        if word == WIN:
            color = (23, 100, 255)
        else:
            color = BLACK

        rect = pygame.Surface((Wth, 60))
        rect.fill(color)
        dispSurf.blit(rect, (0, boundUD))

        ffont = pygame.font.Font("fonts/Fibon_Sans_Regular.otf", 40)
        textSurf = ffont.render(word, True, GOLD)
        textRect = textSurf.get_rect()
        textRect.centerx = (Wth/2)
        textRect.top = boundUD + 10
        dispSurf.blit(textSurf, textRect)
    except:
        print("Parametro invalido")
        sys.exit()

getAnim()                    
main()