#input
from typing import get_origin
from pynput.keyboard import Listener
import os
import time

cursorPos = [4,4]
selectedPos = [-1,-1]
movablePos = [-1,-1]
pposition = [-1,-1]
turn = 'w'
positions = []
promoting = False
Lwcastle = False
Rwcastle = False
LwRMoved = False
RwRMoved = False
wKMoved = False
Lbcastle = False
Rbcastle = False
LbRMoved = False
RbRMoved = False
bKMoved = False
LUT = {
    'bP': '♙ ',
    'bN': '♘ ',
    'bB': '♗ ',
    'bR': '♖ ',
    'bQ': '♕ ',
    'bK': '♔ ',
    'wP': '♟ ',
    'wN': '♞ ',
    'wB': '♝ ',
    'wR': '♜ ',
    'wQ': '♛ ',
    'wK': '♚ ',
    '-': '  '
}
# board = [['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
#          ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
#          ['-',  '-',  '-',  '-',  '-',  '-',  '-',  '-' ],
#          ['-',  '-',   '-',  '-',  '-',  '-',  '-',  '-' ],
#          ['-',  '-',  '-',  '-',   '-',  '-',  '-',  '-' ],
#          ['-',  '-',  '-',  '-',  '-',  '-',  '-',  '-' ],
#          ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
#          ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']]

board = [['bR', '-', '-', '-', 'bK', '-', '-', 'bR'],
         ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
         ['-',  '-',  '-',  '-',  '-',  '-',  '-',  '-' ],
         ['-',  '-',   '-',  '-',  'wP',  '-',  '-',  '-'],
         ['-',  '-',  '-',  '-',   '-',  '-',  '-',  '-'],
         ['-',  '-',  '-',  '-',  '-',  '-',  '-',  '-' ],
         ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
         ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']]

def keyInput(key):
    global selectedPos
    global cursorPos
    try:
        if key == key.up and cursorPos[0] != 0: cursorPos[0] -= 1
        elif key == key.down and cursorPos[0] != 7: cursorPos[0] += 1
        elif key == key.left and cursorPos[1] != 0: cursorPos[1] -= 1
        elif key == key.right and cursorPos[1] != 7: cursorPos[1] += 1
        elif (key == key.enter or key == key.space) and (cursorPos == selectedPos) or key == key.esc: selectedPos = [-1,-1] #deselect
        elif key == key.enter or key == key.space: selectOrMove()
    except: 
        pass
def onPress(key):
    global promoting
    if promoting:
        promotePawn(key)
    else:
        keyInput(key)
        render(board)

def clearScreen():
    time.sleep(0.05)
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def opositeTurn(turn):
    if turn == 'w': turn = 'b'
    else: turn = 'w'
    return turn

def movementsRaycast(x,y,rango):
    global selectedPos
    global turn
    global positions
    
    for i in range(1, rango, 1):
        if selectedPos[0]+i*x <= 7 and selectedPos[0]+i*x >= 0 and selectedPos[1]+i*y <= 7 and selectedPos[1]+i*y >= 0:
            if board[selectedPos[0]+i*x][selectedPos[1]+i*y][0] == '-': #spaces
                positions.append([selectedPos[0]+i*x, selectedPos[1]+i*y])
            elif board[selectedPos[0]+i*x][selectedPos[1]+i*y][0] == turn: #same color pices
                break
            elif board[selectedPos[0]+i*x][selectedPos[1]+i*y][0] == opositeTurn(turn): #other color pices to stop moving after that
                positions.append([selectedPos[0]+i*x, selectedPos[1]+i*y])
                break

def promotePawn(key):
    global LUT
    global turn
    global cursorPos
    global promoting
    global board
    global selectedPos
    piceOrder = {
        0: 'Q',
        1: 'R',
        2: 'B',
        3: 'N'
    }
    if key != None:
        if cursorPos[1] < 3 and key == key.right: 
            cursorPos[1] += 1
        elif cursorPos[1] > 0 and key == key.left: 
            cursorPos[1] -= 1  
    # clearScreen()
    print(cursorPos)
    print('Select pice to promote to:\n    ╔═══╦═══╦═══╦═══╗\n', end='')
    if cursorPos[1] == 0:
        printable = '║ {}║ {}║ {}║ {}║'.format(color(LUT[turn + 'Q'],'green'), LUT[turn + 'R'], LUT[turn + 'B'], LUT[turn + 'N'])
    if cursorPos[1] == 1:
        printable = '║ {}║ {}║ {}║ {}║'.format(LUT[turn + 'Q'], color(LUT[turn + 'R'],'green'), LUT[turn + 'B'], LUT[turn + 'N'])
    if cursorPos[1] == 2:
        printable = '║ {}║ {}║ {}║ {}║'.format(LUT[turn + 'Q'], LUT[turn + 'R'], color(LUT[turn + 'B'],'green'), LUT[turn + 'N'])
    if cursorPos[1] == 3:
        printable = '║ {}║ {}║ {}║ {}║'.format(LUT[turn + 'Q'], LUT[turn + 'R'], LUT[turn + 'B'], color(LUT[turn + 'N'],'green'))
    print('    ' + printable)
    print('    ╚═══╩═══╩═══╩═══╝')
    if key == key.enter or key == key.space:
        if turn == 'w':
            print(selectedPos)
            board[0][selectedPos[1]] = turn + piceOrder[cursorPos[1]]
            print(board[0][selectedPos[1]])
        if turn == 'b':
            board[7][selectedPos[1]] = turn + piceOrder[cursorPos[1]]
        promoting = False
        turn = opositeTurn(turn)
        cursorPos = selectedPos
        selectedPos = [-1,-1]
        render(board)
        return 0
    #time.sleep(3)

def selectOrMove():
    global selectedPos
    global turn
    global board
    global positions
    global promoting
    global cursorPos
    global Lwcastle
    global Rwcastle
    global LwRMoved
    global RwRMoved
    global wKMoved
    global Lbcastle
    global Rbcastle
    global bKMoved
    global LbRMoved
    global RbRMoved
    global pposition

    if board[cursorPos[0]][cursorPos[1]][0] == turn:
        selectedPos = cursorPos.copy()
        positions = []
        #===Rook===#
        if board[cursorPos[0]][cursorPos[1]][1] == 'R': #selected piece
            movementsRaycast(1,0,8) #up
            movementsRaycast(0,1,8) #right
            movementsRaycast(-1,0,8) #down
            movementsRaycast(0,-1,8) #left
            if turn == "b":
                if RbRMoved == False and not board[0][7] == "bR":
                    RbRMoved = True
                if LbRMoved == False and not board[0][0] == "bR":
                    LbRMoved == True

            if turn == "w":
                if RwRMoved == False and not board[7][7] == "wR":
                    RwRMoved = True
                if LwRMoved == False and not board[7][0] == "wR":
                    LwRMoved = True

        #===Bishop===#
        if board[cursorPos[0]][cursorPos[1]][1] == 'B':
            movementsRaycast(1,1,8)
            movementsRaycast(-1,1,8)
            movementsRaycast(1,-1,8)
            movementsRaycast(-1,-1,8)
        #===Qween===#
        if board[cursorPos[0]][cursorPos[1]][1] == 'Q':
            movementsRaycast(1,1,8)
            movementsRaycast(-1,1,8)
            movementsRaycast(1,-1,8)
            movementsRaycast(-1,-1,8)
            movementsRaycast(1,0,8)
            movementsRaycast(0,1,8)
            movementsRaycast(-1,0,8)
            movementsRaycast(0,-1,8)
        #===kNight===#
        if board[cursorPos[0]][cursorPos[1]][1] == 'N':
            movementsRaycast(1,2,2)
            movementsRaycast(-1,2,2)
            movementsRaycast(1,-2,2)
            movementsRaycast(-1,-2,2)
            movementsRaycast(2,1,2)
            movementsRaycast(2,-1,2)
            movementsRaycast(-2,-1,2)
            movementsRaycast(-2,1,2)

        #===King===#
        if board[cursorPos[0]][cursorPos[1]][1] == 'K':
            movementsRaycast(1,1,2)
            movementsRaycast(1,-1,2)
            movementsRaycast(-1,-1,2)
            movementsRaycast(-1,1,2)
            movementsRaycast(0,1,2)
            movementsRaycast(0,-1,2)
            movementsRaycast(1,0,2)
            movementsRaycast(-1,0,2)

            if turn == "b":
                if bKMoved == False and not selectedPos[0] == 0 and not selectedPos[1] == 4:
                    bKMoved = True
                if Rbcastle == False and board[0][6] == "-" and board[0][5] == "-" and bKMoved == False and RbRMoved == False and board[0][7] == "bR":
                    Rbcastle = True
                    movementsRaycast(0,1,3)
                if Lbcastle == False and (board[0][1] == "-" and board[0][2] == "-" and board[0][3] == "-") and (bKMoved == False and LbRMoved == False) and board[0][0] == "bR":
                    Lbcastle = True
                    movementsRaycast(0,-1,3)
            if turn == "w":
                if wKMoved == False and not selectedPos[0] == 7 and not selectedPos[1] == 4:
                    wKMoved = True
                if Rwcastle == False and (board[7][6] == "-" and board[7][5] == "-") and (wKMoved == False and RwRMoved == False) and board[7][7] == "wR":
                    Rwcastle = True
                    movementsRaycast(0,1,3)
                if Lwcastle == False and (board[7][1] == "-" and board[7][2] == "-" and board[7][3] == "-") and (wKMoved == False and RwRMoved == False) and board[7][0] == "wR":
                    Lwcastle = True
                    movementsRaycast(0,-1,3)
                
        #===Pawn===#
        if board[cursorPos[0]][cursorPos[1]][1] == 'P':
            if turn == 'w': direction = -1
            elif turn == 'b': direction = 1
            if board[selectedPos[0]+direction][selectedPos[1]][0] == '-': # can move one
                positions.append([selectedPos[0]+direction,selectedPos[1]])
            if selectedPos[0] == 6 and board[4][selectedPos[1]][0] == '-' and board[5][selectedPos[1]][0] == '-' and board[cursorPos[0]][cursorPos[1]][0] == 'w': # can move two (white)
                positions.append([4,selectedPos[1]])
            if selectedPos[0] == 1 and board[3][selectedPos[1]][0] == '-' and board[2][selectedPos[1]][0] == '-'and board[cursorPos[0]][cursorPos[1]][0] == 'b': # can move two (black)
                positions.append([3,selectedPos[1]])
            if selectedPos[0]+1 <= 7 and selectedPos[0]+1 >= 0 and selectedPos[1]+1 <= 7 and selectedPos[1]+1 >= 0:
                if board[selectedPos[0]+direction][selectedPos[1]+1][0] == opositeTurn(turn): # can eat right
                    positions.append([selectedPos[0]+direction,selectedPos[1]+1])
            if selectedPos[0]-1 <= 7 and selectedPos[0]-1 >= 0 and selectedPos[1]-1 <= 7 and selectedPos[1]-1 >= 0:
                if board[selectedPos[0]+direction][selectedPos[1]-1][0] == opositeTurn(turn): # can eat left
                    positions.append([selectedPos[0]+direction,selectedPos[1]-1])
            if turn == "b":
                print("b",pposition[0],pposition[1],cursorPos)
                if pposition[0] ==  6 and cursorPos[0] == 4:
                    print(pposition[0]-1,pposition[1])
                    positions.append([pposition[0]-1,pposition[1]])
                    
            # if turn == "w":
            #     print("w",pposition[0]+1,pposition[1],cursorPos)
            #     if pposition[0]+1 ==  3 and cursorPos[0] == 4:
            #         print("zuuu")
            #         positions.append(pposition[0]+1,pposition[1])
            pposition = selectedPos.copy()
                
    elif selectedPos != [-1,-1]:
        print(selectedPos,cursorPos)
        if [cursorPos[0],cursorPos[1]] in positions:
            if (cursorPos[0] == 0 or cursorPos[0] == 7) and board[selectedPos[0]][selectedPos[1]] == turn + 'P': # promote
                board[selectedPos[0]][selectedPos[1]] = '-'
                promoting = True
                selectedPos = cursorPos.copy()
                cursorPos[1] = 0
                promotePawn(None)
            else:
                board[cursorPos[0]][cursorPos[1]] = board[selectedPos[0]][selectedPos[1]]
                board[selectedPos[0]][selectedPos[1]] = '-'
                turn = opositeTurn(turn)
        if not promoting: selectedPos = [-1,-1]        

def color(string, color=''): #set colors
        #https://stackabuse.com/how-to-print-colored-text-in-python/
    if color == 'white':
        string = '\u001b[48;5;244m' + string + '\u001b[0m'
    elif color == 'green':
        string = '\u001b[48;5;2m' + string + '\u001b[0m'
    elif color == 'orange':
        string = '\u001b[48;5;166m' + string + '\u001b[0m'
    elif color == 'yellow':
        string = '\u001b[48;5;3m' + string + '\u001b[0m'
    elif color == 'darkMove':
        string = '\u001b[48;5;65m' + string + '\u001b[0m'
    elif color == 'lightMove':
        string = '\u001b[48;5;101m' + string + '\u001b[0m'    
    elif color == 'red':
        string = '\u001b[48;5;196m' + string + '\u001b[0m'
    return string

def render(board):
    
    global selectedPos
    global positions
    global LUT
    global Rbcastle
    global Lwcastle
    global pposition
    
    if promoting == False:
        # clearScreen()
        if turn == "b":
            print(color("      Black     ","red"))
        else:
            print(color("      White     ","red"))
        for i in range(8):
            for j in range(8):
                item = LUT[board[i][j]]
                if Rbcastle and board[0][6] == "bK":
                    board[0][5] = "bR"
                    board[0][7] = "-"
                if Lbcastle and board[0][2] == "bK":
                    board[0][3] = "bR"
                    board[0][0] = "-"
                if selectedPos == pposition:
                    board[4][pposition[1]] = "-"
                if i == cursorPos[0] and j == cursorPos[1]:
                    item = color(item, 'orange') # Cursor
                if selectedPos != [-1,-1] and [i,j] in positions:
                    if board[i][j][0] == opositeTurn(turn) or selectedPos == turn:
                        item = color(item, 'red') #Movable
                    else:
                        item = color(item, 'lightMove') #Movable

                if i == cursorPos[0] and j == cursorPos[1] and cursorPos == selectedPos:
                    item = color(item, 'yellow') #Selected and cursor in same position
                if i == selectedPos[0] and j == selectedPos[1]:
                    item = color(item, 'green') # selected

                if (i+j) % 2 == 0:
                    item = color(item, 'white')
                print(item,end='')
            print()
        # print(positions)

with Listener(on_press=onPress) as l:
    l.join()


