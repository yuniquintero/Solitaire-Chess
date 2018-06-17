#   Proyecto de Laboratorio de Algoritmos 1
#   Entrega 1
#   Autores:
#   Gustavo Castellanos 14-10192
#   Yuni Quintero       14-10880

import pygame, sys, random, time
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
BLUE_WIN = (23, 100, 255)
LIME = (50, 205, 50)
SNOW4 = (139, 137, 137)

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
SOLUTION = "Modo de Solucion"
RECORDS = "Mostrar records"

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

    global count, piezas, textMode, movement, window, dispSurf, font, font2, font3, getuser, userName, TEXTRECT, option, \
    level, animation, chess, grid, contD, contR, contP, contA, contT, contC, cont, FINISHED, TIMER, sec, states, posInicial, \
    solGrid, partida, lineaPartida, jugar, wins, temp, recordLv, pag, lastPage

    jugar = False

    states = []

    FINISHED = False

    TIMER = 0
    sec = 0

    wins = 0
    count = 0
    piezas = 0
    movement = ""
    chess = ""
    posInicial = ""
    partida = ""
    textMode = OFF
    temp = 0
    grid = []
    count = 1
    for i in range(4):
        grid.append([])
        for j in range(4):
            grid[i].append("Z")

    #NUEVO
    solGrid = []
    for i in range(4):
        solGrid.append([])
        for j in range(4):
            solGrid[i].append(0)

    animation = 0
    
    window = START
    getuser = False
    userName = ""
    option = None
    dispSurf = pygame.display.set_mode((Wth, Hht))
    font = pygame.font.Font("freesansbold.ttf", 14)
    font2 = pygame.font.Font("freesansbold.ttf", 27)
    font3 = pygame.font.Font("freesansbold.ttf", 20)
    pygame.display.set_caption("Solitaire Chess")

    while True:
        #background
        dispSurf.fill(TAN)
        
        if window == MAIN:
            init()
            genMain()

        elif window == LEAVE:
        	genLeave()

        elif window == RECORDS and recordLv == None:
            genNew()

            boundUD = 120
            x = Wth/2
            textSurf = font3.render("Escoja nivel para mostrar los records correspondientes:", True, BLACK)
            textRect = textSurf.get_rect()
            textRect.top = boundUD
            textRect.centerx = x
            dispSurf.blit(textSurf, textRect)

        elif window == RECORDS:
            showRecords()

        elif window == OPTION:
            genOption()

        elif window == NEW:
            genNew()
            
        elif window == CHESS:
            genNew()
            printInBox2(chess)

        elif window == LOAD:
            genMain()
            genLoad()
            printInBox3(partida)
            printInBox4(lineaPartida)
            
        elif window == INGAME:
            genGame(level)

            if jugar == True:
                printBoard()
                printInBox(movement)
                if cont == 1 and level == 4 and wins <3:
                    wins += 1
                    if wins == 3:
                        temp = 1
                    elif wins != 3:
                        emptyBoard()
                        randBoard()
                        genGame(level)
                        printBoard()
                elif (cont == 1 and level != 4) or (temp == 1):
                    genFinish(WIN)
                    FINISHED = True
                elif TIMER == 0:
                    genFinish(LOSE)
                    FINISHED = True

        elif window == SOLUTION:
            genGame(level)
            printBoard()
            printInBox(posInicial)
            
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
                        window = LOAD

                    elif event.key == K_3:
                        window = LEAVE

                    elif event.key == K_0: 
                        userName = ""
                        window = START

                    elif event.key == K_4:
                        window = RECORDS

                #RECORDS MENU
                elif window == RECORDS:
                    if (event.key == K_1 or event.key == K_2 or event.key == K_3 or event.key == K_4) and recordLv == None:
                        recordLv = event.unicode

                    elif recordLv != None and event.key == K_LEFT and pag > 1:
                        pag -= 1

                    elif recordLv != None and event.key == K_RIGHT and pag + 1 < lastPage:
                        pag += 1

                    elif event.key == K_0:
                        if recordLv == None:
                            window = MAIN
                        else:
                            recordLv = None
                            pag = 1
                        lastPage = 3

                #LEAVE MENU
            	elif (window == LEAVE):
            		if event.key == K_0 or event.key == K_2:
            			window = MAIN
            		elif event.key == K_1:
            			pygame.quit()
                		sys.exit()

                #LOAD MENU 
                elif (window == LOAD):
                    #NUEVO 11/dic/16, 2:14
                    if event.key != K_RETURN:

                        if event.key == K_0 and (len(partida) == 0 or partida == INVALID):
                            window = MAIN

                        elif event.key == K_BACKSPACE and len(partida) > 0 and partida != INVALID:
                            partida = partida[:-1]

                        elif ord(event.unicode) >= ord("0") and ord(event.unicode) <= ord("9"):

                            if event.unicode == "0" and (len(partida) == 0 or partida == INVALID):
                                continue

                            if partida == INVALID:
                                partida = ""

                            partida += event.unicode

                        printInBox3(partida)
                        lineaPartida = getGame(0)
                        printInBox4(lineaPartida)

                    elif len(partida) > 0:
                        getGame(1)

                # OPTION MENU
                elif (window == OPTION):
                    if event.key == K_1:

                        #print("Esta opcion aun no esta disponible.")
                        #continue

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
                        '''
                        print("Esta opcion aun no esta disponible.")
                        continue
                        '''

                        level = 1
                        TIMER = -1
                        if option == "user":
                            window = CHESS
                        else:
                            randBoard()
                            window = INGAME

                    elif event.key == K_2:
                        level = 2
                        TIMER = 3*minuto
                        if option == "user":
                            window = CHESS
                        else:
                            randBoard()
                            window = INGAME

                    elif event.key == K_3:
                        level = 3
                        TIMER = 3*minuto/2
                        if option == "user":
                            window = CHESS
                        else:
                            randBoard()
                            window = INGAME

                    elif event.key == K_4 and option == "random":
                        level = 4
                        TIMER = 2*minuto
                        randBoard()
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
                    if textMode == ON and jugar == True:
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

                    elif event.key == K_6 and jugar == True:
                        textMode = ON
                        movement = ""

                    elif event.key == K_4:
                        if level != 4 and level != 1:
                            window = SAVE
                        else:
                            window = MAIN
                            emptyBoard()
                            states = []
                        jugar = False

                    elif event.key == K_1:
                        jugar = True

                    #NUEVO
                    elif event.key == K_0 and level == 1 and jugar == True:
                        window = SOLUTION

                    elif event.key == K_3 and (level == 1 or level == 2) and len(states) > 1:
                        states = states[:-1]
                        grid = states[len(states) - 1]
                        cont += 1

                    #NUEVO
                    elif event.key == K_2 and level != 4 and level != 1:
                        jugar = False

                #NUEVO
                #SOLUTION
                elif (window == SOLUTION):
                    if event.key == K_0:
                        window = INGAME
                        posInicial = ""

                        for i in range(4):
                            for j in range(4):
                                solGrid[i][j] = 0


                    elif event.key != K_RETURN:
                        if event.unicode in "abcd1234" and (len(posInicial) < 2 or posInicial == INVALID):
                            if posInicial == INVALID:
                                posInicial = ""
                            posInicial += event.unicode
                        elif event.key == K_BACKSPACE and len(posInicial) > 0 and posInicial != INVALID:
                            posInicial = posInicial[:-1]

                    elif len(posInicial) == 2:
                        genSolution(posInicial)


                #SAVE
                elif (window == SAVE):
                    if event.key == K_1:
                        #si decide guardar(poner una confirmacion)
                        #print("Esta opcion aun no esta disponible.")
                        #continue

                        save()

                        chess = ""
                        window = MAIN
                        emptyBoard()
                        states = []
                    elif event.key == K_2:
                        #se decide no guardar
                        chess = ""
                        window = MAIN
                        emptyBoard()
                        states = []
                    elif event.key == K_0: 
                        window = INGAME


        pygame.display.update()

        fpsClock.tick(FPS)
        animation = (animation+1)%(2*FPS)

        if window == INGAME and FINISHED == False and jugar == True and level != 1:
            sec = (sec+1)%FPS
            if sec == 0:
                TIMER -= 1

        if FINISHED == True:
            count = (count+1)%300
            if count == 0:
                window = MAIN
                if cont == 1:
                	saveRecord()


#NUEVO 11/dic/16, 2:48
def init():
    '''
    Funcion que inicializa las variables globales necesarias
    '''
    assert True

    global movement, chess, window, FINISHED, count, states, states, textMode, jugar, partida, sec, lineaPartida, wins, temp, recordLv, pag, lastPage
    emptyBoard()
    temp = 0
    movement = ""
    chess = ""
    window = MAIN
    wins = 0
    FINISHED = False
    count = 0
    states = []
    textMode = OFF
    jugar = False
    partida = ""
    lineaPartida = ""
    sec = 0
    recordLv = None
    pag = 1
    lastPage = 3

    assert True

#NUEVO 12/dic/16, 21:05
def saveRecord():


    '''
    Funcion que guarda el record del usuario en el nivel correspondiente. Luego ordena la lista de records
    '''

    global userName, level
    assert len(userName) > 0 and str(level) in "1234", "userName vacio o level fuera de rango"

    f = open("records/" + str(level) + ".txt", "r")
    p = -1
    lineas = f.readlines()
    for i in range(len(lineas)):
        l = lineas[i].split(" ")
        if l[0] == userName:
            p = i

    if p == -1: #Crear record
        lineas.insert(0, userName + " 1 \n")
        n = 1
    else: #Actualizar record
        l = lineas[p].split(" ")
        n = int(l[1]) + 1
        l[1] = str(n)
        lineas[p] = l[0] + " " + l[1] + " \n"

    lineas.sort(key=getVictories, reverse=True)

    left = -1
    right = -1
    for i in range(len(lineas)) :
        l = lineas[i].split(" ")
        if left == -1 and int(l[1]) == n:
            left = i
            right = left
            continue
        if int(l[1]) == n:
            right = i

    #Ordenar lista
    lineas[left:right+1] = sorted(lineas[left:right+1], key=getUsername)

    f.close()

    f = open("records/" + str(level) + ".txt", "w")
    for l in lineas:
        f.write(l)

    f.close()

    assert f.closed, "file abierto"

#NUEVO 12/dic/16, 23:48
def showRecords():

    '''
    Funcion que imprime en pantalla la lista de records del nivel escogido. Si la lista de records es muy larga, 
    esta se divide en varias paginas. La variable pag indica en que pagina se encuentra el usuario y la variable
    lastPage indica el numero de la ultima pagina
    '''

    global recordLv, lastPage, pag

    assert recordLv in "1234", "recordLv fuera de rango"
    assert pag >= 1, "pag fuera de rango"
    assert pag <= lastPage, "pag y lastPage incorrectos: " + str(pag) + " > " + str(lastPage)

    if recordLv == "1":
        nivel = "Entrenamiento"
    elif recordLv == "2":
        nivel = "Facil"
    elif recordLv == "3":
        nivel = "Dificil"
    else:
        nivel = "Muy dificil"

    x = 10
    y = 70

    ffont = pygame.font.Font("freesansbold.ttf", 35)
    textSurf = ffont.render("Nivel " + nivel + ": ", True, VEN)
    textRect = textSurf.get_rect()
    textRect.topleft = (x, y - 66)
    dispSurf.blit(textSurf, textRect)

    ffont = pygame.font.Font("freesansbold.ttf", 15)
    textSurf = ffont.render("<usuario> <numero de victorias>", True, VEN)
    textRect = textSurf.get_rect()
    textRect.topleft = (x, y - 32)
    dispSurf.blit(textSurf, textRect)

    f = open("records/" + recordLv + ".txt", "r")
    lineas = f.readlines()
    right = 16*pag
    left = 16*pag - 16
    if right >= len(lineas):
        right = len(lineas)
        lastPage = pag #Para indicar que la pagina actual es la ultima pagina
    else:
        lastPage = pag + 2

    lineas = lineas[left: right]

    for l in lineas:
        l = l[:-1]
        textSurf = font2.render(l, True, BLACK)
        textRect = textSurf.get_rect()
        textRect.topleft = (x,y)
        dispSurf.blit(textSurf, textRect)
        y += 30

    genReturn()

    x = Wth/2
    y = Hht - 10

    if pag == 1:
        color = SNOW4
    else:
        color = BLUE_WIN

    textSurf = font.render("<- Retroceder pagina", True, color)
    textRect = textSurf.get_rect()
    textRect.left = x
    textRect.bottom = y
    dispSurf.blit(textSurf, textRect)

    x += textRect.width + 10

    if pag == lastPage:
        color = SNOW4
    else:
        color = BLUE_WIN

    textSurf = font.render("Avanzar pagina ->", True, color)
    textRect = textSurf.get_rect()
    textRect.left = x
    textRect.bottom = y
    dispSurf.blit(textSurf, textRect)

    assert True

def getVictories(linea):

    '''
    Funcion que devuelve el numero de victorias presente en linea
    '''

    assert len(linea) > 0, "linea vacia"

    l = linea.split(" ")

    assert len(l[1]) > 0

    return l[1]

def getUsername(linea):

    '''
    Funcion que devuelve en nombre de usuario presente en linea
    '''

    assert len(linea) > 0, "linea vacia"

    l = linea.split(" ")

    assert len(l[1]) > 0

    return l[0]

#NUEVO
def genSolution(pos):

    '''
    Funcion que recibe una posicion inicial de una pieza y guarda en la matriz solGrid las posibles posiciones finales
    '''

    global grid, solGrid, posInicial

    assert len(posInicial) > 0, "posInicial vacia"

    #Inicializar solGrid
    for i in range(4):
        for j in range(4):
            solGrid[i][j] = 0

    row = int(pos[1]) - 1
    col = getNumber(pos[0]) - 1

    p = grid[row][col]

    if p == "Z":
        posInicial = INVALID
        return

    posInicial = ""
    pos1 = (row, col)

    solGrid[row][col] = 2

    for i in range(4):
        for j in range(4):
            pos2 = (i,j)
            if pos2 == pos1:
                continue

            if valid(pos1, pos2):
                solGrid[i][j] = 1

    assert True


#NUEVO 11/dic/16, 1:21
def save():

    '''
    la cual a partir de la matriz grid, que contiene el estado actual del tablero con las piezas y posiciones respectivas, 
    genera una cadena de caracteres llamada tablero de la forma Pieza1Posicion1-Pieza2Posicion2- ... -PiezaNPosicionN, con 0 < N < 11.
    Esta cadena de caracteres nueva se escribe sobre partidasguardadas.txt junto con la fecha en que fue jugada la partida, 
    la ultima actualizacion del cronometro, el nivel y un numero que identifica a la partida.
    ''' 

    global grid, TIMER, level

    assert str(level) in "1234", "level fuera de rango"

    tablero = ""

    for i in range(4):
        for j in range(4):
            if grid[i][j] != "Z":
                if len(tablero) > 0:
                    tablero += "-"

                if grid[i][j] == "P":
                    c = ""
                else:
                    c = grid[i][j]

                tablero += c + getLetter(j) + str(i+1)


    f = open("partidasguardadas.txt", "r")
    lineas = f.readlines()

    if len(lineas) > 0:
        tablero += " \n"

    lineas.insert(0, str(len(lineas) + 1) + " " + time.strftime("%x") + " " + str(TIMER) + " " + str(level) + " " + tablero)

    f.close()

    f = open("partidasguardadas.txt", "w")
    for i in range(len(lineas)):
        l = lineas[i]
        f.write(l)

    f.close()

    assert f.close, "file abierto"



#NUEVO 11/dic/16, 1:23
def getLetter(n):

    '''
    Funcion que recibe un entero y deuelve una letra del conjunto {'a', 'b', 'c', 'd'}.
    '''
    assert n >= 0, "n fuera de rango"

    return chr(n + ord('a'))

#NUEVO 11/dic/16, 2:20
def getGame(n):

    '''
    Funcion que si n == 0 devuelve el string correpondiente al valor en partida; si n==1 le asigna a chess la configuracion
    del tablero correspondiente a partida y llama a la funcion genBoard
    '''

    global grid, level, TIMER, partida, chess, window

    assert partida > 0, "partida fuera de rango"

    p = partida.split(" ")
    f = open("partidasguardadas.txt", "r")
    lineas = f.readlines()

    P = []

    for l in lineas:
        L = l.split(" ")
        if L[0] == p[0]:
            P = L
            break

    if P == []:
        if n == 1:
            partida = INVALID
        return ""

    if n == 0:
        timer = ""
        T = int(P[2])

        if T/60 < 10:
            timer += "0"
        timer += str(T/60) + ":"

        if T%60 < 10:
            timer += "0"
        timer += str(T%60)

        if P[3] == "2":
            nivel = "Facil"
        elif P[3] == "3":
            nivel = "Dificil"

        assert len(timer) > 0 and len(nivel) > 0, "timer vacio o nivel vacio"

        return P[1] + " " + timer + " " + nivel + " " + P[4]

    TIMER = int(P[2])
    level = int(P[3])
    chess = P[4]
    genBoard()

    window = INGAME

    assert len(window) > 0 and TIMER >= 0 and level > 1 and len(chess) > 0, "TIMER fuera de rango o level fuera de rango o chess vacio"


def emptyBoard():

    #Funcion que inicializa la matriz global Grid en todas sus casillas con el caracter Z
    #que representa a una casilla sin pieza colocada por el usuario en el tablero


    global grid

    assert len(grid) > 0, "grid vacia"

    for i in range(4):
        for j in range(4):
            grid[i][j] = "Z"

    assert True

#NUEVO
def randBoard():

    '''
    Funcion que toma un tablero aleatorio guardado en el archivo partidasnuevas.txt, lo guarda en chess para luego llamar
    a la funcion genBoard. Finalmente anade la configuracion del tablero (de forma matricial) a la lista de matrices states.
    '''

    global grid, chess, states

    f = open("partidasnuevas.txt", "r")
    assert not f.closed, "partidasnuevas.txt no se ha abierto"

    boards = f.readlines()
    random.seed()
    chess = boards[random.randint(0, len(boards) - 1)]
    chess = chess[:-1]
    genBoard()

    f.close()

    grid2 = deepcopy(grid)
    states.append(grid2)

    assert len(states) > 0 and f.closed, "states vacio o partidasnuevas.txt sigue abierto"


def getAnim():

    # Funcion que genera las listas a utilizar para la animacion de la pantalla de inicio


    global animation, animations

    animations = []
    animations.append([])
    animations.append([])

    assert len(animations) == 2, "Tamano de animations == " + str(len(animations))

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

    assert len(animations[0]) == 6 and len(animations[1]) == 6, "len(animations[0]) == " + str(len(animations[0])) + \
    "; len(animations[1]) == " + str(len(animations[1]))


def genAnim():

    #Funcion que genera la animacion presente al inicio del juego en la ventana START, permite que las
    #imagenes se intercambien cada segundo

    global animation, animations

    assert animation >= 0 and animation < 2*FPS, "animation fuera de rango"

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
            
    assert True
        
      
def genStart():

    #Funcion que imprime en la ventana START/Inicio el icono y titulo del juego, la animacion presente
    #y un cuadro de texto para que el usuario pueda ingresar su nombre y asi iniciar sesion

    global TEXTRECT, animation

    #Animation
    genAnim()
    
    #LOGO
    logox = Wth/2
    logoy = Hht/2 - 100 

    assert logox >= 0 and logoy >= 0, "Posicion del logo == (" + str(logox) + ", " + str(logoy) + ")"

    logo = pygame.image.load('logo.png')
    logoRect = logo.get_rect()
    logoRect.center = (logox, logoy)
    dispSurf.blit(logo, logoRect)

    #TITLE
    ffont = pygame.font.Font("freesansbold.ttf", 50)
    textSurf = ffont.render("Solitaire Chess", True, WHITE)
    textRect = textSurf.get_rect()

    assert textRect.width > 0 and textRect.height > 0, "Tamano de textRect (TITLE) == " + str(textRect.size)

    textRect.center = (logox, logoy)
    dispSurf.blit(textSurf, textRect)

    #Fill name
    ffont = pygame.font.Font("freesansbold.ttf", 20)
    textSurf = ffont.render("Ingrese nombre para iniciar sesion", True, WHITE)
    textRect = textSurf.get_rect()

    assert textRect.width > 0 and textRect.height > 0, "Tamano de textRect (Fill name) == " + str(textRect.size)

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

    assert TEXTRECT.width > 0 and TEXTRECT.height > 0 and TEXTRECT == tBoxRect, "TEXTRECT.size == " + len(TEXTRECT.size)

def getUser(event):

    '''
    Funcion que permite al usuario ingresar por teclado su nombre en la pantalla START/Inicio. La funcion modifica la variable
    userName segun el input del usuario; tambien valida que userName tenga un formato correcto, i.e, no sea un string vacio 
    cuando el usuario oprime la tecla Enter, que el usuario no ingrese espacios ni caracteres extranos (incluyendo letras pertenecientes)
    al abecedario espanol) y que no pueda borrar un caracter si el string es vacio
    '''

    global TEXRECT, userName, window

    assert TEXTRECT.width > 0 and TEXTRECT.height > 0, "TEXTRECT.size == " + len(TEXTRECT.size)
    assert window == START, "window no es START. window == " + window

    try:
        if event != None and len(userName) > 0 and event.key == K_RETURN:
            window = MAIN
            return
        elif (event != None and event.key == K_BACKSPACE and len(userName) > 0):
            userName = userName[:-1]
        elif event != None and event.key != K_RETURN and event.key != K_BACKSPACE and len(userName) < TEXTRECT.width/8 - 10 and\
        ord(event.unicode) > 32 and ord(event.unicode) < 127:
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

    assert textRect.center == TEXTRECT.center, "textRect.center != TEXTRECT.center"


def genReturn():

    #Funcion que genera un cuadro de texto en la esquina inferior izquierda de una ventana. Indica al usuario
    #la tecla a presionar para regresar a la ventana anterior, siendo esta "0"

    x = 20
    y = 590

    assert 0 <= x and x < Wth and 0 <= y and y < Hht, "x y/o y fuera de rango. (" + str(x) + ", " + str(y) + ")"

    pygame.draw.rect(dispSurf, VEN, (x, y, 120, 50))
    pygame.draw.rect(dispSurf, WHITE, (x + 10, y+10, 100, 30))
    textSurf = font.render("0. REGRESAR", True, BLACK, WHITE)
    textRect = textSurf.get_rect()
    textRect.topleft = (x+15, y+15)
    dispSurf.blit(textSurf, textRect)

    assert textRect.width > 0 and textRect.height > 0, "Tamano de textRect == " + str(textRect.size)

def genSave():

    #Funcion que imprime en la ventana Save cuadros de texto que indican al usuario que
    #teclas presionar para decidir si guardar o no una partida antes de terminarla por completo y
    #regresar al menu principal

    boundUD = 200

    assert 0 <= boundUD and boundUD < Hht, "boundUD fuera de rango"

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

    assert True

def genLeave():

    #Funcion que imprime en la ventana LEAVE cuadros de texto que indican al usuario que
    #teclas presionar para decidir si salir completamente o no del juego
    global font2
    boundUD = 200

    assert 0 <= boundUD and boundUD < Hht, "boundUD fuera de rango"

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

    assert True


def genMain():

    #Funcion que imprime en la ventana MAIN/Menu Principal cuadros de texto que indican al usuario que
    #teclas presionar para escoger si jugar una partida nueva, cargar una partida pasada, mostrar records o salir del juego.

    boundUD = 200

    assert 0 <= boundUD and boundUD < Hht, "boundUD fuera de rango"

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

    assert textRect.width > 0 and textRect.height > 0, "Tamano de textRect == " + str(textRect.size)


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
    #o permitir al usuario cargar su propio tablero para jugar una partida nueva.

    boundUD = 200

    assert 0 <= boundUD and boundUD < Hht, "boundUD fuera de rango"

    pygame.draw.rect(dispSurf, VEN, (0, boundUD, Wth, Hht - 2*boundUD))
    x = 40
    y = boundUD + 20
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

    assert True

def genNew():

    #Funcion que imprime en la ventana NEW/Partida Nueva cuadros de texto que indican al 
    #usuario que teclas presionar para elegir la dificultad de la partida a jugar y donde se
    #cargara el tablero por teclado

    global font, font2, option, window
    boundUD = 150
    pygame.draw.rect(dispSurf, VEN, (0, boundUD, Wth, Hht - 2*boundUD))
    
    x = 20
    y = boundUD + 20

    assert 0 <= boundUD and boundUD < Hht, "boundUD fuera de rango"

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

    if option == "user":
        genIcon('undone.png',455,420)
    if option == "user" and window == CHESS:
        textSurf = font.render("Ingrese tablero: ", True, BLACK)
        textRect = textSurf.get_rect()
        textRect.top = y
        textRect.centerx = Wth/2
        dispSurf.blit(textSurf, textRect)

        assert textRect.width > 0 and textRect.height > 0, "Tamano de textRect == " + str(textRect.size)

    genReturn()

    assert 0 <= y and y < Hht, "y fuera de rango"

def printInBox2(word):

    #Funcion que imprime en pantalla el tablero que el usuario carga por teclado, el cual es el parametro
    #de tipo string que recibe la funcion 

    global font2
    y = Hht - 130

    assert 0 <= y and y < Hht, "y fuera de rango"

    textSurf = font2.render(word, True, BLACK)
    textRect = textSurf.get_rect()
    textRect.top = y
    textRect.centerx = Wth/2
    dispSurf.blit(textSurf, textRect)

    assert textRect.width > 0 and textRect.height > 0, "Tamano de textRect == " + str(textRect.size)

def getNumber(a):

    '''
    Funcion que le asigna a las letras en el conjunto A = {a,b,c,d} un entero del intervalo [1, 4].
    Si la letras no esta en A, aborta, i.e, bad := True
    '''
    
    global bad

    assert isinstance(a, basestring), "variable a no es un string"
    assert len(a) == 1, "a no es un caracter"

    bad = False
    if a not in "abcd":
        bad = True
        return

    #NUEVO 11/dic/16, 1:26

    assert bad == False, "bad no es False"

    return ord(a) - ord('a') + 1

def genBoard():

    #Funcion que a partir de un string ingresado por el usuario que contiene las piezas a cargar y sus
    #respectivas posiciones en el tablero, modifica la matriz "grid" inicializada con caracteres Z e
    #inserta los caracteres P,D,R,A,T,C en las posiciones respectivas de la matriz donde no haya sido modificada
    #anteriormente, esto permite que la funcion verifique que no se introduzca mas de una pieza en una misma posicion.
    #Ademas, la funcion verifica la cantidad de piezas necesarias y suficientes para que el tablero cargado sea valido 
    #y que el string ingresado sea valido en cuanto al formato de entrada para el tablero

    global chess, option, grid, window, contD, contR, contP, contA, contT, contC, cont
    contD, contR, contP, contA, contT, contC, cont = 0,0,0,0,0,0,0

    piezas = chess.split("-")
    for p in piezas:

        if p[0] == 'a' or p[0] == "b" or p[0] == "c" or p[0] == "d":

            assert not (grid[int(p[1])-1][getNumber(p[0])-1] != "Z" or len(p) != 2)

            grid[int(p[1])-1][getNumber(p[0])-1] = "P"
            contP+=1
            cont+=1
        else:

            assert not ((int(p[2]) == 0 or grid[int(p[2])-1][getNumber(p[1])-1] != "Z") or len(p) != 3)
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
                5/0 #AssertionError
            cont+=1

    assert not (contD>1 or contR >1 or contP>2 or contA>2 or contT>2 or contC>2 or cont<2 or cont>10)
        
    window = INGAME

def printBoard():

    #Funcion que imprime en pantalla el tablero cargado por el usuario mediante la matriz grid, el cual
    #indica en sus casillas que tipo de pieza se encuentra en una posicion determinada del tablero.
    #Iterando sobre la matriz, la funcion inserta una imagen que tiene por nombre de archivo el caracter distinto de Z presente en la 
    #casilla de la matriz en la posicion correspondiente segun los pixeles y la casilla de la matriz

    global grid, solGrid, window

    assert len(grid) > 0, "grid vacia (printBoard)"
    assert len(solGrid) > 0, "solGrid vacia (printBoard)"

    for i in range(4):
        for j in range(4):
            if grid[i][j] != "Z":
                posx = getX(j)
                posy = getY(i)
                img = pygame.image.load("pieces/" + grid[i][j] + ".png")
                imgRect = img.get_rect()
                imgRect.center = (posx, posy)
                dispSurf.blit(img, imgRect)

    if window == INGAME:
        return

    for i in range(4):
        for j in range(4):
            if solGrid[i][j] == 1:
                posx = getX(j) - boxSize/2
                posy = getY(i) - boxSize/2
                pygame.draw.rect(dispSurf, LIME, (posx, posy, boxSize, boxSize), 5)
            elif solGrid[i][j] == 2:
                posx = getX(j) - boxSize/2
                posy = getY(i) - boxSize/2
                pygame.draw.rect(dispSurf, BLUE_WIN, (posx, posy, boxSize, boxSize), 5)

            assert 0 <= posx and posx < Wth and 0 <= posy and posy < Hht, "posx o posy fuera de rango"


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


#NUEVO 11/dic/16, 3:00
def genLoad():

    '''
    Funcion que "imprime" en pantalla el string "Ingrese numero de la partida: " para indicarle al usuario como cargar una partida.
    '''

    global window
    boundUD = 200

    assert 0 <= boundUD and boundUD < Hht, "boundUD fuera de rango"

    y = Hht - boundUD
    textSurf = font.render("Ingrese numero de la partida: ", True, BLACK)
    textRect = textSurf.get_rect()
    textRect.top = y
    textRect.centerx = Wth/2
    dispSurf.blit(textSurf, textRect)

    assert textRect.width > 0 and textRect.height > 0, "Tamano de textRect == " + str(textRect.size)


#NUEVO 11/dic/16, 3:08
def printInBox3(word):

    '''
    Funcion que imprime en pantalla el string word, con top = Hht - 180 y centerx = Wth/2
    '''

    global window, font2

    boundUD = 180

    assert 0 <= boundUD and boundUD < Hht, "boundUD fuera de rango"

    y = Hht - boundUD
    textSurf = font2.render(word, True, BLACK)
    textRect = textSurf.get_rect()
    textRect.top = y
    textRect.centerx = Wth/2
    dispSurf.blit(textSurf, textRect)

    assert textRect.width > 0 and textRect.height > 0, "Tamano de textRect == " + str(textRect.size)

def printInBox4(word):

    '''
    Funcion que imprime en pantalla el string word, con top = Hht - 150 y centerx = Wth/2
    '''

    global window, font3
    boundUD = 150

    assert 0 <= boundUD and boundUD < Hht, "boundUD fuera de rango"

    y = Hht - boundUD
    textSurf = font3.render(word, True, BLACK)
    textRect = textSurf.get_rect()
    textRect.top = y
    textRect.centerx = Wth/2
    dispSurf.blit(textSurf, textRect)

    assert textRect.width > 0 and textRect.height > 0, "Tamano de textRect == " + str(textRect.size)

def genGame(level):

    #Funcion que imprime en la ventana INGAME/menu de juego cuadros de texto e imagenes que indican al 
    #usuario que teclas presionar para habilitar cargar movimientos por teclado, jugar, pausar el juego, 
    #deshacer jugadas y terminar la partida, indicadores del nombre del jugador, el nivel que se esta 
    #jugando y el tiempo disponible para jugar
    try:
        assert(type(level) == int and (level==1 or level==2 or level==3 or level==4)), "level no es int o level esta fuera de rango"
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

        if level != 1:
            genTimer()


        if window == INGAME:
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

        elif window == SOLUTION:
            textSurf = font.render("Ingrese posicion inicial, por ejemplo: a2. Ingrese 0 para salir de este modo.", True, BLACK)
            textRect = textSurf.get_rect()
            textRect.left = 3
            textRect.top = 597
            dispSurf.blit(textSurf, textRect)


    except:
        print("Parametro invalido.")
        sys.exit()

    assert True

def genTimer():

    '''
    Funcion que genera un temporizador o reloj en cuenta regresiva en la ventana INGAME/menu de juego
    que le indica al usuario el tiempo disponible para resolver el juego, convirtiendose el texto que 
    indica el tiempo en rojo cuando este es menor a 30 segundos.
    Dicho temporizador depende de la variable TIMER, la cual depende del nivel escogido por el usuario.
    La relacion entre TIMER y el cronometro es que, gracias a que TIMER esta en segundos, la division entera
    TIMER/60 devuelve los minutos y la operacion TIMER mod 60 devuelve los segundos restantes. De esta manera
    se obtiene el formato minutos:segundos.
    '''

    global TIMER

    assert TIMER >= 0, "TIMER NEGATIVO"

    x = 80
    y = 350

    assert 0 <= x and x < Wth, "x fuera de rango (getTimer)"
    assert 0 <= y and y < Hht, "y fuera de rango (getTimer)"

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

    assert textRect.width > 0 and textRect.height > 0, "Tamano de textRect == " + str(textRect.size)


def getMovement():

    #Funcion que valida, apoyandose en la funcion valid, si la jugada ingresada por el usuario es correcta; de serlo, actualiza la matriz
    #segun la jugada

    global movement, bad, grid, cont, states

    print(str(cont) + " " + len(states) + " " + len(grid) + " " + len(movement))

    assert cont >= 1 and len(states) > 0 and len(grid) > 0 and len(movement) > 0

    boxes = movement.split("-")

    try:
        pos1 = (int(boxes[0][1]) - 1, getNumber(boxes[0][0]) - 1)
        pos2 = (int(boxes[1][1]) - 1, getNumber(boxes[1][0]) - 1)
    except:
        movement = INVALID
        return

    if (not valid(pos1,pos2)) or bad == True or pos1 == pos2 or len(boxes[0]) != 2 or len(boxes[1]) != 2 or len(movement) < 5:
        movement = INVALID
        return

    grid[pos2[0]][pos2[1]] = grid[pos1[0]][pos1[1]]
    grid[pos1[0]][pos1[1]] = "Z"
    movement = ""
    cont -= 1

    grid2 = deepcopy(grid)
    states.append(grid2)

    assert len(states) > 0 and len(grid2) > 0 and len(grid) > 0 and cont >= 1 and len(movement) == 0

def printInBox(word):

    global textMode

    '''
    Funcion que imprime en pantalla el string que ha escrito hasta el momento el usuario tantos en el modo de Ingreso de Jugada como el de ver solucion.
    '''

    assert textMode == ON or textMode == OFF, "Valor incorrecto de textMode"

    if textMode == ON:
        jugada = "Jugada: "
    elif window == SOLUTION:
        jugada = "Posicion inicial: "
    else:
        jugada = ""

    global font2
    textSurf = font2.render(jugada + word, True, BLACK)
    textRect = textSurf.get_rect()
    textRect.bottom = Hht - 3
    textRect.left = 3
    dispSurf.blit(textSurf, textRect)

    assert textRect.width > 0 and textRect.height > 0, "Tamano de textRect == " + str(textRect.size)

def valid(pos1, pos2):

    #Funcion que valida las jugadas de cada pieza presente en el tablero de acuerdo a las reglas del Ajedrez Solitario

    assert len(pos1) == 2 and len(pos2) == 2, "pos1 o pos2 incorrecto"

    p1 = grid[pos1[0]][pos1[1]]
    p2 = grid[pos2[0]][pos2[1]]

    # 0 is Y, 1 is X
    if p2 == "R" or p2 == "Z" or p1 == "Z":
        return False

    if p1 == "A":
        return valAlfil(pos1, pos2)

    if p1 == "T":
    	return valTorre(pos1, pos2)

    if p1 == "P":
        return pos2[0] == pos1[0] + 1 and abs(pos2[1] - pos1[1]) == 1

    if p1 == "D":

        if (abs(pos1[0]-pos2[0]) == abs(pos1[1] - pos2[1])):
            return valAlfil(pos1, pos2)
        if (pos1[0] == pos2[0] or pos1[1] == pos2[1]):
            return valTorre(pos1, pos2)
        else:
            return False

    if p1 == "R":
        return abs(pos1[0] - pos2[0]) <= 1 and abs(pos1[1] - pos2[1]) <= 1

    if p1 == "C":
        return (abs(pos1[1] - pos2[1]) == 1 and abs(pos1[0] - pos2[0]) == 2) or \
        (abs(pos1[1] - pos2[1]) == 2 and abs(pos1[0] - pos2[0]) == 1)


def valTorre(pos1, pos2):

    '''
    Funcion que valida un movimiento a partir de una torre. Es utilizada tambien para validar a la Dama.
    '''

    global grid

    assert len(grid) > 0, "grid vacia (valTorre)"
    assert len(pos1) == 2 and len(pos2) == 2, "pos1 o pos2 incorrecto"

    ret = True

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
                break
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
                break
            i += add

    assert add == 1 or add == -1, "add incorrecto"

    return (pos1[0] == pos2[0] or pos1[1] == pos2[1]) and ret

def valAlfil(pos1, pos2):

    '''
    Funcion que valida un movimiento a realizar a partir de un alfil. Tambien se utiliza para validar a la Dama.
    '''

    global grid

    assert len(grid) > 0, "grid vacia (valAlfil)"
    assert len(pos1) == 2 and len(pos2) == 2, "pos1 o pos2 incorrecto"

    ret = True

    addx = 0
    addy = 0

    if (pos1[0] < pos2[0]):
        addy = 1
    else:
        addy = -1

    if (pos1[1] < pos2[1]):
        addx = 1
    else:
        addx = -1

    col = pos1[1] + addx
    row = pos1[0] + addy

    while col != pos2[1] and row != pos2[0] and col < 4 and row < 4 and col >= 0 and row >= 0:
        if (grid[row][col] != "Z"):
            ret = False
            break
        row += addy
        col += addx


    assert (addx == 1 or addx == -1) and (addy == 1 or addy == -1), "addx o addy incorrecto"

    return abs(pos1[0]-pos2[0]) == abs(pos1[1] - pos2[1]) and ret


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

    assert textRect.width > 0 and textRect.height > 0, "Tamano de textRect == " + str(textRect.size)

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

    '''
    Funcion que inserta en la ventana de juego del nivel Muy Dificil un cuadro de texto que indica el nivel, unas equis rojas que indican
    que opciones no estan habilitadas para este nivel, unos sprites de globos que indican cuantos tableros ya ha resuelto el usuario en la
    partida.
    '''

    global window, wins

    assert wins >= 0, "wins negativo"

    genTitle2("MUY",80,220)
    genTitle2("DIFICIL",80,250)
    genIcon('undone.png',375,525)
    genIcon('undone.png',225,525)

    tumblr=(50,70,105)
    pygame.draw.rect(dispSurf, tumblr, (20, 10, 120, 50))
    pygame.draw.rect(dispSurf, WHITE, (27, 17, 105, 35))

    size = 21
    x = 40 + size/2

    assert 0 <= x and x < Wth, "x fuera de rango (genVHard)"

    img = pygame.image.load("rballoon.png")
    for i in range(wins):
    	imgRect = img.get_rect()
    	imgRect.centerx = x
    	imgRect.top = 19
    	dispSurf.blit(img, imgRect)
    	x += size + 8
        assert imgRect.width > 0 and imgRect.height > 0, "Tamano de imgRect == " + str(imgRect.size)

    
    img = pygame.image.load("wballoon.png")
    for i in range(3 - wins):
    	imgRect = img.get_rect()
    	imgRect.centerx = x
    	imgRect.top = 19
    	dispSurf.blit(img, imgRect)
    	x += size + 8
        assert imgRect.width > 0 and imgRect.height > 0, "Tamano de imgRect == " + str(imgRect.size)
    


    
def getBoard():

    #Funcion que imprime la estructura de un tablero de ajedrez de dimension 4x4 en la ventana INGAME/menu de juego
    #y los indicadores de las posiciones de cada fila y columna

    x = board[0]
    y = board[1]

    assert 0 <= y and y < Hht, "y fuera de rango"
    assert 0 <= x and x < Wth, "x fuera de rango"

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
    assert 0 <= x and x < Wth, "x fuera de rango"

    for i in range(4):
        textSurf = font.render(letras[i], True, VEN, TAN)
        textRect = textSurf.get_rect()
        textRect.topleft = (x+45, 420)
        dispSurf.blit(textSurf, textRect)
        x+=100
        
    assert len(letras) > 0

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