import sys, pygame, copy
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
        #return 0 if draw 
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
                if self.empty_square(row, col):
                    empties.append((row, col))
        return empties

    def isfull(self):
        return self.marked_squares == 9

    def isempty(self):
        return self.marked_squares == 0

class AI:
    
    def __init__(self, player = 2):
        self.player = player

    def minimax(self, board, maximizing): #returns (evaluation, best move)
        case = board.final_state()

        #terminal cases

        if case == 1: #if player 1 wins
            return 1, None

        elif case == 2: #if player 2 wins
            return -1, None
        
        elif board.isfull(): #if draw
            return 0, None

        if maximizing:
            max_eval = -10
            best_move = None
            empty_squares = board.get_empty_squares()

            for (row, col) in empty_squares:
                temp_board = copy.deepcopy(board)
                temp_board.mark_square(row, col, 1)
                eval = self.minimax(temp_board, False)[0]

                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)

            return max_eval, best_move

        elif not maximizing:
            min_eval = 10
            best_move = None
            empty_squares = board.get_empty_squares()

            for (row, col) in empty_squares:
                temp_board = copy.deepcopy(board)
                temp_board.mark_square(row, col, 2)
                eval = self.minimax(temp_board, True)[0]

                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)

            return min_eval, best_move

    def eval(self, main_board):
        eval, move = self.minimax(main_board, False)
        print(f'AI has chosen to mark square in position {move}, with an evaluation of {eval}')
        return move      

class Game:

    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1
        self.running = True
        self.lines()

    def lines(self): #board lines
        pygame.draw.line(surface, BLACK, (0, SQSIZE), (WIDTH, SQSIZE), LINE_WIDTH)
        pygame.draw.line(surface, BLACK, (0, HEIGHT - SQSIZE), (WIDTH, HEIGHT - SQSIZE), LINE_WIDTH)

        pygame.draw.line(surface, BLACK, (SQSIZE, 0), (SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(surface, BLACK, (WIDTH - SQSIZE, 0), (WIDTH - SQSIZE, HEIGHT), LINE_WIDTH)
    
    def make_move(self, row, col):
        self.board.mark_square(row, col, self.player)
        self.draw(row, col)
        self.next_turn()
        print(self.board.squares)

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

    def isover(self):
        return self.board.final_state() != 0 or self.board.isfull()

def main():
    game = Game()
    board = game.board
    ai = game.ai
    while True:                                         #   This is always the same on pygame
        for event in pygame.event.get():                  
            if event.type == pygame.QUIT:               #  checks if we have closed the program                                                 
                pygame.quit()                           
                sys.exit()                                                                                
                                                        #casting positions into coordinatess
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos                         #position of the click(built in pygame)
                col = pos[0] // SQSIZE                  #variable x
                row = pos[1] // SQSIZE                  #variable y

                if board.empty_square(row, col) and game.running:
                    game.make_move(row, col)
                    if game.isover(): game.running = False
                    
 
        if game.player == ai.player and game.running:
            pygame.display.update()
            row, col = ai.eval(board)
            game.make_move(row, col)
            if game.isover(): game.running = False

        pygame.display.update()

main()