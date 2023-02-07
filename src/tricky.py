import sys, pygame
pygame.init()

size = width, height = 900, 900
speed = [2, 2]
white = 255, 255, 255
black = 0,0,0

board = pygame.display.set_mode(size)
pygame.display.set_caption('Tricky')
board.fill(white)

def lines():
    pygame.draw.line(board, black, (0, 300), (900, 300), 15)
    pygame.draw.line(board, black, (0, 600), (900, 600), 15)
    pygame.draw.line(board, black, (300, 0), (300, 900), 15)
    pygame.draw.line(board, black, (600, 0), (600, 900), 15)

lines()

#mainloop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    pygame.display.flip()