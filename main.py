from random import randint
from sys import argv
from os import path, mkdir
import pickle
import pyray as pr  #pip install raylib

WINDOW_WIDTH = 1040
WINDOW_HEIGHT = 800
BOARD_X = 20
BOARD_Y = 20
FONT_SIZE = 30
STEP_PERC = 10
MAX_TIME = 2
SANDBOX = False
SHOULD_SIM = True
BOARD = None
CELL_WIDTH = None
CELL_HEIGHT = None
FPS_X = None

if(len(argv) > 1):
    winH  = "winHeight:"
    winW  = "winWidth:"
    brdX  = "boardX:"
    brdY  = "boardY:"
    board = "board:"
    stepP = "stepPercent:"
    mxTim = "maxTime:"
    snd   = "sandbox"
    argv.pop(0)
    if "help" in argv:
        print("\n[HELP]")
        print("W - increase step value")
        print("S - decrease step value")
        print("P - pause the board")
        print("F - save current board under boards/*name*.gol")
        print("Click on cell to invert it")
        print("----")
        print(winW, WINDOW_WIDTH)
        print(winH, WINDOW_HEIGHT)
        print(brdX, BOARD_X)
        print(brdY, BOARD_Y)
        print(stepP, STEP_PERC)
        print(mxTim, MAX_TIME)
        print(board)
        print(snd)
        exit()
    for i in argv:
        if i.startswith(winH):    WINDOW_HEIGHT = int(i[len(winH):])
        elif i.startswith(winW):  WINDOW_WIDTH = int(i[len(winW):])
        elif i.startswith(brdX):  BOARD_X = int(i[len(brdX):])
        elif i.startswith(brdY):  BOARD_Y = int(i[len(brdX):])
        elif i.startswith(stepP): STEP_PERC = int(i[len(stepP):])
        elif i.startswith(mxTim): MAX_TIME = int(i[len(mxTim):])
        elif i.startswith(board):
            BOARD = str(i[len(board):])
            SHOULD_SIM = False
        elif i == snd:
            SANDBOX = True
            SHOULD_SIM = False
        else:
            print("invalid argument:", i)
            exit()

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
   
def simBoard(board, bx, by):
    alist = []
    sBoard = createBoard(bx, by) #creating a new board every time. Python bad....
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

def xSTR(num, numOfChar):
    string = str(num)
    x = WINDOW_WIDTH - int((numOfChar+len(string)) * FONT_SIZE/2)
    return x, string

gen = 0
alist = []
time = 0
step = 0.1

if SANDBOX: mainBoard = createBoard(BOARD_X, BOARD_Y)
elif BOARD != None:
    try:
        f = open(BOARD, "rb")
    except IOError:
        print("file does not exist:", BOARD)
        exit()
    else:
        WINDOW_WIDTH, WINDOW_HEIGHT, BOARD_X, BOARD_Y, FONT_SIZE, STEP_PERC, MAX_TIME = pickle.load(f)
        mainBoard = pickle.load(f)
        alist = pickle.load(f)
        f.close()
else: mainBoard = createBoardWithRand(BOARD_X, BOARD_Y)

CELL_WIDTH, CELL_HEIGHT, FPS_X = int(WINDOW_WIDTH/BOARD_X), int(WINDOW_HEIGHT/BOARD_Y), WINDOW_WIDTH - int(9*FONT_SIZE/2)
print("\n[CONFIG]\nwindow_width:", WINDOW_WIDTH, "\nwindow_height:", WINDOW_HEIGHT,
      "\nboard_x:", BOARD_X, "\nboard_y:", BOARD_Y,
      "\ncell_width:", CELL_WIDTH, "\ncell_height:", CELL_HEIGHT,
      "\nfont_size:", FONT_SIZE, "\nstep_percentage:", STEP_PERC, "\nmax_time:", MAX_TIME,
      end="\n\n")

pr.init_window(WINDOW_WIDTH, WINDOW_HEIGHT, "Conway's game of life")
pr.set_window_state(pr.FLAG_VSYNC_HINT)

while not pr.window_should_close():
    #SIMULATE
    if pr.get_gesture_detected() == pr.GESTURE_TAP:
        tap = pr.get_touch_position(0)
        x,y = sspace2bspace(tap.x, tap.y)
        if mainBoard[y][x]:
            mainBoard[y][x] = False
            alist.remove([x,y])
        else:
            mainBoard[y][x] = True
            alist.append([x,y])
    if pr.is_key_pressed(pr.KEY_F):
        fileName = ""
        firstTime = True
        while True:
            if pr.window_should_close(): exit()
            pr.begin_drawing()
            pr.clear_background(pr.BLACK)
            key = pr.get_key_pressed()
            if key == 0 or key == 280 or key == 340 or key == 341: pass
            elif key == 259: fileName = fileName[:-1]
            elif key == 257:
                if not path.exists("boards"): mkdir("boards")
                f = open("boards/"+fileName+".gol", "wb")
                pickle.dump([WINDOW_WIDTH, WINDOW_HEIGHT, BOARD_X, BOARD_Y, FONT_SIZE, STEP_PERC, MAX_TIME], f)
                pickle.dump(mainBoard, f)
                pickle.dump(alist, f)
                f.close()
                break
            else:
                if not firstTime:
                    key = chr(key)
                    if key.isalpha(): fileName += key
                firstTime = False
            pr.draw_text(fileName, 0, int(WINDOW_HEIGHT/2), FONT_SIZE*2, pr.WHITE)
            pr.end_drawing()
    if pr.is_key_pressed(pr.KEY_P): SHOULD_SIM = not SHOULD_SIM
    if pr.is_key_down(pr.KEY_W): step += (STEP_PERC/100) * step
    if pr.is_key_down(pr.KEY_S): step -= (STEP_PERC/100) * step
    step = round(step, 5)
    if SHOULD_SIM:
        if time < MAX_TIME: time += step
        else:
            time = 0
            gen += 1
            mainBoard, alist = simBoard(mainBoard, BOARD_X, BOARD_Y)
    #DRAW
    pr.begin_drawing()
    pr.clear_background(pr.BLACK)
    #lines
    lineX = 0
    lineY = 0
    while(lineY != BOARD_Y):
        temp = CELL_HEIGHT*lineY
        pr.draw_line(0, temp, WINDOW_WIDTH, temp, pr.WHITE)
        lineY += 1
    while(lineX != BOARD_X):
        temp = CELL_WIDTH*lineX
        pr.draw_line(temp, WINDOW_HEIGHT, temp, 0, pr.WHITE)
        lineX += 1
    #alive cells
    for i in alist:
        x, y = bspace2sspace(i[0], i[1])
        pr.draw_rectangle(x, y, CELL_WIDTH, CELL_HEIGHT, pr.WHITE)
    #STAT
    pr.draw_text("FPS: " + str(pr.get_fps()), FPS_X, 0, FONT_SIZE, pr.BLUE)
    x, string = xSTR(step, 7)
    pr.draw_text("STEP: " + string, x, FONT_SIZE, FONT_SIZE, pr.BLUE)
    x, string = xSTR(gen, 6)
    pr.draw_text("GEN: " + string, x, FONT_SIZE*2, FONT_SIZE, pr.BLUE)
    pr.end_drawing()

pr.close_window()
