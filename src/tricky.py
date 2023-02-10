import sys, pygame
import numpy as np

WIDTH = 900
HEIGHT = 900

ROWS = 3
COLS = 3

SQSIZE = WIDTH // COLS
LINE_WIDTH = 15
CIRC_WIDTH = 60
CROSS_WIDTH = 15
RADIUS = SQSIZE // 4
OFFSET = 90

WHITE = 255, 255, 255
BLACK = 0,0,0

pygame.init()

surface = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Tricky')
surface.fill(WHITE)

class Board:
    def __init__(self):
        self.squares = np.zeros((ROWS,COLS))
        self.empty_squares = self.squares
        self.marked_squares = 0
        print(self.squares)

    def final_state(self):
            
        #return 1 if 1st player wins
        #return 2 if 2nd player wins

        #vertical wins
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                return self.squares[0][col]

        #horizontal wins
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                return self.squares[row][0]

        #1st diagonal win
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            return self.squares[1][1]
                    
        #2st diagonal win
        if self.squares[0][2] == self.squares[1][1] == self.squares[2][0] != 0:
            return self.squares[1][1]

        #no win yet
        return 0

    def mark_square(self, row, col, player):
        self.squares[row][col] = player
        self.marked_squares += 1

    def empty_square(self, row, col):
        return self.squares[row][col] == 0

    def get_empty_squares(self):
        empties = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty(row, col):
                    empties.append((row, col))
        return empties

    def isfull(self):
        return self.marked_squares == 9

    def isempty(self):
        return self.marked_squares == 0

class Game:

    def __init__(self):
        self.board = Board()
        #self.ai = AI()
        self.player = 1
        self.gamemode = 'pvp'
        self.running = True
        self.lines()

    def lines(self): #board lines
        pygame.draw.line(surface, BLACK, (0, SQSIZE), (WIDTH, SQSIZE), LINE_WIDTH)
        pygame.draw.line(surface, BLACK, (0, HEIGHT - SQSIZE), (WIDTH, HEIGHT - SQSIZE), LINE_WIDTH)

        pygame.draw.line(surface, BLACK, (SQSIZE, 0), (SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(surface, BLACK, (WIDTH - SQSIZE, 0), (WIDTH - SQSIZE, HEIGHT), LINE_WIDTH)
    
    def next_turn(self):
        self.player = (self.player % 2) + 1

    def draw(self, row, col):
        
        if self.player == 1:
            start_desc = (col * SQSIZE + OFFSET, row * SQSIZE + OFFSET) 
            end_desc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            pygame.draw.line(surface, BLACK, start_desc, end_desc, LINE_WIDTH)

            start_desc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + OFFSET) 
            end_desc = (col * SQSIZE + OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            pygame.draw.line(surface, BLACK, start_desc, end_desc, LINE_WIDTH)
            
        elif self.player == 2:
            center  = (col * SQSIZE + SQSIZE // 2 , row * SQSIZE + SQSIZE // 2  )
            pygame.draw.circle(surface, BLACK, center, CIRC_WIDTH)
            pygame.draw.circle(surface, WHITE, center, 50)

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
                col = pos[0] // SQSIZE                  #variable x
                row = pos[1] // SQSIZE                  #variable y

                if board.empty_square(row, col):
                    board.mark_square(row, col, game.player)
                    game.draw(row, col)
                    game.next_turn()
                    print(board.squares)
 
        pygame.display.update() #update the display

if __name__ == '__main__':
    main()