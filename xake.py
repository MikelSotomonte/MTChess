# coding: utf8
from typing import get_origin
try: # check if pynput is installed and try to install it if it isn't
    from pynput.keyboard import Listener
except:
    print("Pynput libreria ez dago instalatuta. Enter sakatu instalatzen saiatzeko.")
    input()
    try:
        import subprocess
        import sys
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pynput"])
        print("Libreria instalatu da. Enter sakatu programa exekutatzeko.")
        input()
        from pynput.keyboard import Listener
    except: 
        print("Ez da libreria instalatu, pynput manualki instalatu beharko duzu. Pip erabiltzea gomendatzen dizugu.")
import random
import os
import time
# declare variables
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
bstep = False
wstep = False

LUT = { # lookup table, dictionary
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

board = [['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'], # current board position, declared with beginning position
         ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
         ['-',  '-',  '-',  '-',  '-',  '-',  '-',  '-' ],
         ['-',  '-',   '-',  '-',  '-',  '-',  '-',  '-'],
         ['-',  '-',  '-',  '-',   '-',  '-',  '-',  '-'],
         ['-',  '-',  '-',  '-',  '-',  '-',  '-',  '-' ],
         ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
         ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']]

# handle input
def onPress(key):
    global promoting
    if promoting: #different rendering and input when promote menu is up
        promotePawn(key) 

    else:
        keyInput(key)
        render(board) 

def keyInput(key): 
    global selectedPos
    global cursorPos
    try:
        if key == key.up and cursorPos[0] != 0: cursorPos[0] -= 1 # use arrows to move
        elif key == key.down and cursorPos[0] != 7: cursorPos[0] += 1
        elif key == key.left and cursorPos[1] != 0: cursorPos[1] -= 1
        elif key == key.right and cursorPos[1] != 7: cursorPos[1] += 1
        elif (key == key.enter or key == key.space) and (cursorPos == selectedPos) or key == key.esc: selectedPos = [-1,-1] # deselect
        elif key == key.enter or key == key.space: selectOrMove() # move pice
        
    except: 
        pass


def clearScreen(): # clears the screen each time the board is refreshed
    time.sleep(0.05)
    if os.name == 'nt':
        os.system('cls')

    else:
        os.system('clear')

def opositeTurn(turn): # flips the turn
    if turn == 'w': 
        turn = 'b'
    else: 
        turn = 'w'
    return turn

def movementsRaycast(x,y,rango): # save the positons the piece can move to, either giving a max lenght or untill the ray hits a pice or the edge of the board
    global selectedPos
    global turn
    global positions
    
    for i in range(1, rango, 1):
        if selectedPos[0]+i*x <= 7 and selectedPos[0]+i*x >= 0 and selectedPos[1]+i*y <= 7 and selectedPos[1]+i*y >= 0: # checks the available positions and range

            if board[selectedPos[0]+i*x][selectedPos[1]+i*y][0] == '-': # empty spaces
                positions.append([selectedPos[0]+i*x, selectedPos[1]+i*y])
                
            elif board[selectedPos[0]+i*x][selectedPos[1]+i*y][0] == turn: # same color pices, stop moving before this position
                break

            elif board[selectedPos[0]+i*x][selectedPos[1]+i*y][0] == opositeTurn(turn): # oposite color pices, stop moving after this position
                positions.append([selectedPos[0]+i*x, selectedPos[1]+i*y])
                break

def promotePawn(key): # pawn promotion logic
    global LUT
    global turn
    global cursorPos
    global promoting
    global board
    global selectedPos
    
    piceOrder = { # pice order in the promote menu
        0: 'Q',
        1: 'R',
        2: 'B',
        3: 'N'
    }
    clearScreen() # custom rendering for this state, and custom key logic 
    if key != None:
        if cursorPos[1] < 3 and key == key.right: 
            cursorPos[1] += 1
            
        elif cursorPos[1] > 0 and key == key.left: 
            cursorPos[1] -= 1  
            
    print('Select pice to promote to:\n    ╔═══╦═══╦═══╦═══╗\n', end='')
    if cursorPos[1] == 0:
        printable = '║ {}║ {}║ {}║ {}║'.format(color(LUT[turn + 'Q'],'green'), LUT[turn + 'R'], LUT[turn + 'B'], LUT[turn + 'N']) #qween
        
    if cursorPos[1] == 1:
        printable = '║ {}║ {}║ {}║ {}║'.format(LUT[turn + 'Q'], color(LUT[turn + 'R'],'green'), LUT[turn + 'B'], LUT[turn + 'N']) #Rook

    if cursorPos[1] == 2:
        printable = '║ {}║ {}║ {}║ {}║'.format(LUT[turn + 'Q'], LUT[turn + 'R'], color(LUT[turn + 'B'],'green'), LUT[turn + 'N']) #Bishop

    if cursorPos[1] == 3:
        printable = '║ {}║ {}║ {}║ {}║'.format(LUT[turn + 'Q'], LUT[turn + 'R'], LUT[turn + 'B'], color(LUT[turn + 'N'],'green')) #kNight

    print('    ' + printable)
    print('    ╚═══╩═══╩═══╩═══╝')
    if key == key.enter or key == key.space: # pice to promote to selection
        if turn == 'w':
            board[0][selectedPos[1]] = turn + piceOrder[cursorPos[1]]

        if turn == 'b':
            board[7][selectedPos[1]] = turn + piceOrder[cursorPos[1]]

        promoting = False
        turn = opositeTurn(turn)
        cursorPos = selectedPos
        selectedPos = [-1,-1]
        render(board)
        return 0

def selectOrMove(): # select or move :)
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
    global bstep
    global wstep

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
                if RbRMoved == False and not board[0][7] == "bR": # to know if the rooks moved, if so, can't castle on that side 
                    RbRMoved = True

                if LbRMoved == False and not board[0][0] == "bR":
                    LbRMoved == True

            if turn == "w":
                if RwRMoved == False and not board[7][7] == "wR":
                    RwRMoved = True

                if LwRMoved == False and not board[7][0] == "wR":
                    LwRMoved = True

        #===Bishop===#
        if board[cursorPos[0]][cursorPos[1]][1] == 'B': # bishop movement
            movementsRaycast(1,1,8)
            movementsRaycast(-1,1,8)
            movementsRaycast(1,-1,8)
            movementsRaycast(-1,-1,8)

        #===Qween===#
        if board[cursorPos[0]][cursorPos[1]][1] == 'Q': # qween movement
            movementsRaycast(1,1,8)
            movementsRaycast(-1,1,8)
            movementsRaycast(1,-1,8)
            movementsRaycast(-1,-1,8)
            movementsRaycast(1,0,8)
            movementsRaycast(0,1,8)
            movementsRaycast(-1,0,8)
            movementsRaycast(0,-1,8)

        #===kNight===#
        if board[cursorPos[0]][cursorPos[1]][1] == 'N': # knight movement
            movementsRaycast(1,2,2)
            movementsRaycast(-1,2,2)
            movementsRaycast(1,-2,2)
            movementsRaycast(-1,-2,2)
            movementsRaycast(2,1,2)
            movementsRaycast(2,-1,2)
            movementsRaycast(-2,-1,2)
            movementsRaycast(-2,1,2)

        #===King===#
        if board[cursorPos[0]][cursorPos[1]][1] == 'K': # king movement
            movementsRaycast(1,1,2)
            movementsRaycast(1,-1,2)
            movementsRaycast(-1,-1,2)
            movementsRaycast(-1,1,2)
            movementsRaycast(0,1,2)
            movementsRaycast(0,-1,2)
            movementsRaycast(1,0,2)
            movementsRaycast(-1,0,2)

            if turn == "b":
                if bKMoved == False and not selectedPos[0] == 0 and not selectedPos[1] == 4:# know if the king moved, cancel casteling if so
                    bKMoved = True

                if Rbcastle == False and board[0][6] == "-" and board[0][5] == "-" and bKMoved == False and RbRMoved == False and board[0][7] == "bR": # to do short castle
                    Rbcastle = True
                    movementsRaycast(0,1,3)

                if Lbcastle == False and (board[0][1] == "-" and board[0][2] == "-" and board[0][3] == "-") and (bKMoved == False and LbRMoved == False) and board[0][0] == "bR":# to do long castle
                    Lbcastle = True
                    movementsRaycast(0,-1,3)

            if turn == "w":
                if wKMoved == False and not selectedPos[0] == 7 and not selectedPos[1] == 4: # know if the king moved, cancel casteling if so
                    bKMoved = True
                    wKMoved = True

                if Rwcastle == False and (board[7][6] == "-" and board[7][5] == "-") and (wKMoved == False and RwRMoved == False) and board[7][7] == "wR":# to do short castle
                    Rwcastle = True
                    movementsRaycast(0,1,3)

                if Lwcastle == False and (board[7][1] == "-" and board[7][2] == "-" and board[7][3] == "-") and (wKMoved == False and RwRMoved == False) and board[7][0] == "wR":# to do long castle
                    Lwcastle = True
                    movementsRaycast(0,-1,3)
                
        #===Pawn===#
        if board[cursorPos[0]][cursorPos[1]][1] == 'P': # pawn movement
            if turn == 'w': 
                direction = -1

            elif turn == 'b': 
                direction = 1

            if board[selectedPos[0]+direction][selectedPos[1]][0] == '-': # can move one
                positions.append([selectedPos[0]+direction,selectedPos[1]])

            if selectedPos[0] == 6 and board[4][selectedPos[1]][0] == '-' and board[5][selectedPos[1]][0] == '-' and board[cursorPos[0]][cursorPos[1]][0] == 'w': # can move two (white)
                positions.append([4,selectedPos[1]])

            if selectedPos[0] == 1 and board[3][selectedPos[1]][0] == '-' and board[2][selectedPos[1]][0] == '-'and board[cursorPos[0]][cursorPos[1]][0] == 'b': # can move two (black)
                positions.append([3,selectedPos[1]])

            if selectedPos[0]+1 <= 7 and selectedPos[0]+1 >= 0 and selectedPos[1]+1 <= 7 and selectedPos[1]+1 >= 0:
                if board[selectedPos[0]+direction][selectedPos[1]+1][0] == opositeTurn(turn): # can eat to the right
                    positions.append([selectedPos[0]+direction,selectedPos[1]+1])

            if selectedPos[0]-1 <= 7 and selectedPos[0]-1 >= 0 and selectedPos[1]-1 <= 7 and selectedPos[1]-1 >= 0:
                if board[selectedPos[0]+direction][selectedPos[1]-1][0] == opositeTurn(turn): # can eat to the left
                    positions.append([selectedPos[0]+direction,selectedPos[1]-1])

            if turn == "b":
                if pposition[0] ==  6 and cursorPos[0] == 4 and (pposition[1] == selectedPos[1]-1 or pposition[1] == selectedPos[1]+1):# can eat on passant
                    positions.append([pposition[0]-1,pposition[1]])
                    wstep = True

            if turn == "w":
                if pposition[0] ==  1 and cursorPos[0] == 3 and (pposition[1] == selectedPos[1]-1 or pposition[1] == selectedPos[1]+1):# can eat on passant
                    positions.append([pposition[0]+1,pposition[1]])
                    bstep = True

            pposition = selectedPos.copy() # save past position to know if can eat on passant
                
    elif selectedPos != [-1,-1]:
        if bstep and selectedPos[0] == cursorPos[0]+1 and selectedPos[1] and cursorPos[1]-1: # if eaten on passant, delete the pawn
            board[cursorPos[0]+1][cursorPos[1]] = "-"
            bstep = False

        if wstep and selectedPos[0] == cursorPos[0]-1 and selectedPos[1] and cursorPos[1]+1: 
            board[cursorPos[0]-1][cursorPos[1]] = "-"
            wstep = False

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

        if Rbcastle and board[0][6] == "bK": # black castle short
            board[0][5] = "bR"
            board[0][7] = "-"

        if Lbcastle and board[0][2] == "bK": # black castle long
            board[0][3] = "bR"
            board[0][0] = "-"

        if Rwcastle and board[7][6] == "wK":  # white castle short
            board[7][5] = "wR"
            board[7][7] = "-"

        if Lwcastle and board[7][2] == "wK": # white castle long
            board[7][3] = "wR"
            board[7][0] = "-"

        if not promoting: 
            selectedPos = [-1,-1]        

def color(string, color=''): # set colors (https://stackabuse.com/how-to-print-colored-text-in-python/)
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

    elif color == 'blue':
        string = '\u001b[48;5;21m' + string + '\u001b[0m'

    return string

def render(board): # board rendering
    
    global selectedPos
    global positions
    global LUT
    win = True
    
    if promoting == False:
        clearScreen()
        if turn == "b": # print turn
            print(color("      Black     ","blue"))

        else: 
            print(color("      White     ","blue"))
            
        for i in range(8):
            for j in range(8):
                item = LUT[board[i][j]]
                if i == cursorPos[0] and j == cursorPos[1]:
                    item = color(item, 'orange') # cursor

                if selectedPos != [-1,-1] and [i,j] in positions:
                    if board[i][j][0] == opositeTurn(turn) or selectedPos == turn:
                        item = color(item, 'red') # movable

                    else:
                        item = color(item, 'lightMove') # movable

                if i == cursorPos[0] and j == cursorPos[1] and cursorPos == selectedPos:
                    item = color(item, 'yellow') # selected and cursor in same position

                if i == selectedPos[0] and j == selectedPos[1]:
                    item = color(item, 'green') # selected

                if (i+j) % 2 == 0: #flip-flop for white and black bacground
                    item = color(item, 'white')

                if board[i][j] == turn + "K":
                    win = False

                print(item,end='')
            print()
        
        if win == True: # win scene
            clearScreen()
            if opositeTurn(turn) == "w":
                for i in range(3):
                    for j in range(6):
                        print(color("♚ ",random.choice(["white",'darkMove','green','lightMove','orange'])), end = "")
                    print()

                print(color(" White wins ","blue"))
                for i in range(3):
                    for j in range(6):
                        print(color("♚ ",random.choice(["white",'darkMove','green','lightMove','orange'])), end = "")
                    print()
                time.sleep(3)
                exit()

            if opositeTurn(turn) == "b":
                for i in range(3):
                    for j in range(6):
                        print(color("♔ ",random.choice(["white",'darkMove','green','lightMove','orange'])), end = "")
                    print()
                print(color(" Black wins ","blue"))
                for i in range(3):
                    for j in range(6):
                        print(color("♔ ",random.choice(["white",'darkMove','green','lightMove','orange'])), end = "")
                    print()
                time.sleep(3)
                exit()
render(board) # first frame rendering
with Listener(on_press=onPress) as l: # input handling
    l.join()