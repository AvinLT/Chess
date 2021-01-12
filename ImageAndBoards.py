import pygame


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
resetImage = pygame.image.load(r"Sprites\reset.png")


pieces = {"p": [pawn, pawnB], "r": [rook, rookB], "b": [bishop, bishopB],
          "q": [queen, queenB], "k": [king, kingB], "h": [horse, horseB]}




# pieces on board. Will be changed during game
boardPieces = [["r", "h", "b", "q", "k", "b", "h", "r"],
               ["p", "p", "p", "p", "p", "p", "p", "p"],
               ["o", "o", "o", "o", "o", "o", "o", "o"],
               ["o", "o", "o", "o", "o", "o", "o", "o"],
               ["o", "o", "o", "o", "o", "o", "o", "o"],
               ["o", "o", "o", "o", "o", "o", "o", "o"],
               ["p", "p", "p", "p", "p", "p", "p", "p"],
               ["r", "h", "b", "q", "k", "b", "h", "r"]]

# this board is used to reset the playing boardPieces
boardPiecesReset = [["r", "h", "b", "q", "k", "b", "h", "r"],
                   ["p", "p", "p", "p", "p", "p", "p", "p"],
                   ["o", "o", "o", "o", "o", "o", "o", "o"],
                   ["o", "o", "o", "o", "o", "o", "o", "o"],
                   ["o", "o", "o", "o", "o", "o", "o", "o"],
                   ["o", "o", "o", "o", "o", "o", "o", "o"],
                   ["p", "p", "p", "p", "p", "p", "p", "p"],
                   ["r", "h", "b", "q", "k", "b", "h", "r"]]

# used for debugging. Can get to check/checkmate in 2 moves
# Just change name to boardPieces if you want to start mid game
boardPieces1 = [["r", "o", "b", "q", "k", "b", "h", "r"],
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

# this board is used to reset the playing boardPlayer
boardPlayerReset = [[2, 2, 2, 2, 2, 2, 2, 2],
                   [2, 2, 2, 2, 2, 2, 2, 2],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [1, 1, 1, 1, 1, 1, 1, 1],
                   [1, 1, 1, 1, 1, 1, 1, 1]]

# used for debugging. Can get to check/checkmate in 2 moves
# Just change name to boardPlayer if you want to start mid game
boardPlayer1 = [[2, 0, 2, 2, 2, 2, 2, 2],
               [2, 2, 2, 2, 0, 2, 2, 2],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 2, 0, 0, 0],
               [0, 0, 0, 2, 1, 0, 1, 0],
               [0, 0, 1, 0, 0, 0, 0, 0],
               [1, 1, 1, 1, 1, 1, 1, 1],
               [1, 0, 1, 1, 1, 1, 0, 1]]
