#input
from pynput.keyboard import Listener
import os
import time

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

def movementsRaycast(a,b):
    global selectedPos
    global board
    global turn
    global positions
    
    for i in range(1, 8, 1):
        if selectedPos[1]+i*a <= 7 and selectedPos[1]+i*a >= 0 and selectedPos[1]+i*b <= 7 and  + selectedPos[1]+i*b >= 0:
            if board[selectedPos[0]+i*a][selectedPos[1]+i*b][0] == '-': #spaces
                positions.append([selectedPos[0]+i*a, selectedPos[1]+i*b])
            elif board[selectedPos[0]+i*a][selectedPos[1]+i*b][0] == turn: #same color pices
                break
            elif board[selectedPos[0]+i*a][selectedPos[1]+i*b][0] == opositeTurn(turn): #other color pices to stop moving after that
                positions.append([selectedPos[0]+i*a, selectedPos[1]+i*b])
                break
        else: break


def selectOrMove():
    global selectedPos
    global turn
    global board
    global positions
    if board[cursorPos[0]][cursorPos[1]][0] == turn:
        selectedPos = cursorPos.copy()
        positions = []
        #===ROOK===#
        if board[cursorPos[0]][cursorPos[1]][1] == 'R':
            movementsRaycast(1,0)
            movementsRaycast(0,1)
            movementsRaycast(-1,0)
            movementsRaycast(0,-1)
        #===BISHOP===#
        if board[cursorPos[0]][cursorPos[1]][1] == 'B':
            movementsRaycast(1,1)
            movementsRaycast(-1,1)
            movementsRaycast(1,-1)
            movementsRaycast(-1,-1)
        #===QWEEN===#
        if board[cursorPos[0]][cursorPos[1]][1] == 'Q':
            movementsRaycast(1,1)
            movementsRaycast(-1,1)
            movementsRaycast(1,-1)
            movementsRaycast(-1,-1)
            movementsRaycast(1,0)
            movementsRaycast(0,1)
            movementsRaycast(-1,0)
            movementsRaycast(0,-1)
        #===PAWN===#
        if board[cursorPos[0]][cursorPos[1]][1] == 'P':
            if turn == 'w': direction = -1
            elif turn == 'b': direction = 1
            if board[selectedPos[0]+direction][selectedPos[1]-1][0] == opositeTurn(turn): # can eat left
                positions.append([selectedPos[0]+direction,selectedPos[1]-1])
            if board[selectedPos[0]+direction][selectedPos[1]+1][0] == opositeTurn(turn): # can eat right
                positions.append([selectedPos[0]+direction,selectedPos[1]+1])
            if board[selectedPos[0]+direction][selectedPos[1]][0] == '-': # can move one
                positions.append([selectedPos[0]+direction,selectedPos[1]])
                if selectedPos[0] == 6 and board[4][selectedPos[1]][0] == '-' and board[cursorPos[0]][cursorPos[1]][0] == 'w': # can move two
                    positions.append([4,selectedPos[1]])
                if selectedPos[0] == 1 and board[3][selectedPos[1]][0] == '-' and board[cursorPos[0]][cursorPos[1]][0] == 'b': # can move two
                    positions.append([3,selectedPos[1]])


    elif selectedPos != [-1,-1]:
        if [cursorPos[0],cursorPos[1]] in positions:
            board[cursorPos[0]][cursorPos[1]] = board[selectedPos[0]][selectedPos[1]]
            board[selectedPos[0]][selectedPos[1]] = '-'
            turn = opositeTurn(turn)
        selectedPos = [-1,-1]
        
        
def color(string, color=''):
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
    global movablePos
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
        '-': '  ',
    }

    # MoveLut = {
    #     'bP': [[-1,-1],[-1,1],[-1,0],[-2,0]],
    #     'bN': [[1,-2],[1,2],[2,1],[2,-1],[-1,-2],[-1,2],[-2,1],[-2,-1]],
    #     'bB': [[1,1],[1,-1],[-1,1],[-1,-1],[2,2],[2,-2],[-2,2],[-2,-2],[3,3],[3,-3],[-3,3],[-3,-3],[4,4],[4,-4],[-4,4],[-4,-4],[5,5],[5,-5],[-5,5],[-5,-5],[6,6],[6,-6],[-6,6],[-6,-6],[7,7],[7,-7],[-7,7],[-7,-7]],
    #     'bR': [[0,-1],[0,-2],[0,-3],[0,-4],[0,-5],[0,-6],[0,-7],[0,1],[0,2],[0,3],[0,4],[0,5],[0,6],[0,7],[-1,0],[-2,0],[-3,0],[-4,0],[-5,0],[-6,0],[-7,0],[1,0],[2,0],[3,0],[4,0],[5,0],[6,0],[7,0]],
    #     'bQ': [[0,-1],[0,-2],[0,-3],[0,-4],[0,-5],[0,-6],[0,-7],[0,1],[0,2],[0,3],[0,4],[0,5],[0,6],[0,7],[-1,0],[-2,0],[-3,0],[-4,0],[-5,0],[-6,0],[-7,0],[1,0],[2,0],[3,0],[4,0],[5,0],[6,0],[7,0],[1,1],[2,2],[3,3],[4,4],[5,5],[6,6],[7,7],[-1,1],[-2,2],[-3,3],[-4,4],[-5,5],[-6,6],[-7,7],[1,-1],[2,-2],[3,-3],[4,-4],[5,-5],[6,-6],[7,-7],[-1,-1],[-2,-2],[-3,-3],[-4,-4],[-5,-5],[-6,-6],[-7,-7]],
    #     'bK': [[-1,0],[1,0],[0,1],[0,-1],[1,-1],[-1,-1],[-1,1],[1,1]],
    #     'wP': [[1,-1],[1,1],[1,0],[2,0]],
    #     'wN': [[1,-2],[1,2],[2,1],[2,-1],[-1,-2],[-1,2],[-2,1],[-2,-1]],
    #     'wB': [[1,1],[1,-1],[-1,1], [-1,-1],[2,2],[2,-2],[-2,2],[-2,-2], [3,3],[3,-3],[-3,3],[-3,-3],[4,4],[4,-4],[-4,4],[-4,-4],[5,5],[5,-5],[-5,5],[-5,-5],[6,6],[6,-6],[-6,6],[-6,-6],[7,7],[7,-7],[-7,7],[-7,-7]],
    #     'wR': [[0,-1],[0,-2],[0,-3],[0,-4],[0,-5],[0,-6],[0,-7],[0,1],[0,2],[0,3],[0,4],[0,5],[0,6],[0,7],[-1,0],[-2,0],[-3,0],[-4,0],[-5,0],[-6,0],[-7,0],[1,0],[2,0],[3,0],[4,0],[5,0],[6,0],[7,0]],
    #     'wQ': [[0,-1],[0,-2],[0,-3],[0,-4],[0,-5],[0,-6],[0,-7],[0,1],[0,2],[0,3],[0,4],[0,5],[0,6],[0,7],[-1,0],[-2,0],[-3,0],[-4,0],[-5,0],[-6,0],[-7,0],[1,0],[2,0],[3,0],[4,0],[5,0],[6,0],[7,0],[1,1],[2,2],[3,3],[4,4],[5,5],[6,6],[7,7],[-1,1],[-2,2],[-3,3],[-4,4],[-5,5],[-6,6],[-7,7],[1,-1],[2,-2],[3,-3],[4,-4],[5,-5],[6,-6],[7,-7],[-1,-1],[-2,-2],[-3,-3],[-4,-4],[-5,-5],[-6,-6],[-7,-7]],
    #     'wK': [[-1,0],[1,0],[0,1],[0,-1],[1,-1],[-1,-1],[-1,1],[1,1]],
    # }
    clearScreen()
    for i in range(8):
        for j in range(8):
            item = LUT[board[i][j]]
            if i == cursorPos[0] and j == cursorPos[1] and cursorPos == selectedPos:
                item = color(item, 'yellow') #Selected and cursor in same position
            if i == selectedPos[0] and j == selectedPos[1]:
                item = color(item, 'green') # selected
            if i == cursorPos[0] and j == cursorPos[1]:
                item = color(item, 'orange') # Cursor
            
            #if selectedPos != [-1,-1] and movablePos in MoveLut[board[selectedPos[0]][selectedPos[1]]]:
            if selectedPos != [-1,-1] and [i,j] in positions:
                if board[i][j][0] == opositeTurn(turn):
                    item = color(item, 'red') #Movable
                else:
                    item = color(item, 'lightMove') #Movable
            if (i+j) % 2 == 0:
                item = color(item, 'white')
            print(item,end='')
        print()

board = [['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
         ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
         ['-',  '-',  '-',  '-',  '-',  '-',  '-',  '-' ],
         ['-',  '-',  'wR',  '-',  '-',  '-',  '-',  '-' ],
         ['-',  '-',  '-',  '-',  'bR',  '-',  '-',  '-' ],
         ['-',  '-',  '-',  '-',  '-',  '-',  '-',  '-' ],
         ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
         ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']]

cursorPos = [4,4]
selectedPos = [-1,-1]
movablePos = [-1,-1]
turn = 'w'
positions = []

with Listener(on_press=onPress) as l:
    l.join()