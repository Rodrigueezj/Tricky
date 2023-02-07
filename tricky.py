import pygame, sys

size = 800, 800

board = pygame.display.set_mode(size)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()