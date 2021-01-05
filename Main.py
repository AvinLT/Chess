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
               ["p", "p", "p", "p", "p", "p", "p", "p"],
               ["o", "o", "o", "o", "o", "o", "o", "o"],
               ["o", "o", "o", "o", "o", "o", "o", "o"],
               ["o", "o", "o", "o", "o", "o", "o", "o"],
               ["o", "o", "o", "o", "o", "o", "o", "o"],
               ["p", "p", "p", "p", "p", "p", "p", "p"],
               ["r", "h", "b", "k", "q", "b", "h", "r"]]

# board to indicate each player
boardPlayer = [["2", "2", "2", "2", "2", "2", "2", "2"],
               ["2", "2", "2", "2", "2", "2", "2", "2"],
               ["0", "0", "0", "0", "0", "0", "0", "0"],
               ["0", "0", "0", "0", "0", "0", "0", "0"],
               ["0", "0", "0", "0", "0", "0", "0", "0"],
               ["0", "0", "0", "0", "0", "0", "0", "0"],
               ["1", "1", "1", "1", "1", "1", "1", "1"],
               ["1", "1", "1", "1", "1", "1", "1", "1"]]

boardTiles = [] # will consist of board. but each element is a list in this format: [rect for tile, tile colour marker]
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

# fills boardTiles
# each element is a list in this format: [rect for tile, tile colour marker]
for j in range(8):
    row = []
    for i in range(8):
        row.append(
            [pygame.Rect(i * tileSize, j * tileSize, tileSize, tileSize), (i + j) % 2])
    boardTiles.append(row)

# darws board
def drawBoard(boardTiles):
    for j in range(len(boardTiles)):
        for i in range(len(boardTiles[0])):
            if boardTiles[j][i][1] == 0: # white tile
                pygame.draw.rect(display, cream, boardTiles[j][i][0])
            elif boardTiles[j][i][1] == 1: # black tile
                pygame.draw.rect(display, brown, boardTiles[j][i][0])
            elif boardTiles[j][i][1] == 2: # tile where the cursor is on
                pygame.draw.rect(display, lightGreen, boardTiles[j][i][0])
            elif boardTiles[j][i][1] == 3: # tile where cursor has been clicked
                pygame.draw.rect(display, darkGreen, boardTiles[j][i][0])

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
def cursor(loc, tileSize, boardStart, boardTiles, click):
    mx = loc[0] - boardStart[0]
    my = loc[1] - boardStart[1]

    for j in range(8):
        for i in range(8):
            boardTiles[j][i][1] = (i + j) % 2

    for j in range(0, tileSize * 8, tileSize):
        if my >= j and my <= j + tileSize:
            for i in range(0, tileSize * 8, tileSize):
                if mx >= i and mx <= i + tileSize:
                    if click == 0:
                        boardTiles[j // tileSize][i // tileSize][1] = 2
                    elif click == 1:
                        boardTiles[j // tileSize][i // tileSize][1] = 3

    return boardTiles


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



    cursor(loc, tileSize, boardStart, boardTiles, click)
    drawBoard(boardTiles)
    drawPieces(boardPieces)




    #mainDisplay = pygame.transform.scale(display, WINDOW_SIZE)
    screen.blit(display, (boardStart[0],boardStart[1]))
    pygame.display.update()  # update display
    clock.tick(60)  # set frame rate
