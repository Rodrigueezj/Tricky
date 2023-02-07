import sys, pygame
import numpy as np

pygame.init()

speed = [2, 2]
white = 255, 255, 255
black = 0,0,0

surface = pygame.display.set_mode((900,900))
pygame.display.set_caption('Tricky')
surface.fill(white)

class Board:
    def __init__(self):
        self.squares = np.zeros((3,3))
        print(self.squares)

    def mark(self, row, col, player):
        self.squares[row][col] = player

    def empty(self, row, col):
        return self.squares[row][col] == 0


class Game:

    def __init__(self):
        self.board = Board()
        self.player = 1
        self.lines()

    def lines(self): #board lines
        pygame.draw.line(surface, black, (0, 300), (900, 300), 15)
        pygame.draw.line(surface, black, (0, 600), (900, 600), 15)
        pygame.draw.line(surface, black, (300, 0), (300, 900), 15)
        pygame.draw.line(surface, black, (600, 0), (600, 900), 15)
    
    def next_turn(self):
        self.player = (self.player % 2) + 1

    def draw(self, row, col):
        
        if self.player == 1:
            start_desc = col * 
        elif self.player == 2:
            center  = (col * 300 + 300 // 2 , row * 300 + 300 // 2  )
            pygame.draw.circle(surface, black, center, 15)

def main():
    game = Game()
    board = game.board
    while True:                                         #   This is always the same on pygame
        for event in pygame.event.get():                #  
            if event.type == pygame.QUIT:               #  checks if we have closed the program                                                 
                pygame.quit()                           #
                sys.exit()                              #
                                                        
                                                        #casting positions into coordinatess
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos                         #position of the click(built in pygame)
                col = pos[0] // 300
                row = pos[1] // 300

                if board.empty(row, col):
                    board.mark(row, col, game.player)
                    game.draw(row, col)
                    game.next_turn()
                    print(board)
                    
 
        pygame.display.update() #update the display

main()