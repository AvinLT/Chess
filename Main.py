import pygame
from pygame.locals import *
import sys

clock = pygame.time.Clock()  # initialize clock
pygame.init()  # initialize pygame

WINDOW_SIZE = (350, 300)  # window size
DISPLAY_SIZE = (350, 300) # display size
display = pygame.Surface(DISPLAY_SIZE)  # what we display images on. later print 'display' on screen
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)  # initialize window

# image sprites
pawn = pygame.image.load("Sprites\pawn.png")
rook = pygame.image.load(r'Sprites\rook.png')
bishop = pygame.image.load(r"Sprites\bishop.png")
queen = pygame.image.load(r"Sprites\queen.png")
king = pygame.image.load(r"Sprites\king.png")
horse = pygame.image.load(r"Sprites\horse.png")

# pieces on board
boardPieces = [["r", "h", "b", "q", "k", "b", "h", "r"],
               ["p", "p", "p", "p", "o", "p", "p", "p"],
               ["o", "o", "o", "o", "o", "o", "k", "o"],
               ["o", "o", "o", "h", "o", "o", "k", "o"],
               ["o", "q", "o", "h", "o", "o", "o", "o"],
               ["o", "o", "o", "o", "o", "k", "o", "o"],
               ["p", "p", "p", "p", "p", "p", "p", "p"],
               ["r", "h", "b", "k", "q", "b", "h", "r"]]

# board to indicate each player
boardPlayer = [["2", "2", "2", "2", "2", "2", "2", "2"],
               ["2", "2", "2", "2", "0", "2", "2", "2"],
               ["0", "0", "0", "0", "0", "0", "1", "0"],
               ["0", "0", "0", "1", "0", "0", "1", "0"],
               ["0", "1", "0", "1", "0", "0", "0", "0"],
               ["0", "0", "0", "0", "0", "1", "0", "0"],
               ["1", "1", "1", "1", "1", "1", "1", "1"],
               ["1", "1", "1", "1", "1", "1", "1", "1"]]

boardRects = [] # a board of rects for each tile
boardMarker = [] # a board with numbers corresponding to the colour of the tile
boardStart = (45, 20) # top left corner of board
tileSize = 32
borderSize = 4

# colour codes
white = (255, 255, 255)
black = (0, 0, 0)
brown = (213, 157, 0)
darkBrown = (142, 90, 0)
cream = (252, 214, 112)
lightGreen = (174, 255, 144)
darkGreen = (61, 233, 71)
lightRed = (255, 84, 84)


global moving
moving = False

# fills boardMarker and boardRects
for j in range(8):
    row = []
    row1 = []
    for i in range(8):
        row.append(pygame.Rect(i * tileSize, j * tileSize, tileSize, tileSize))
        row1.append((i + j) % 2)
    boardRects.append(row)
    boardMarker.append((row1))
    

# darws board
def drawBoard(boardRects, boardMarker):
    for j in range(8):
        for i in range(8):
            if boardMarker[j][i] == 0: # white tile
                pygame.draw.rect(display, cream, boardRects[j][i])
            elif boardMarker[j][i] == 1: # black tile
                pygame.draw.rect(display, brown, boardRects[j][i])
            elif boardMarker[j][i] == 2: # tile where the cursor is on
                pygame.draw.rect(display, darkGreen, boardRects[j][i])
            elif boardMarker[j][i] == 3: # tile where cursor has been clicked
                pygame.draw.rect(display, lightGreen, boardRects[j][i])
                pygame.draw.rect(display, darkGreen, boardRects[j][i], 1)
            elif boardMarker[j][i] == 4: # tile where the cursor is on
                pygame.draw.rect(display, lightRed, boardRects[j][i])

    # border of the board
    pygame.draw.rect(display, darkBrown, pygame.Rect(0, 0, tileSize * 8, tileSize * 8), borderSize)

# draws chess pieces
def drawPieces(boardPieces):
    for j in range(len(boardPieces)):
        for i in range(len(boardPieces)):
            if boardPieces[j][i] == "p":
                display.blit(pawn, [i * tileSize, j * tileSize])
            elif boardPieces[j][i] == "r":
                display.blit(rook, [i * tileSize, j * tileSize])
            elif boardPieces[j][i] == "h":
                display.blit(horse, [i * tileSize, j * tileSize])
            elif boardPieces[j][i] == "b":
                display.blit(bishop, [i * tileSize, j * tileSize])
            elif boardPieces[j][i] == "q":
                display.blit(queen, [i * tileSize, j * tileSize])
            elif boardPieces[j][i] == "k":
                display.blit(king, [i * tileSize, j * tileSize])

# changes the colour indication for the tile where the cursor is on
def cursor(loc, tileSize, boardStart, boardMarker, boardPlayer, click):
    mx = loc[0] - boardStart[0]
    my = loc[1] - boardStart[1]
    global moving

    if not moving:
        for j in range(8): # resets the colour marker for all tiles
            for i in range(8):
                boardMarker[j][i] = (i + j) % 2

        for j in range(0, tileSize * 8, tileSize):
            if my >= j and my <= j + tileSize:
                for i in range(0, tileSize * 8, tileSize):
                    if mx >= i and mx <= i + tileSize:
                        if click == 0:

                            boardMarker[j // tileSize][i // tileSize] = 2 # makes tiles light green
                        elif click == 1:
                            moving = True
                            boardMarker[j // tileSize][i // tileSize] = 3 # makes tiles dark green
                            boardMarker = moveOption(boardPieces, boardMarker, boardPlayer, (j // tileSize, i // tileSize))

    return boardMarker

def moveValid(tilePos, boardPlayer):
    if tilePos[0] < 0 or tilePos[0] > 7:
        return 1 # out of the board
    if tilePos[1] < 0 or tilePos[1] > 7:
        return 1 # out of the board
    if boardPlayer[tilePos[0]][tilePos[1]] == "2":
        return 2 # enemy piece
    if boardPlayer[tilePos[0]][tilePos[1]] == "1":
        return 3 # same team piece


    return 0

# changes the tiles where the horse can move to 3 or 4. 3 means empty tile. 4 is enemy tile
def rookOption(boardPieces, boardMarker, boardPlayer, tilePos):
    j, i = tilePos
    piece = boardPieces[j][i]


    for k in [-1, 1]:
        c = 0
        while moveValid([j + c + k, i], boardPlayer) == 0:
            boardMarker[j + c + k][i] = 3
            c += k

        if moveValid([j + c + k, i], boardPlayer) == 2:
            boardMarker[j + c + k][i] = 4

    for k in [-1, 1]:
        c = 0
        while moveValid([j, i + c + k], boardPlayer) == 0:
            boardMarker[j][i + c + k] = 3
            c += k
        if moveValid([j, i + c + k], boardPlayer) == 2:
            boardMarker[j][i + c + k] = 4

    return boardMarker

# changes the tiles where the bishop can move to 3 or 4. 3 means empty tile. 4 is enemy tile
def bishopOption(boardPieces, boardMarker, boardPlayer, tilePos):
    j, i = tilePos
    piece = boardPieces[j][i]

    for k in [-1, 1]:
        c = 0

        while moveValid([j + c + k, i + c + k], boardPlayer) == 0:
            boardMarker[j + c + k][i + c + k] = 3
            c += k
        if moveValid([j + c + k, i + c + k], boardPlayer) == 2:
            boardMarker[j + c + k][i + c + k] = 4

    for k in [-1, 1]:
        c = 0

        while moveValid([j + c + k, i + (c + k) * -1], boardPlayer) == 0:
            boardMarker[j + c + k][i + (c + k) * -1] = 3
            c += k
        if moveValid([j + c + k, i + (c + k) * -1], boardPlayer) == 2:
            boardMarker[j + c + k][i + (c + k) * -1] = 4

    return boardMarker

# changes the tiles where the chosen piece can move to 3 or 4. 3 means empty tile. 4 is enemy tile
def moveOption(boardPieces, boardMarker, boardPlayer, tilePos):
    j, i = tilePos
    piece = boardPieces[j][i]

    if piece == "p":
        if moveValid([j - 1, i], boardPlayer) == 0:
            boardMarker[j - 1][i] = 3
        if j == 6:
            if moveValid([j - 2, i], boardPlayer) == 0:
                boardMarker[j - 2][i] = 3

    elif piece == "r":
        rookOption(boardPieces, boardMarker, boardPlayer, tilePos)

    elif piece == "b":
        bishopOption(boardPieces, boardMarker, boardPlayer, tilePos)

    elif piece == "h":
        for k in [-1, 1]:
            for c in [-1, 1]:
                if moveValid([j + 2 * k, i + c], boardPlayer) == 0:
                    boardMarker[j + 2 * k][i + c] = 3
                if moveValid([j + 2 * k, i + c], boardPlayer) == 2:
                    boardMarker[j + 2 * k][i + c] = 4

        for k in [-1, 1]:
            for c in [-1, 1]:
                if moveValid([j + c, i + 2 * k], boardPlayer) == 0:
                    boardMarker[j + c][i + 2 * k] = 3
                elif moveValid([j + c, i + 2 * k], boardPlayer) == 2:
                    boardMarker[j + c][i + 2 * k] = 4

    elif piece == "q":
        rookOption(boardPieces, boardMarker, boardPlayer, tilePos)
        bishopOption(boardPieces, boardMarker, boardPlayer, tilePos)

    elif piece == "k":
        for k in [0, 1]:
            if moveValid([j - 1, i + k], boardPlayer) == 0:
                boardMarker[j - 1][i + k] = 3
            elif moveValid([j - 1, i + k], boardPlayer) == 2:
                boardMarker[j - 1][i + k] = 4
        for k in [0, 1]:
            if moveValid([j + k, i + 1], boardPlayer) == 0:
                boardMarker[j + k][i + 1] = 3
            elif moveValid([j + k, i + 1], boardPlayer) == 2:
                boardMarker[j + k][i + 1] = 4
        for k in [0, -1]:
            if moveValid([j + 1, i + k], boardPlayer) == 0:
                boardMarker[j + 1][i + k] = 3
            elif moveValid([j + 1, i + k], boardPlayer) == 2:
                boardMarker[j + 1][i + k] = 4
        for k in [0, -1]:
            if moveValid([j + k, i - 1], boardPlayer) == 0:
                boardMarker[j + k][i - 1] = 3
            if moveValid([j + k, i - 1], boardPlayer) == 2:
                boardMarker[j + k][i - 1] = 4



    return boardMarker
                
            
            



# Main game loop
while True:

    display.fill((0, 0, 0)) # makes display black

    mx, my = pygame.mouse.get_pos() # gets cursor co-ords
    loc = [mx, my]
    click = 0 # indicates whether mouse has been clicked

    for event in pygame.event.get():  # event loop
        if event.type == QUIT:  # checks if window is closed
            pygame.quit()  # stops pygame
            sys.exit()  # stops script
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1: # left click
                click = 1



    cursor(loc, tileSize, boardStart, boardMarker, boardPlayer, click)
    drawBoard(boardRects, boardMarker)
    drawPieces(boardPieces)




    #mainDisplay = pygame.transform.scale(display, WINDOW_SIZE)
    screen.blit(display, (boardStart[0],boardStart[1]))
    pygame.display.update()  # update display
    clock.tick(60)  # set frame rate
