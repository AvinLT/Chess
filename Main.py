# Made by Avin Lanson

from pygame.locals import *
import sys
import copy
from ImageAndBoards import *



clock = pygame.time.Clock()  # initialize clock
pygame.init()  # initialize pygame

WINDOW_SIZE = (650, 630)  # window size
DISPLAY_SIZE = (512, 512)  # display size
display = pygame.Surface(DISPLAY_SIZE)  # what we display images on. later print 'display' on screen
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)  # initialize window

# font styles
fontStyle = pygame.font.SysFont("franklingothicmedium", 60, bold = True)
fontStyle1 = pygame.font.SysFont("franklingothicmedium", 20, bold = True)

# texts to be shown on screen
textBlack =     "     BLACK'S MOVE     "
textWhite =     "     WHITE'S MOVE     "
textCheck =     "       IN CHECK       "
textCHECKMATE = "      CHECKMATE!      "
testNotify =    "    KING IN DANGER !  "

texts = [textBlack, textWhite, textCheck, textCHECKMATE, testNotify]

boardStart = (64, 32)  # top left corner of board
tileSize = 64
borderSize = 4 # size of the border around the board

# colour codes
white = (255, 255, 255)
black = (0, 0, 0)
brown = (220, 155, 60)
darkBrown = (145, 85, 0)
cream = (255, 221, 143)
cream1 = (250, 183, 92)
lightGreen = (167, 253, 137)
darkGreen = (59, 236, 58)
lightRed = (255, 84, 84)

tempJI = [0, 0]  # displacement of the piece for original position when moving
animation = False  # the animation of a piece is occuring
moving = False  # player is in the process of choosing a piece, include animation
initialPos = [0, 0]  # initial position of piece picked
grads = [0, 0]  # y and x speed of the piece in animation
ignore = None  # holds positon of the piece which is in animation.
turn = 0 # 0 means its white's turn, 1 means its black's turn
inCheck = False
inCheckMate = False

notify = False # if True, notification will be on screen
notifyTime = 0 # if +ive, notify is True, else, decremented by 1
notifyTimeMark = 80 # notifyTime resets to this value

pauseTimeMark = 60 # pauseTime resets to this value
pauseTime = pauseTimeMark # used for the pause after the animation of a move, if +ive, still in pause

# rect for the reset button
resetRect = pygame.Rect(tileSize * 8 - resetImage.get_width() + boardStart[0] + 45,
                        tileSize * 8  + boardStart[1] + 15,
                        resetImage.get_width(), resetImage.get_height())


boardRects = []  # a board of Rects for each tile
boardMarker = []  # a board with numbers corresponding to the colour of the tile
for j in range(8): # fills boardMarker and boardRects
    row = []
    row1 = []
    for i in range(8):
        row.append(pygame.Rect(i * tileSize, j * tileSize, tileSize, tileSize))
        row1.append((i + j) % 2)
    boardRects.append(row)
    boardMarker.append((row1))


# draws board using boardMarker
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
                pygame.draw.rect(display, darkGreen, boardRects[j][i], 1) # border
            elif boardMarker[j][i] == 4:  # tile where the cursor is on
                pygame.draw.rect(display, lightRed, boardRects[j][i])

    # border of the board
    pygame.draw.rect(display, darkBrown, pygame.Rect(0, 0, tileSize * 8, tileSize * 8), borderSize)


# draws chess pieces on board
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

# draw the text below the board
def drawText(texts, fontStyle, fontStyle1, displayDim, inCheck, inCheckmate, notify, turn, textColour, boardStart):
    offsetY = 15

    if inCheck:
        textStart = [(displayDim[0] / 2 - fontStyle.size(texts[2])[0] / 2) + boardStart[0], displayDim[1] + boardStart[1] + offsetY]
        textObj = fontStyle.render(texts[2], 1, textColour)
    elif inCheckmate:
        textStart = [(displayDim[0] / 2 - fontStyle.size(texts[3])[0] / 2) + boardStart[0],displayDim[1] + boardStart[1] + offsetY]
        textObj = fontStyle.render(texts[3], 1, textColour)
    else:
        if turn == 0:
            textStart = [(displayDim[0] / 2 - fontStyle.size(texts[1])[0] / 2) + boardStart[0], displayDim[1] + boardStart[1] + offsetY]
            textObj = fontStyle.render(texts[1], 1, textColour)
        else:
            textStart = [(displayDim[0] / 2 - fontStyle.size(texts[0])[0] / 2) + boardStart[0], displayDim[1] + boardStart[1] + offsetY]
            textObj = fontStyle.render(texts[0], 1, textColour)

    if notify:
        textStart1 = [(displayDim[0] / 2 - fontStyle1.size(texts[4])[0] / 2) + boardStart[0], displayDim[1] + boardStart[1]]
        textObj1 = fontStyle1.render(texts[4], 1, textColour)
        screen.blit(textObj1, textStart1)

    screen.blit(textObj, textStart)
    screen.blit(resetImage, resetRect)


# changes the value of the appropriate element in boardMarker
# different values in boardMarker makes the tile different colours
# check drawBoard() to find which number corresponds to which colour
def cursor(loc, tileSize, boardStart, boardMarker, boardPlayer, boardPieces, click, tilePos):
    mx = loc[0] - boardStart[0]
    my = loc[1] - boardStart[1]
    global moving

    if not moving:
        tilePos = [0, 0]

    if not moving:

        # resets the boardMarker for all tiles, resets colour
        for j in range(8):
            for i in range(8):
                boardMarker[j][i] = (i + j) % 2

        # finds the tile the cursor is on
        for j in range(0, tileSize * 8, tileSize):
            if my >= j and my <= j + tileSize:
                for i in range(0, tileSize * 8, tileSize):
                    if mx >= i and mx <= i + tileSize:

                        if click == 0: # if not being clicked
                            boardMarker[j // tileSize][i // tileSize] = 2  # makes tiles dark green

                        elif click == 1: # if tile being clicked
                            if boardPlayer[j // tileSize][i // tileSize] == 1: # has to click a player piece
                                moving = True
                                tilePos = [j, i] # pos of tile being clicked
                                boardMarker[j // tileSize][i // tileSize] = 3  # makes tiles light green
                                # changes the boardMarker appropriately to show where player can move to
                                boardMarker = moveOption(boardPieces, boardMarker, boardPlayer,
                                                         (j // tileSize, i // tileSize), False)

    return boardMarker, tilePos

# reset appropriate variable to restart game
def resetButton(boardPieces, boardPlayer, boardMarker, click, loc, turn, inCheck, inCheckmate):
    mx , my = loc[0], loc[1]

    if click == 1:
        if pygame.Rect.collidepoint(resetRect, [mx, my]):
            boardPieces = copy.deepcopy(boardPiecesReset)
            boardPlayer = copy.deepcopy(boardPlayerReset)
            boardMarker = resetMarker()
            turn = 0
            inCheck = False
            inCheckmate = False

    return boardPieces, boardPlayer, boardMarker, turn, inCheck, inCheckmate

# gives a number depending on whether the tile pos in enemy, team, empty or outOfBound
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

    return 0 # empty space


# changes the appropriate elements in boardMarker to show the options of where the horse can move
def rookOption(boardMarker, boardPlayer, tilePos, OppDir):
    j, i = tilePos

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


# changes the appropriate elements in boardMarker to show the options of where the bishop can move
def bishopOption(boardMarker, boardPlayer, tilePos, OppDir):
    j, i = tilePos

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

    if piece == "p": # pawn
        if not OppDir:
            if moveValid([j - 1, i], boardPlayer, OppDir) == 0:
                boardMarker[j - 1][i] = 3
            if moveValid([j - 1, i - 1], boardPlayer, OppDir) == 2:
                boardMarker[j - 1][i - 1] = 4
            if moveValid([j - 1, i + 1], boardPlayer, OppDir) == 2:
                boardMarker[j - 1][i + 1] = 4
            if j == 6:
                if moveValid([j - 2, i], boardPlayer, OppDir) == 0 \
                        and moveValid([j - 1, i], boardPlayer, OppDir) == 0:
                    boardMarker[j - 2][i] = 3
        else:

            if moveValid([j + 1, i], boardPlayer, OppDir) == 0:
                boardMarker[j + 1][i] = 3
            if moveValid([j + 1, i + 1], boardPlayer, OppDir) == 2:
                boardMarker[j + 1][i + 1] = 4
            if moveValid([j + 1, i - 1], boardPlayer, OppDir) == 2:
                boardMarker[j + 1][i - 1] = 4
            if j == 1:
                if moveValid([j + 2, i], boardPlayer, OppDir) == 0 \
                        and moveValid([j + 1, i], boardPlayer, OppDir) == 0:
                    boardMarker[j + 2][i] = 3

    elif piece == "r": # rook
        rookOption(boardMarker, boardPlayer, tilePos, OppDir)

    elif piece == "b": # bishop
        bishopOption(boardMarker, boardPlayer, tilePos, OppDir)

    elif piece == "h": # horse
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

    elif piece == "q": # queen
        rookOption(boardMarker, boardPlayer, tilePos, OppDir)
        bishopOption(boardMarker, boardPlayer, tilePos, OppDir)

    elif piece == "k": # king
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


# mimics turning the board over to other player.
def flip(boardPlayer, boardPieces, boardMarker):
    boards = []
    for board in [boardPlayer, boardPieces, boardMarker]:

        # makes the team being played always 1 in boardPlayer, opponent will be 2
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


# checks whether king is in check by looking at all the move options for the all opponent pieces
# if any opponent piece can kill king, the return True
def isKingCheck(boardPieces, boardPlayer):
    kingPos = []

    for j in range(8): # finds the position of team king
        for i in range(8):
            if boardPieces[j][i] == "k" and boardPlayer[j][i] == 1:
                kingPos = [j, i]

    for j in range(8): # goes through all enemy pieces
        for i in range(8):
            if boardPlayer[j][i] == 2:
                boardMark = resetMarker() # resets boardMarker
                boardMark = moveOption(boardPieces, boardMark, boardPlayer, (j, i), True) # shows options for that piece

                if boardMark[kingPos[0]][kingPos[1]] == 4: # if king can be attacked
                    return True


    return False


# shows whether next move will make own king in check
def kingInDanger(initialPos, finalPos, boardPlayer, boardPieces):
    boardPieces1 = copy.deepcopy(boardPieces)
    boardPlayer1 = copy.deepcopy(boardPlayer)

    boardPieces1[finalPos[0]][finalPos[1]] = boardPieces1[initialPos[0]][initialPos[1]]  # moves piece to chosen position
    boardPieces1[initialPos[0]][initialPos[1]] = "o"  # previous position is now empty

    boardPlayer1[finalPos[0]][finalPos[1]] = 1  # new position is occupied by team piece
    boardPlayer1[initialPos[0]][initialPos[1]] = 0  # previous position is now empty

    if isKingCheck(boardPieces1, boardPlayer1):
        return True
    else:
        return False

# 1 is black, 0 is white
def resetMarker():
    boardMarker1 = []
    for j in range(8):
        row1 = []
        for i in range(8):
            row1.append((i + j) % 2)
        boardMarker1.append((row1))
    return boardMarker1


# checks whether player is in checkmate, only check when player in check
# check all possible moves player can make, if no move allow player to get out of check, then checkmate
def isCheckMate(boardPlayer, boardPieces):

    for j in range(8): # finds each team piece
        for i in range(8):
            if boardPlayer[j][i] == 1:
                initialPos = [j, i] # pos of selected team piece

                boardMarker1 = resetMarker()
                boardPieces1 = copy.deepcopy(boardPieces)
                boardPlayer1 = copy.deepcopy(boardPlayer)
                # shows all possible moves for selected piece
                boardMarker1 = moveOption(boardPieces, boardMarker1, boardPlayer, (j, i), False)

                for y in range(8): # selects a possible pos where selected piece can move to
                    for x in range(8):
                        finalPos = [y, x]

                        # for every possible move (empty or enemy space) and not a pos of itself
                        if boardMarker1[y][x] in [3, 4] and [y, x] != [j, x]:

                            boardPieces1[finalPos[0]][finalPos[1]] = boardPieces1[initialPos[0]][initialPos[1]]  # moves piece to chosen position
                            boardPieces1[initialPos[0]][initialPos[1]] = "o"  # previous position is now empty

                            boardPlayer1[finalPos[0]][finalPos[1]] = 1  # new position is occupied by team piece
                            boardPlayer1[initialPos[0]][initialPos[1]] = 0  # previous position is now empty

                            if not isKingCheck(boardPieces1, boardPlayer1): # checks if king is not in check
                                return False

    return True # if no moves can stop king being in check, then return True


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
    screen.fill(cream1)

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

    ignore = None
    boardMarker, initialPos = cursor(loc, tileSize, boardStart, boardMarker, boardPlayer, boardPieces, click, initialPos)
    drawBoard(boardRects, boardMarker)

    if moving:

        mx = loc[0] - boardStart[0]
        my = loc[1] - boardStart[1]

        if notifyTime > 0:
            notify = True
            notifyTime -= 1
        else:
            notify = False

        if click == 1:

            # if green/red (3/4) tile is clicked from move options
            for j in range(0, tileSize * 8, tileSize):
                if my >= j and my <= j + tileSize:
                    for i in range(0, tileSize * 8, tileSize):
                        if mx >= i and mx <= i + tileSize:

                            # when valid move is clicked, cannot be itself
                            if boardMarker[j // tileSize][i // tileSize] in [3, 4] and [j,i] != initialPos:
                                finalPos = [j, i]  # piece is being moved to

                                # if move doesnt make own king in danger:
                                if not kingInDanger([initialPos[0] // tileSize, initialPos[1] // tileSize],
                                                    [finalPos[0] //tileSize, finalPos[1] // tileSize],
                                                    boardPlayer, boardPieces):

                                    animation = True
                                    grads = [(j - initialPos[0]), (i - initialPos[1])]  # y and x speed of animation
                                else:
                                    # print("KING CANNOT MOVE THERE")
                                    notifyTime = notifyTimeMark # notify player that ling will be in danger

                            # if player wants to pick another piece
                            elif boardMarker[j // tileSize][i // tileSize] in [0, 1]:
                                moving = False

        if animation:
            piece = boardPieces[initialPos[0] // tileSize][initialPos[1] // tileSize]  # piece being moved
            maxx = max(abs(grads[0]), abs(grads[1]))
            grads = [grads[0] / maxx * 1.5, grads[1] / maxx * 1.5]
            done = [False, False]

            tempJI[0] += grads[0]  # increases displacement
            tempJI[1] += grads[1]  # increases displacement

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

            if done == [True, True]: # when animation is complete

                # changes appropriate elements in boards, that correspond to the move that took place
                if pauseTime == pauseTimeMark:
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
                    tempJI = [0, 0]
                    pauseTime = pauseTimeMark
                    initialPos = [0, 0]
                    finalPos = [0, 0]
                    turn = (turn + 1) % 2
                    inCheck, inCheckMate = False, False

                    # 'flips' the boards, so other player can play
                    boardPlayer, boardPieces, boardMarker = \
                    flip(boardPlayer, boardPieces, boardMarker)

                    # checks whether player in check/checkmate
                    if isKingCheck(boardPieces, boardPlayer):
                        if isCheckMate(boardPlayer, boardPieces):
                            inCheckMate = True
                            # print("CHECKMATE")
                        else:
                            inCheck = True
                            # print("JUST CHECKK")
                else:
                    pauseTime -= 1

                #debug(boardPieces, boardMarker, boardPlayer)  # prints boards

            else:
                # the piece in the initial place being moved should be ignored while the animated image is being shown
                ignore = [initialPos[0] // tileSize, initialPos[1] // tileSize]
                # display moving piece with displacement (tempJI)
                display.blit(pieces[piece][turn], [initialPos[1] + tempJI[1], initialPos[0] + tempJI[0]])

    boardPieces, boardPlayer, boardMarker, turn, inCheck, inCheckMate = \
        resetButton(boardPieces, boardPlayer, boardMarker, click, loc, turn, inCheck, inCheckMate)
    drawPieces(boardPieces, turn, boardPlayer, ignore)
    drawText(texts, fontStyle, fontStyle1, DISPLAY_SIZE, inCheck, inCheckMate, notify, turn, darkBrown, boardStart)


    screen.blit(display, (boardStart[0], boardStart[1])) # draws everything onto screen
    pygame.display.update()  # update display
    clock.tick(60)  # set frame rate

# Made by Avin Lanson