import pygame
from pygame.locals import *
import sys
import copy

clock = pygame.time.Clock()  # initialize clock
pygame.init()  # initialize pygame

WINDOW_SIZE = (650, 630)  # window size
DISPLAY_SIZE = (512, 512)  # display size
display = pygame.Surface(DISPLAY_SIZE)  # what we display images on. later print 'display' on screen
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)  # initialize window




# image sprites
pawn = pygame.image.load("Sprites\pawn.png")
pawnB = pygame.image.load("Sprites\pawn (1).png")
rook = pygame.image.load(r'Sprites\rook.png')
rookB = pygame.image.load(r'Sprites\rook (1).png')
bishop = pygame.image.load(r"Sprites\bishop.png")
bishopB = pygame.image.load(r"Sprites\bishop (1).png")
queen = pygame.image.load(r"Sprites\queen.png")
queenB = pygame.image.load(r"Sprites\queen (1).png")
king = pygame.image.load(r"Sprites\king.png")
kingB = pygame.image.load(r"Sprites\king (1).png")
horse = pygame.image.load(r"Sprites\horse.png")
horseB = pygame.image.load(r"Sprites\horse (1).png")

pieces = {"p": [pawn, pawnB], "r": [rook, rookB], "b": [bishop, bishopB],
          "q": [queen, queenB], "k": [king, kingB], "h": [horse, horseB]}

backGround = pygame.image.load(r"Sprites\woodBackground.jpg")

fontStyle = pygame.font.SysFont("franklingothicmedium", 70, bold = True)

textBlack =     "     BLACK'S MOVE     "
textWhite =     "     WHITE'S MOVE     "
textCheck =     "       IN CHECK       "
textCHECKMATE = "      CHECKMATE!      "

texts = [textBlack, textWhite, textCheck, textCHECKMATE]


# pieces on board
boardPieces = [["r", "h", "b", "q", "k", "b", "h", "r"],
               ["p", "p", "p", "p", "p", "p", "p", "p"],
               ["o", "o", "o", "o", "o", "o", "o", "o"],
               ["o", "o", "o", "o", "o", "o", "o", "o"],
               ["o", "o", "o", "o", "o", "o", "o", "o"],
               ["o", "o", "o", "o", "o", "o", "o", "o"],
               ["p", "p", "p", "p", "p", "p", "p", "p"],
               ["r", "h", "b", "q", "k", "b", "h", "r"]]

boardPieces = [["r", "o", "b", "q", "k", "b", "h", "r"],
               ["p", "p", "p", "p", "o", "p", "p", "p"],
               ["o", "o", "o", "o", "o", "o", "o", "o"],
               ["o", "o", "o", "o", "p", "o", "o", "o"],
               ["o", "o", "o", "h", "p", "o", "p", "o"],
               ["o", "o", "h", "o", "o", "o", "o", "o"],
               ["p", "p", "p", "p", "h", "p", "p", "p"],
               ["r", "o", "b", "q", "k", "b", "o", "r"]]
# board to indicate each player
boardPlayer = [[2, 2, 2, 2, 2, 2, 2, 2],
               [2, 2, 2, 2, 2, 2, 2, 2],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [1, 1, 1, 1, 1, 1, 1, 1],
               [1, 1, 1, 1, 1, 1, 1, 1]]

boardPlayer = [[2, 0, 2, 2, 2, 2, 2, 2],
               [2, 2, 2, 2, 0, 2, 2, 2],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 2, 0, 0, 0],
               [0, 0, 0, 2, 1, 0, 1, 0],
               [0, 0, 1, 0, 0, 0, 0, 0],
               [1, 1, 1, 1, 1, 1, 1, 1],
               [1, 0, 1, 1, 1, 1, 0, 1]]

boardRects = []  # a board of rects for each tile
boardMarker = []  # a board with numbers corresponding to the colour of the tile
boardStart = (64, 32)  # top left corner of board
tileSize = 64
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

tempJI = [0, 0]  # displacement of the piece for original position when moving
animation = False  # the animation of a piece is occuring
moving = False  # player is in the process of choosing a piece, include animation
initialPos = [0, 0]  # initial position of piece picked
grads = [0, 0]  # y and x speed of the piece in animation
ignore = None  # holds positon of the piece which is in animation.
turn = 0
inCheck = False
inCheckMate = False
pauseTimeMark = 60
pauseTime = pauseTimeMark

# fills boardMarker and boardRects
for j in range(8):
    row = []
    row1 = []
    for i in range(8):
        row.append(pygame.Rect(i * tileSize, j * tileSize, tileSize, tileSize))
        row1.append((i + j) % 2)
    boardRects.append(row)
    boardMarker.append((row1))


# draws board
def drawBoard(boardRects, boardMarker):
    for j in range(8):
        for i in range(8):
            if boardMarker[j][i] == 0:  # white tile
                pygame.draw.rect(display, cream, boardRects[j][i])
            elif boardMarker[j][i] == 1:  # black tile
                pygame.draw.rect(display, brown, boardRects[j][i])
            elif boardMarker[j][i] == 2:  # tile where the cursor is on
                pygame.draw.rect(display, darkGreen, boardRects[j][i])
            elif boardMarker[j][i] == 3:  # tile where cursor has been clicked
                pygame.draw.rect(display, lightGreen, boardRects[j][i])
                pygame.draw.rect(display, darkGreen, boardRects[j][i], 1)
            elif boardMarker[j][i] == 4:  # tile where the cursor is on
                pygame.draw.rect(display, lightRed, boardRects[j][i])

    # border of the board
    pygame.draw.rect(display, darkBrown, pygame.Rect(0, 0, tileSize * 8, tileSize * 8), borderSize)


# draws chess pieces
def drawPieces(boardPieces, turn, boardPlayer, ignore):
    for j in range(len(boardPieces)):
        for i in range(len(boardPieces)):
            if [j, i] != ignore:
                temp = 0 if (turn + boardPlayer[j][i]) % 2 == 1 else 1

                if boardPieces[j][i] == "p":
                    display.blit(pieces["p"][temp], [i * tileSize, j * tileSize])
                elif boardPieces[j][i] == "r":
                    display.blit(pieces["r"][temp], [i * tileSize, j * tileSize])
                elif boardPieces[j][i] == "h":
                    display.blit(pieces["h"][temp], [i * tileSize, j * tileSize])
                elif boardPieces[j][i] == "b":
                    display.blit(pieces["b"][temp], [i * tileSize, j * tileSize])
                elif boardPieces[j][i] == "q":
                    display.blit(pieces["q"][temp], [i * tileSize, j * tileSize])
                elif boardPieces[j][i] == "k":
                    display.blit(pieces["k"][temp], [i * tileSize, j * tileSize])

def drawText(texts, fontStyle, displayDim, check, checkmate, turn, textColour, boardStart):

    if check:
        textStart = [(displayDim[0] / 2 - fontStyle.size(texts[2])[0] / 2) + boardStart[0], displayDim[1] + boardStart[1]]
        textObj = fontStyle.render(texts[2], 1, textColour)
    elif checkmate:
        textStart = [(displayDim[0] / 2 - fontStyle.size(texts[3])[0] / 2) + boardStart[0],displayDim[1] + boardStart[1]]
        textObj = fontStyle.render(texts[3], 1, textColour)
    else:
        if turn == 0:
            textStart = [(displayDim[0] / 2 - fontStyle.size(texts[1])[0] / 2) + boardStart[0], displayDim[1] + boardStart[1]]
            textObj = fontStyle.render(texts[1], 1, textColour)
        else:
            textStart = [(displayDim[0] / 2 - fontStyle.size(texts[0])[0] / 2) + boardStart[0], displayDim[1] + boardStart[1]]
            textObj = fontStyle.render(texts[0], 1, textColour)

    screen.blit(textObj, textStart)
    
    
# changes the colour indication for the tile where the cursor is on
def cursor(loc, tileSize, boardStart, boardMarker, boardPlayer, click, tilePos):
    mx = loc[0] - boardStart[0]
    my = loc[1] - boardStart[1]
    global moving

    if not moving:
        tilePos = [0, 0]

    if not moving:
        for j in range(8):  # resets the colour marker for all tiles
            for i in range(8):
                boardMarker[j][i] = (i + j) % 2

        for j in range(0, tileSize * 8, tileSize):
            if my >= j and my <= j + tileSize:
                for i in range(0, tileSize * 8, tileSize):
                    if mx >= i and mx <= i + tileSize:
                        if click == 0:

                            boardMarker[j // tileSize][i // tileSize] = 2  # makes tiles dark green
                        elif click == 1:
                            if boardPlayer[j // tileSize][i // tileSize] == 1:
                                moving = True
                                boardMarker[j // tileSize][i // tileSize] = 3  # makes tiles light green
                                tilePos = [j, i]
                                boardMarker = moveOption(boardPieces, boardMarker, boardPlayer,
                                                         (j // tileSize, i // tileSize), False)

    return boardMarker, tilePos


def moveValid(tilePos, boardPlayer, OppDir):
    if tilePos[0] < 0 or tilePos[0] > 7:
        return 1  # out of the board
    if tilePos[1] < 0 or tilePos[1] > 7:
        return 1  # out of the board
    if not OppDir:

        if boardPlayer[tilePos[0]][tilePos[1]] == 2:
            return 2  # enemy piece
        if boardPlayer[tilePos[0]][tilePos[1]] == 1:
            return 3  # same team piece
    else:
        if boardPlayer[tilePos[0]][tilePos[1]] == 1:
            return 2  # enemy piece
        if boardPlayer[tilePos[0]][tilePos[1]] == 2:
            return 3  # same team piece

    return 0


# changes the tiles where the horse can move to 3 or 4. 3 means empty tile. 4 is enemy tile
def rookOption(boardPieces, boardMarker, boardPlayer, tilePos, OppDir):
    j, i = tilePos
    piece = boardPieces[j][i]

    for k in [-1, 1]:
        c = 0
        while moveValid([j + c + k, i], boardPlayer, OppDir) == 0:
            boardMarker[j + c + k][i] = 3
            c += k

        if moveValid([j + c + k, i], boardPlayer, OppDir) == 2:
            boardMarker[j + c + k][i] = 4

    for k in [-1, 1]:
        c = 0
        while moveValid([j, i + c + k], boardPlayer, OppDir) == 0:
            boardMarker[j][i + c + k] = 3
            c += k
        if moveValid([j, i + c + k], boardPlayer, OppDir) == 2:
            boardMarker[j][i + c + k] = 4

    return boardMarker


# changes the tiles where the bishop can move to 3 or 4. 3 means empty tile. 4 is enemy tile
def bishopOption(boardPieces, boardMarker, boardPlayer, tilePos, OppDir):
    j, i = tilePos
    piece = boardPieces[j][i]

    for k in [-1, 1]:
        c = 0

        while moveValid([j + c + k, i + c + k], boardPlayer, OppDir) == 0:
            boardMarker[j + c + k][i + c + k] = 3
            c += k
        if moveValid([j + c + k, i + c + k], boardPlayer, OppDir) == 2:
            boardMarker[j + c + k][i + c + k] = 4

    for k in [-1, 1]:
        c = 0

        while moveValid([j + c + k, i + (c + k) * -1], boardPlayer, OppDir) == 0:
            boardMarker[j + c + k][i + (c + k) * -1] = 3
            c += k
        if moveValid([j + c + k, i + (c + k) * -1], boardPlayer, OppDir) == 2:
            boardMarker[j + c + k][i + (c + k) * -1] = 4

    return boardMarker


# changes the tiles where the chosen piece can move to 3 or 4. 3 means empty tile. 4 is enemy tile
def moveOption(boardPieces, boardMarker, boardPlayer, tilePos, OppDir):
    j, i = tilePos
    piece = boardPieces[j][i]



    if piece == "p":
        if not OppDir:
            if moveValid([j - 1, i], boardPlayer, OppDir) == 0:
                boardMarker[j - 1][i] = 3
            if moveValid([j - 1, i - 1], boardPlayer, OppDir) == 2:
                boardMarker[j - 1][i - 1] = 4
            if moveValid([j - 1, i + 1], boardPlayer, OppDir) == 2:
                boardMarker[j - 1][i + 1] = 4
            if j == 6:
                if moveValid([j - 2, i], boardPlayer, OppDir) == 0:
                    boardMarker[j - 2][i] = 3
        else:

            if moveValid([j + 1, i], boardPlayer, OppDir) == 0:
                boardMarker[j + 1][i] = 3
            if moveValid([j + 1, i + 1], boardPlayer, OppDir) == 2:
                boardMarker[j + 1][i + 1] = 4
            if moveValid([j + 1, i - 1], boardPlayer, OppDir) == 2:
                boardMarker[j + 1][i - 1] = 4
            if j == 1:
                if moveValid([j + 2, i], boardPlayer, OppDir) == 0:
                    boardMarker[j + 2][i] = 3

    elif piece == "r":
        rookOption(boardPieces, boardMarker, boardPlayer, tilePos, OppDir)

    elif piece == "b":
        bishopOption(boardPieces, boardMarker, boardPlayer, tilePos, OppDir)

    elif piece == "h":
        for k in [-1, 1]:
            for c in [-1, 1]:
                if moveValid([j + 2 * k, i + c], boardPlayer, OppDir) == 0:
                    boardMarker[j + 2 * k][i + c] = 3
                if moveValid([j + 2 * k, i + c], boardPlayer, OppDir) == 2:
                    boardMarker[j + 2 * k][i + c] = 4

        for k in [-1, 1]:
            for c in [-1, 1]:
                if moveValid([j + c, i + 2 * k], boardPlayer, OppDir) == 0:
                    boardMarker[j + c][i + 2 * k] = 3
                elif moveValid([j + c, i + 2 * k], boardPlayer, OppDir) == 2:
                    boardMarker[j + c][i + 2 * k] = 4

    elif piece == "q":
        rookOption(boardPieces, boardMarker, boardPlayer, tilePos, OppDir)
        bishopOption(boardPieces, boardMarker, boardPlayer, tilePos, OppDir)

    elif piece == "k":
        for k in [0, 1]:
            if moveValid([j - 1, i + k], boardPlayer, OppDir) == 0:
                boardMarker[j - 1][i + k] = 3
            elif moveValid([j - 1, i + k], boardPlayer, OppDir) == 2:
                boardMarker[j - 1][i + k] = 4
        for k in [0, 1]:
            if moveValid([j + k, i + 1], boardPlayer, OppDir) == 0:
                boardMarker[j + k][i + 1] = 3
            elif moveValid([j + k, i + 1], boardPlayer, OppDir) == 2:
                boardMarker[j + k][i + 1] = 4
        for k in [0, -1]:
            if moveValid([j + 1, i + k], boardPlayer, OppDir) == 0:
                boardMarker[j + 1][i + k] = 3
            elif moveValid([j + 1, i + k], boardPlayer, OppDir) == 2:
                boardMarker[j + 1][i + k] = 4
        for k in [0, -1]:
            if moveValid([j + k, i - 1], boardPlayer, OppDir) == 0:
                boardMarker[j + k][i - 1] = 3
            if moveValid([j + k, i - 1], boardPlayer, OppDir) == 2:
                boardMarker[j + k][i - 1] = 4

    return boardMarker

def flip(boardPlayer, boardPieces, boardMarker):
    boards = []
    for board in [boardPlayer, boardPieces, boardMarker]:

        if board == boardPlayer:
            for j in range(8):
                for i in range(8):
                    if board[j][i] == 2:
                        board[j][i] = 1
                    elif board[j][i] == 1:
                        board[j][i] = 2
                    else:
                        board[j][i] = 0

        board = [row[::-1] for row in board][::-1]
        boards.append(board)
    return boards[0], boards[1], boards[2]


def isKingCheck(boardPieces, boardPlayer, boardMarker):

    boardMarkerEmpty = resetMarker()

    kingPos = []
    boardMarkerCopy = copy.deepcopy(boardMarker)



    for j in range(8):
        for i in range(8):
            if boardPieces[j][i] == "k" and boardPlayer[j][i] == 1:
                kingPos = [j, i]

    for j in range(8):
        for i in range(8):
            if boardPlayer[j][i] == 2:
                piece = boardPieces[j][i]
                boardMarker = copy.deepcopy(boardMarkerEmpty)
                boardMarker = moveOption(boardPieces, boardMarker, boardPlayer, (j, i), True)

                if boardMarker[kingPos[0]][kingPos[1]] == 4:
                    boardMarker = boardMarkerCopy
                    #boardPlayer, boardPieces, boardMarker = flip(boardPlayer, boardPieces, boardMarker)
                    return True

    boardMarker = boardMarkerCopy

    return False


def kingInDanger(initialPos, finalPos, boardPlayer, boardPieces, boardMarker):
    boardPieces1 = copy.deepcopy(boardPieces)
    boardPlayer1 = copy.deepcopy(boardPlayer)
    boardMarker1 = resetMarker()

    boardPieces1[finalPos[0]][finalPos[1]] = boardPieces1[initialPos[0]][initialPos[1]]  # moves piece to chosen position
    boardPieces1[initialPos[0]][initialPos[1]] = "o"  # previous position is now empty

    boardPlayer1[finalPos[0]][finalPos[1]] = 1  # new position is occupied by team piece
    boardPlayer1[initialPos[0]][initialPos[1]] = 0  # previous position is now empty

    if isKingCheck(boardPieces1, boardPlayer1, boardMarker):
        return True
    else:
        return False


def resetMarker():
    boardMarker1 = []
    for j in range(8):
        row1 = []
        for i in range(8):
            row1.append((i + j) % 2)
        boardMarker1.append((row1))
    return boardMarker1


def isCheckMate(boardPlayer, boardPieces):
    boardMarker1 = resetMarker()
    boardPieces1 = copy.deepcopy(boardPieces)
    boardPlayer1 = copy.deepcopy(boardPlayer)

    for j in range(8):
        for i in range(8):
            if boardPlayer[j][i] == 1:
                initialPos = [j, i]

                boardMarker1 = resetMarker()
                boardPieces1 = copy.deepcopy(boardPieces)
                boardPlayer1 = copy.deepcopy(boardPlayer)

                boardMarker1 = moveOption(boardPieces, boardMarker1, boardPlayer, (j, i), False)
                for y in range(8):
                    for x in range(8):
                        finalPos = [y, x]
                        if boardMarker1[y][x] in [3, 4] and [y, x] != [j, x]:
                            boardPieces1[finalPos[0]][finalPos[1]] = boardPieces1[initialPos[0]][initialPos[1]]  # moves piece to chosen position
                            boardPieces1[initialPos[0]][initialPos[1]] = "o"  # previous position is now empty

                            boardPlayer1[finalPos[0]][finalPos[1]] = 1  # new position is occupied by team piece
                            boardPlayer1[initialPos[0]][initialPos[1]] = 0  # previous position is now empty

                            if not isKingCheck(boardPieces1, boardPlayer1, boardMarker1):
                                return False



    return True








# prints out the different boards for debugging purposes
def debug(boardPieces, boardMarker, boardPlayer):
    print("___________________________")
    for row in boardPieces:
        print(row)
    print("\n\n")
    for row in boardMarker:
        print(row)
    print("\n\n")
    for row in boardPlayer:
        print(row)
    print("\n\n")


# Main game loop
while True:

    display.fill((0, 0, 0))  # makes display black
    screen.fill((255, 200, 90))

    mx, my = pygame.mouse.get_pos()  # gets cursor co-ords
    loc = [mx, my]
    click = 0  # indicates whether mouse has been clicked

    for event in pygame.event.get():  # event loop
        if event.type == QUIT:  # checks if window is closed
            pygame.quit()  # stops pygame
            sys.exit()  # stops script
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:  # left click
                click = 1

    """if rotating:
        angle += 5
        if angle >= 180:
            rotating = False"""

    ignore = None
    boardMarker, initialPos = cursor(loc, tileSize, boardStart, boardMarker, boardPlayer, click, initialPos)
    drawBoard(boardRects, boardMarker)

    if moving:

        # grads = [0,0]
        mx = loc[0] - boardStart[0]
        my = loc[1] - boardStart[1]

        if click == 1:
            for j in range(0, tileSize * 8, tileSize):
                if my >= j and my <= j + tileSize:
                    for i in range(0, tileSize * 8, tileSize):
                        if mx >= i and mx <= i + tileSize:
                            if boardMarker[j // tileSize][i // tileSize] in [3, 4] and [j,i] != initialPos:  # when valid move is clicked, cannot be itself
                                finalPos = [j, i]  # pice is being moved to

                                if not kingInDanger([initialPos[0] // tileSize, initialPos[1] // tileSize], [finalPos[0] //tileSize, finalPos[1] // tileSize], boardPlayer, boardPieces, boardMarker):
                                    animation = True
                                    grads = [(j - initialPos[0]), (i - initialPos[1])]  # y and x speed of animation
                                else:
                                    print("KING CANNOT MOVE THERE")

                            elif boardMarker[j // tileSize][i // tileSize] in [0, 1]:
                                moving = False



        if animation:
            piece = boardPieces[initialPos[0] // tileSize][initialPos[1] // tileSize]  # piece being moved
            maxx = max(abs(grads[0]), abs(grads[1]))
            grads = [grads[0] / maxx * 1.5, grads[1] / maxx * 1.5]

            tempJI[0] += grads[0]  # increases displacement
            tempJI[1] += grads[1]  # increases displacement

            done = [False, False]

            # when animation piece has reached correct destination, done will equal [True, True]
            if grads[0] >= 0:
                if initialPos[0] + tempJI[0] >= finalPos[0]:
                    done[0] = True
            else:
                if initialPos[0] + tempJI[0] <= finalPos[0]:
                    done[0] = True

            if grads[1] >= 0:
                if initialPos[1] + tempJI[1] >= finalPos[1]:
                    done[1] = True
            else:
                if initialPos[1] + tempJI[1] <= finalPos[1]:
                    done[1] = True

            if done == [True, True]:

                initialPos = [initialPos[0] // tileSize, initialPos[1] // tileSize]
                finalPos = [finalPos[0] // tileSize, finalPos[1] // tileSize]

                boardPieces[finalPos[0]][finalPos[1]] = boardPieces[initialPos[0]][
                    initialPos[1]]  # moves piece to chosen position
                boardPieces[initialPos[0]][initialPos[1]] = "o"  # previous position is now empty

                boardPlayer[finalPos[0]][finalPos[1]] = 1  # new position is occupied by team piece
                boardPlayer[initialPos[0]][initialPos[1]] = 0  # previous position is now empty

                if pauseTime <= 0:
                    moving = False
                    animation = False
                    rotating = True
                    tempJI = [0, 0]
                    pauseTime = pauseTimeMark



                    initialPos = [0, 0]
                    finalPos = [0, 0]

                    turn = (turn + 1) % 2

                    boardPlayer, boardPieces, boardMarker = \
                    flip(boardPlayer, boardPieces, boardMarker)


                    inCheck, inCheckMate = False, False
                    if isKingCheck(boardPieces, boardPlayer, boardMarker):
                        if isCheckMate(boardPlayer, boardPieces):
                            inCheckMate = True
                            print("CHECKMATE")
                        else:
                            inCheck = True
                            print("JUST CHECKK")
                else:
                    pauseTime -= 1


                #debug(boardPieces, boardMarker, boardPlayer)  # prints boards

            else:
                ignore = [initialPos[0] // tileSize,
                          initialPos[1] // tileSize]  # the piece being moved should be ignored
                display.blit(pieces[piece][turn], [initialPos[1] + tempJI[1],
                                             initialPos[0] + tempJI[0]])  # display moving piece with displacement

    drawPieces(boardPieces, turn, boardPlayer, ignore)
    drawText(texts, fontStyle, DISPLAY_SIZE, inCheck, inCheckMate, turn, darkBrown, boardStart)

    """if rotating:
        displayCopy = pygame.transform.rotate(display, angle)
        screen.blit(displayCopy, (175 - int(displayCopy.get_width() / 2), 150 - int(displayCopy.get_height() / 2)))
    else:"""

    #mainDisplay = pygame.transform.scale(display, WINDOW_SIZE)
    screen.blit(display, (boardStart[0], boardStart[1]))

    pygame.display.update()  # update display
    clock.tick(60)  # set frame rate
