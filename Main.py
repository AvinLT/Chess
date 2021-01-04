import pygame
from pygame.locals import *
import sys

clock = pygame.time.Clock()  # initialize clock
pygame.init()  # initialize pygame

WINDOW_SIZE = (350, 300)  # window size
DISPLAY_SIZE = (350, 300)
display = pygame.Surface(DISPLAY_SIZE)  # what we display images on. later print 'display' on screen
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)  # initialize window



piece = pygame.image.load("Sprites\pawn.png")

mapPieces = [["c","h","b","q","k","b","h","c"],
             ["p","p","p","p","p","p","p","p"],
             ["o","o","o","o","o","o","o","o"],
             ["o","o","o","o","o","o","o","o"],
             ["o","o","o","o","o","o","o","o"],
             ["o","o","o","o","o","o","o","o"],
             ["p","p","p","p","p","p","p","p"],
             ["c","h","b","k","q","b","h","c"]]

mapPlayer = [["2","2","2","2","2","2","2","2"],
             ["2","2","2","2","2","2","2","2"],
             ["0","0","0","0","0","0","0","0"],
             ["0","0","0","0","0","0","0","0"],
             ["0","0","0","0","0","0","0","0"],
             ["0","0","0","0","0","0","0","0"],
             ["1","1","1","1","1","1","1","1"],
             ["1","1","1","1","1","1","1","1"],]



while True:

    display.fill((0, 0, 0))

    for event in pygame.event.get():  # event loop
        if event.type == QUIT:  # checks if window is closed
            pygame.quit()  # stops pygame
            sys.exit()  # stops script

    display.blit(piece, [10, 10])



    mainDisplay = pygame.transform.scale(display, WINDOW_SIZE)
    screen.blit(mainDisplay, (0, 0))
    pygame.display.update()  # update display
    clock.tick(60)  # set frame rate
