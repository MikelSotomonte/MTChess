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

def selectOrMove():
    global selectedPos
    global turn
    global board
    if board[cursorPos[0]][cursorPos[1]][0] == turn:
        selectedPos = cursorPos.copy()
    elif selectedPos != [-1,-1]:
        board[cursorPos[0]][cursorPos[1]] = board[selectedPos[0]][selectedPos[1]]
        board[selectedPos[0]][selectedPos[1]] = '-'
        selectedPos = [-1,-1]
        if turn == 'w': turn = 'b'
        else: turn = 'w' 
        
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
    return string

def render(board):
    global selectedPos

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

    MoveLut = {
        'bP': [[1,1],[1,-1],[-1,2],[-1,0]],
    
        'bR': [[-1, 0], [1, 0], [0, -1], [0, 1], [-2, 0], [2, 0], [0, -2], [0, 2], [-3, 0], [3, 0], [0, -3], [0, 3], [-4, 0], [4, 0], [0, -4], [0, 4], [-5, 0], [5, 0], [0, -5], [0, 5], [-6, 0], [6, 0], [0, -6], [0, 6], [-7, 0], [7, 0], [0, -7], [0, 7]],
        'bN': [[1,-2],[1,2],[2,1],[2,-1],[-1,-2],[-1,2],[-2,1],[-2,-1]],
        
        'bB': [[1, 1], [1, -1], [-1, 1], [-1, -1], [2, 2], [2, -2], [-2, 2], [-2, -2], [3, 3], [3, -3], [-3, 3], [-3, -3], [4, 4], [4, -4], [-4, 4], [-4, -4], [5, 5], [5, -5], [-5, 5], [-5, -5], [6, 6], [6, -6], [-6, 6], [-6, -6], [7, 7], [7, -7], [-7, 7], [-7, -7]],
        'bR': [[0,-1],[0,-2],[0,-3],[0,-4],[0,-5],[0,-6],[0,-7],[0,1],[0,2],[0,3],[0,4],[0,5],[0,6],[0,7],[-1,0],[-2,0],[-3,0],[-4,0],[-5,0],[-6,0],[-7,0],[1,0],[2,0],[3,0],[4,0],[5,0],[6,0],[7,0]],
        'bQ': [[0,-1],[0,-2],[0,-3],[0,-4],[0,-5],[0,-6],[0,-7],[0,1],[0,2],[0,3],[0,4],[0,5],[0,6],[0,7],[-1,0],[-2,0],[-3,0],[-4,0],[-5,0],[-6,0],[-7,0],[1,0],[2,0],[3,0],[4,0],[5,0],[6,0],[7,0],[1,1],[2,2],[3,3],[4,4],[5,5],[6,6],[7,7],[-1,1],[-2,2],[-3,3],[-4,4],[-5,5],[-6,6],[-7,7],[1,-1],[2,-2],[3,-3],[4,-4],[5,-5],[6,-6],[7,-7],[-1,-1],[-2,-2],[-3,-3],[-4,-4],[-5,-5],[-6,-6],[-7,-7]],
        'bK': [[0,-1],[0,-2],[1,-1],[-1,-1]],
        'wP': [[0,1],[0,2],[1,1],[-1,1]],
        'wN': [[1,-2],[1,2],[2,1],[2,-1],[-1,-2],[-1,2],[-2,1],[-2,-1]],
        'wB': [[-1,0],[-2,0],[-1,1],[-1,-1]],
        'wR': [[0,-1],[0,-2],[0,-3],[0,-4],[0,-5],[0,-6],[0,-7],[0,1],[0,2],[0,3],[0,4],[0,5],[0,6],[0,7],[-1,0],[-2,0],[-3,0],[-4,0],[-5,0],[-6,0],[-7,0],[1,0],[2,0],[3,0],[4,0],[5,0],[6,0],[7,0]],
        'wQ': [[0,-1],[0,-2],[0,-3],[0,-4],[0,-5],[0,-6],[0,-7],[0,1],[0,2],[0,3],[0,4],[0,5],[0,6],[0,7],[-1,0],[-2,0],[-3,0],[-4,0],[-5,0],[-6,0],[-7,0],[1,0],[2,0],[3,0],[4,0],[5,0],[6,0],[7,0],[1,1],[2,2],[3,3],[4,4],[5,5],[6,6],[7,7],[-1,1],[-2,2],[-3,3],[-4,4],[-5,5],[-6,6],[-7,7],[1,-1],[2,-2],[3,-3],[4,-4],[5,-5],[6,-6],[7,-7],[-1,-1],[-2,-2],[-3,-3],[-4,-4],[-5,-5],[-6,-6],[-7,-7]],
        'wK': [[0,-1],[0,-2],[1,-1],[-1,-1]],
    }
    time.sleep(0.1)
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('cls')
    for i in range(8):
        for j in range(8):
            item = LUT[board[i][j]]
            if i == cursorPos[0] and j == cursorPos[1] and cursorPos == selectedPos:
                item = color(item, 'yellow') #Selected and cursor in same position
            if i == selectedPos[0] and j == selectedPos[1]:
                item = color(item, 'green') # selected
            if i == cursorPos[0] and j == cursorPos[1]:
                item = color(item, 'orange') # Cursor
            movablePos[0] = selectedPos[0] - i
            movablePos[1] = selectedPos[1] - j
            if selectedPos != [-1,-1] and movablePos in MoveLut[board[selectedPos[0]][selectedPos[1]]]:
                item = color(item, 'lightMove') #Movable
            if (i+j) % 2 == 0:
                item = color(item, 'white')
            print(item,end='')
        print()

board = [['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
         ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
         ['-',  '-',  '-',  '-',  '-',  '-',  '-',  '-' ],
         ['-',  '-',  '-',  '-',  '-',  '-',  '-',  '-' ],
         ['-',  '-',  '-',  '-',  '-',  '-',  '-',  '-' ],
         ['-',  '-',  '-',  '-',  '-',  '-',  '-',  '-' ],
         ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
         ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']]

cursorPos = [4,4]
selectedPos = [-1,-1]
movablePos = [-1,-1]
turn = 'w'
with Listener(on_press=onPress) as l:
    l.join()