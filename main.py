from random import randint
import pyray as pr

WINDOW_HEIGHT = 800
WINDOW_WIDTH = 1040

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
        
def simBoard(board, sBoard):
    alist = []
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
            if board[y][x]:
                if acount < 2: sBoard[y][x] = False
                elif acount > 3: sBoard[y][x] = False
            else:
                if acount == 3: sBoard[y][x] = True
            if sBoard[y][x]: alist.append([x, y])
    return sBoard, alist

mainBoard = []
secBoard = []

mainBoard = createBoardWithRand(6, 6)
secBoard = createBoard(6, 6)

mainBoard, alist = simBoard(mainBoard, secBoard)
printBoard(mainBoard)

pr.init_window(WINDOW_WIDTH, WINDOW_HEIGHT, "Conway's game of life")
pr.set_window_state(pr.FLAG_VSYNC_HINT)

while not pr.window_should_close():
    pr.begin_drawing()
    pr.clear_background(pr.RAYWHITE)
    pr.draw_text("FPS: " + str(pr.get_fps()), 910, 10, 30, pr.BLUE)
    pr.end_drawing()

pr.close_window()
