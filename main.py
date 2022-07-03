from random import randint
from sys import argv
import pyray as pr        #pip install raylib
    
WINDOW_WIDTH = 1040
WINDOW_HEIGHT = 800
BOARD_X = 20
BOARD_Y = 20
FONT_SIZE = 30
CELL_WIDTH = int(WINDOW_WIDTH/BOARD_X)
CELL_HEIGHT = int(WINDOW_HEIGHT/BOARD_Y)
FPS_X = WINDOW_WIDTH - int(9*FONT_SIZE/2)
SANDBOX = False
SHOULD_SIM = True

if(len(argv) > 1):
    winH  = "winHeight:"
    winW  = "winWidth:"
    cellW = "cellWidth:"
    cellH = "cellHeight:"
    brdX  = "boardX:"
    brdY  = "boardY:"
    snd   = "sandbox"
    if "help" in argv:
        print("\n[HELP]")
        print(winW, WINDOW_WIDTH)
        print(winH, WINDOW_HEIGHT)
        print(cellW, CELL_WIDTH)
        print(cellH, CELL_HEIGHT)
        print(brdX, BOARD_X)
        print(brdY, BOARD_Y)
        exit()
    for i in argv:
        if i.startswith(winH):  WINDOW_HEIGHT = int(i[len(winH):])
        if i.startswith(winW):  WINDOW_WIDTH = int(i[len(winW):])
        if i.startswith(cellW): CELL_WIDTH = int(i[len(cellW):])
        if i.startswith(cellH): CELL_HEIGHT = int(i[len(cellW):])
        if i.startswith(brdX):  BOARD_X = int(i[len(brdX):])
        if i.startswith(brdY):  BOARD_Y = int(i[len(brdX):])
        if i == snd:
            SANDBOX = True
            SHOULD_SIM = False
    CELL_WIDTH = int(WINDOW_WIDTH/BOARD_X)
    CELL_HEIGHT = int(WINDOW_HEIGHT/BOARD_Y)
    FPS_X = WINDOW_WIDTH - int(9*FONT_SIZE/2)

def dumpConfig():
    print("\n[CONFIG]\nwindow_width:", WINDOW_WIDTH, "\nwindow_height:", WINDOW_HEIGHT,
          "\nboard_x:", BOARD_X, "\nboard_y:", BOARD_Y,
          "\ncell_width:", CELL_WIDTH, "\ncell_height:", CELL_HEIGHT,
          end="\n\n")

def createBoardWithRand(x,y):
    board = []
    for i in range(y):
        cur=[]
        for j in range(x): cur.append(bool(randint(0,1)))
        board.append(cur)
    return board

def createBoard(x,y):
    board = []
    for i in range(y):
        cur=[]
        for j in range(x): cur.append(False)
        board.append(cur)
    return board

def printBoard(board):
    for i in board:
        print("[", end=" ")
        for j in i:
            if j: print("true, ", end=" ")
            else: print("false", end=", ")
        print("]")
    print()
   
def simBoard(board, bx, by):
    alist = []
    sBoard = createBoard(bx, by)
    for y in range(len(board)):
        for x in range(len(board[0])):
            #FIND NUMBER OF ALIVE NEIGHBOURS
            acount = 0
            clear1 = False
            clear2 = False
            if y-1 >= 0:
                #above
                if board[y-1][x]: acount += 1
                clear1 = True
            if y+1 < len(board):
                #bottom
                if board[y+1][x]: acount += 1
                clear2 = True
            if x-1 >= 0:
                #left
                if board[y][x-1]: acount += 1
                if clear1:
                    if board[y-1][x-1]: acount += 1
                if clear2:
                    if board[y+1][x-1]: acount += 1
            if x+1 < len(board[0]):
                #right
                if board[y][x+1]: acount += 1
                if clear1:
                    if board[y-1][x+1]: acount += 1
                if clear2:
                    if board[y+1][x+1]: acount += 1
            #RULES
            if board[y][x]:
                if acount < 2: sBoard[y][x] = False
                elif acount == 2 or acount == 3: sBoard[y][x] = True
                else: sBoard[y][x] = False
            else:
                if acount == 3: sBoard[y][x] = True
            if sBoard[y][x]: alist.append([x,y])
    return sBoard, alist

def bspace2sspace(x, y): return x*CELL_WIDTH, y*CELL_HEIGHT

def sspace2bspace(x, y): return int(x/CELL_WIDTH), int(y/CELL_HEIGHT)

def genXSTR(gen):
    gen = str(gen)
    genX = WINDOW_WIDTH - int((6+len(gen)) * FONT_SIZE/2)
    return genX, gen

if SANDBOX: mainBoard = createBoard(BOARD_X, BOARD_Y)
else: mainBoard = createBoardWithRand(BOARD_X, BOARD_Y)

secBoard = createBoard(BOARD_X, BOARD_Y)

dumpConfig()

gen = 0
alist = []

pr.init_window(WINDOW_WIDTH, WINDOW_HEIGHT, "Conway's game of life")
pr.set_window_state(pr.FLAG_VSYNC_HINT)

while not pr.window_should_close():
    if pr.get_gesture_detected() == pr.GESTURE_TAP:
        tap = pr.get_touch_position(0)
        x,y = sspace2bspace(tap.x, tap.y)
        mainBoard[y][x] = not mainBoard[y][x]
        alist.append([x,y])
    if pr.is_key_pressed(pr.KEY_P): SHOULD_SIM = not SHOULD_SIM
    if SHOULD_SIM:
        gen += 1
        mainBoard, alist = simBoard(mainBoard, BOARD_X, BOARD_Y)
    pr.begin_drawing()
    pr.clear_background(pr.RAYWHITE)
    #lines
    lineX = 0
    lineY = 0
    while(lineY != BOARD_Y):
        temp = CELL_HEIGHT*lineY
        pr.draw_line(0, temp, WINDOW_WIDTH, temp, pr.BLACK)
        lineY += 1
    while(lineX != BOARD_X):
        temp = CELL_WIDTH*lineX
        pr.draw_line(temp, WINDOW_HEIGHT, temp, 0, pr.BLACK)
        lineX += 1
    #alive cells
    for i in alist:
        x, y = bspace2sspace(i[0], i[1])
        pr.draw_rectangle(x, y, CELL_WIDTH, CELL_HEIGHT, pr.BLACK)
    #stat
    pr.draw_text("FPS: " + str(pr.get_fps()), FPS_X, 0, FONT_SIZE, pr.BLUE)
    genX, genStr = genXSTR(gen)
    pr.draw_text("GEN: " + genStr, genX, FONT_SIZE, FONT_SIZE, pr.BLUE)
    pr.end_drawing()

pr.close_window()
